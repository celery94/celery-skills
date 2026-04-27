---
name: xiaohongshu-publisher
description: |
  使用 Chrome DevTools MCP（要求以 --autoConnect 启动）自动打开小红书创作者图文发布页，
  将本地图片或 info-card-designer 输出目录发布为小红书图文笔记。
  适用于“发小红书”“发布到小红书图文”“把这组图片发到小红书”“把 info-card 发到小红书”等场景。
  会复用用户当前 Chrome 会话；如果未登录，则暂停等待用户手动登录后继续。
---

# 小红书图文发布技能

本技能通过 **Chrome DevTools MCP + `--autoConnect`** 复用用户当前 Chrome 会话，打开固定发布页：

`https://creator.xiaohongshu.com/publish/publish?from=tab_switch&target=image`

目标是把一组本地图片发布成小红书图文笔记。v1 支持：

- 图片（单张、多张、或目录）
- 标题
- 正文描述
- 话题 / hashtags
- `info-card-designer` 输出目录直连发布

## 工作流程

1. **收集必需信息**
2. **确认 Chrome DevTools MCP 可用且为 `--autoConnect` 模式**
3. **打开小红书图文发布页**
4. **检测登录状态；如未登录则暂停等待用户手动登录**
5. **上传图片并等待缩略图全部出现**
6. **填写标题、正文、话题**
7. **执行发布前检查**
8. **点击最终发布并等待成功结果**
9. **向用户汇报发布状态**

## 所需输入

| 字段          | 必填                  | 说明                                                                                      |
| ------------- | --------------------- | ----------------------------------------------------------------------------------------- |
| `title`       | 是                    | 笔记标题                                                                                  |
| `description` | 是                    | 正文描述 / 文案                                                                           |
| `image`       | 与 `image_dir` 二选一 | 单张或多张本地图片路径                                                                    |
| `image_dir`   | 与 `image` 二选一     | 图片目录；可直接传 `info-card-designer` 输出目录                                          |
| `topics`      | 否                    | 话题数组或话题字符串；发布时尽量插入为话题，失败时回退为正文中的带空格分隔的 `#话题` 文本 |

### 图片目录规则

- 如果传入的是 `info-card-designer` 输出目录，优先按以下顺序收集：
  1. `card-01.png`, `card-02.png`, ...
  2. `card-1.png`, `card-2.png`, ...（兼容旧产物）
  3. `card.png`
- 否则，按文件名升序收集常见图片扩展名：`.png`, `.jpg`, `.jpeg`, `.webp`
- 如果目录里没有可上传图片，直接报错，不要继续打开发布流程

## Chrome DevTools MCP 要求

- **必须**使用 Chrome DevTools MCP，且浏览器连接方式为 `--autoConnect`
- **必须**复用用户当前 Chrome 会话，不要改用 Playwright、Puppeteer 或独立无头浏览器
- 如果当前环境没有 Chrome DevTools MCP 工具，直接说明无法执行此技能
- 如果工具可用但没有连接到现有 Chrome，会话不满足 `--autoConnect` 前提时，明确提示用户修正环境后再继续

## 执行步骤

### Step 1：整理输入

1. 校验 `title`、`description`、`image` / `image_dir`
2. 把图片整理为最终有序列表
3. 规范化 `topics`
   - 输入为数组：去掉空项，保持顺序
   - 输入为字符串：按用户原意拆分或保留
   - 插入页面前去掉重复项

### Step 2：打开发布页

1. 通过 Chrome DevTools MCP 打开：
   `https://creator.xiaohongshu.com/publish/publish?from=tab_switch&target=image`
2. 等待页面稳定
3. 确认当前处于“小红书创作者”图文发布上下文

### Step 3：处理登录状态

如果出现以下任一情况，视为未登录或会话失效：

- 被重定向到登录页
- 页面出现手机号 / 验证码 / 登录按钮等登录表单
- 发布区不可见，仅显示登录引导

此时：

1. 明确告诉用户需要在 **已 auto-connect 的 Chrome** 中手动完成登录
2. 暂停自动化
3. 用户确认登录完成后，重新聚焦发布页并继续

不要尝试自动输入账号、密码、验证码，也不要绕过登录流程。

### Step 4：上传图片

小红书图文发布页的上传机制分两个阶段，**不支持一次性提交多张**；每张图片必须按以下流程逐张提交：

#### 阶段 A：上传第一张（空白发布页）

1. 页面刚打开时，上传区显示一个可见的 `button[value="No file chosen"]`（"Choose Files"），通过 `take_snapshot` 找到其 `uid`
2. 直接用 `mcp_chrome-devtoo_upload_file` 以该 `uid` 上传第一张图片
3. 页面会自动切换到"图片编辑"视图，显示缩略图行，确认 "1/18" 标签出现即为成功

#### 阶段 B：追加后续图片（切换为编辑视图后）

切换到图片编辑视图后，页面的所有 `input[type="file"]` 均被隐藏（`width=0, height=0`），直接对其调用 `upload_file` 会失败；必须先通过 JS 把隐藏 input 暴露再上传：

```
对每一张待追加图片执行：
  1. evaluate_script：创建一个覆盖层代理按钮，让它触发那个隐藏的 file input
  2. take_snapshot：找到代理按钮的 uid
  3. mcp_chrome-devtoo_upload_file：以代理按钮 uid 上传该图片
  4. 等待缩略图计数更新（如 "2/18"）再继续下一张
```

**代理按钮创建脚本**（每次追加前运行）：

```javascript
// evaluate_script function body
() => {
  const inputs = document.querySelectorAll('input[type="file"]');
  // 找 accept image 且 parent 为 .top 的 input（实际为 multiple=true 的那个）
  const fileInput =
    Array.from(inputs).find(
      (inp) =>
        inp.accept.includes("png") &&
        inp.parentElement &&
        inp.parentElement.className === "top",
    ) || inputs[0];
  if (!fileInput) return "no input";

  // 确保代理按钮不重复创建
  let btn = document.getElementById("xhs-upload-proxy");
  if (!btn) {
    btn = document.createElement("button");
    btn.id = "xhs-upload-proxy";
    btn.setAttribute("aria-label", "Add more images");
    document.body.appendChild(btn);
    btn.addEventListener("click", () => fileInput.click());
  }
  // 固定放在视口左上角，保持可见
  btn.style.cssText =
    "position:fixed;top:4px;left:4px;width:60px;height:24px;opacity:0.01;z-index:99999;cursor:pointer;";
  return "proxy ready";
};
```

运行后 `take_snapshot` 会看到 `uid=X button "Add more images"`，对这个 uid 调用 `mcp_chrome-devtoo_upload_file` 即可追加一张图片。

**追加完所有图片后**，确认缩略图计数等于总张数（如 3 张时显示 "3/18"），再进入 Step 5。

#### 异常处理

- 如果代理按钮触发后 `upload_file` 没有弹出文件选择器（返回 `Failed to upload`），说明 input 点击被页面阻止；改为对 `.img-upload-area .entry` 元素直接调用 `upload_file`（点击会打开文件选择器）
- 如果页面提示图片格式不支持、超过 32MB 或数量超限（最多 18 张），立即停止并把具体错误告诉用户，不继续追加

### Step 5：填写内容

1. 找到标题输入区域并填入 `title`（用 `fill` 工具）
2. 找到正文编辑区域，**只填入正文描述部分**，不含话题标签（用 `fill` 或 `click` + `type_text`）
3. 如有 `topics`，按以下方式逐个插入：

   #### 话题插入方式（首选）

   > ⚠️ XHS 富文本编辑器会把 `#tag` 后的空格当作「话题提交符」**消耗掉**。
   > 若把多个 `#tag ` 拼成一段字符串通过 `type_text` 一次性发送，
   > 所有间隔空格会被吃掉，结果是 `#AI#TTS#Gemini` 挤在一起。
   > **必须通过话题按钮 UI 逐个插入，或使用下面的回退方案逐个发送。**

   对每个话题执行：
   1. 确保正文编辑器处于焦点（点击正文区末尾）
   2. 点击工具栏 `button " 话题"`（snapshot 中标注为 `" 话题"` 的按钮）
   3. 等待话题搜索框出现
   4. 在搜索框输入话题关键词（不含 `#`）
   5. 等待候选列表出现，点击最匹配的候选项
   6. 确认话题已插入正文（正文中出现对应的 `#话题` 样式文本）
   7. 如需插入下一个话题，重复步骤 1–6

   #### 回退方案（话题按钮 UI 不可用时）

   若话题搜索弹窗无法交互或候选始终为空：
   - 在正文末尾另起一行（`press_key Enter`）
   - 逐个发送每个标签：`type_text "#话题"` 后紧跟 `press_key Space`（让编辑器提交该 tag），
     再 `press_key Enter` 换行，再输入下一个
   - **禁止**把多个 `#tag ` 拼成一整段字符串通过 `type_text` 一次性发送

不要擅自改写用户提供的标题、正文事实内容；仅在页面明确报长度限制时，才提示用户缩短。

### Step 6：发布前检查

在点击“发布”前，**必须同时满足**：

1. 上传图片已全部成功显示
2. 标题与正文都已写入页面
3. 页面没有可见的校验错误、红字错误或上传失败提示
4. 发布按钮处于可点击状态
5. 当前页面仍是目标图文发布页，而不是草稿列表或其他后台页面

如果任一条件不满足，不要点击发布。

### Step 7：执行发布

1. 只点击一次最终“发布”
2. 点击后等待明确结果，不要在无结果时连续重复点击
3. 以以下任一信号视为成功：
   - 成功提示 / toast
   - 跳转到笔记列表、内容管理页、或新笔记详情
   - 页面出现已发布成功的明确文案
   - URL 变为 `...?published=true`（最可靠的确认方式，用 `evaluate_script` 检查 `location.href`）

如果点击后出现二次确认框，确认内容与当前发布动作一致后再继续。

### Step 8：反馈结果

成功时向用户说明：

- 已打开并使用小红书图文发布页
- 本次上传的图片数量
- 使用的标题
- 使用的话题数量（如果有）
- 已完成发布

失败时向用户说明：

- 卡在哪一步
- 页面上可见的具体报错
- 是否需要用户重新登录、补图、删减文案或手动处理页面限制

## 常见异常处理

| 场景                       | 处理方式                                                             |
| -------------------------- | -------------------------------------------------------------------- |
| Chrome DevTools MCP 不可用 | 直接说明当前环境无法执行该浏览器自动化技能                           |
| 未登录 / 登录失效          | 暂停并等待用户在 auto-connected Chrome 中手动登录，再继续            |
| 图片目录为空               | 直接失败，不打开发布页                                               |
| 图片上传部分失败           | 停止发布，报告具体失败图片或页面提示；不改变已上传的数量，不回退重传 |
| 发布按钮不可点             | 检查是否缺标题、缺正文、上传未完成、或页面存在校验错误               |
| 话题候选未出现             | 回退方案：每个 `#tag` 单独 `type_text` 后紧跟 `press_key Space`，再换行继续下一个；禁止一次性发送多个 `#tag ` 拼接字符串 |
| 点击发布后无响应           | 先观察页面状态，不要连续重复点击；仅在确认未触发提交时再决定下一步   |

## 注意事项

- 这是一个**有真实副作用**的技能；满足条件后会真正点击“小红书发布”
- 不要把“保存草稿”“预览”“取消”误当成最终发布
- 不要依赖脆弱的随机 class 名；优先使用页面可见文本、语义标签、输入控件关系和稳定属性
- 不要在同一次发布里重复提交
- 如果用户给的是 `info-card-designer` 输出目录，默认把该目录里的最终成品图按顺序全部发布
- 参考更细的页面交互规则：`references/publish-flow.md`
