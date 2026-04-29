---
name: info-card-designer
description: |
  将任意文本/URL/信息转化为杂志质感 HTML 信息卡片，并自动截图保存为图片。
  支持直接输入 URL，自动抓取内容、提炼要点、生成卡片。
  默认在图片落盘后同时调用 wechat-draft 与 xiaohongshu-publisher。
  触发词："生成信息卡"、"做张信息卡"、"把这段内容做成卡片"、"信息卡片"、"make info card"、"generate card"、"把这个链接做成卡片"。
  卡片特点：中等信息密度、字号合适、内容饱满，瑞士国际主义 + 杂志质感，默认 900px 宽多张 4:5 卡片。
---

# Info Card Designer

将任意内容转化为杂志质感中文信息卡，默认 900px 宽、多张 `4:5`（900×1125）卡片。默认目标是**中等信息密度、字号适中、画面饱满**：读者在手机上能读清，单页不会像海报一样空，也不会像长文截图一样挤。第 1 张主信息，后续细节展开，最后一张编辑式终章收尾，逐页导出 PNG（2x → 1800×2250）。
图片落盘后默认同时进入 `wechat-draft`（newspic）与 `xiaohongshu-publisher`；用户明确要求只发其中一个或只生成卡片时跳过。

## ⚡ 执行节奏（强制）

1. **全流程 3 步完成**：获取+提炼+规划 → 生成 HTML+导出 PNG → 双平台发布
2. **不输出中间产物**：page_plan、icon_plan、选题结论等在内部完成决策，不单独输出文本块给用户；直接产出 HTML
3. **一次性生成**：读完内容后，在同一个回合内完成主题选取、布局决策、HTML 编写
4. **默认中密度优先**：普通页优先采用 `2-4` 个信息块的中等密度结构；不要把核心内容稀释成大字海报，也不要压成密集长文
5. **饱满度必须验收**：先按默认骨架导出；若出现裁切、错序、明显半页空白、单页只有标题+一行解释、或 footer 上方纯空白超过约 `12%`，必须回到 HTML 调整后重导
6. **页眉页脚必须一致**：同一套卡片选定 1 种 header shell 和 1 种 footer 变体后，全页沿用；页码可变，位置、字号、对齐、分隔线、来源格式不可变
7. **发布覆盖优先**：用户明确说“只生成”“只发微信”“只发小红书”“不要发布”时，覆盖默认双平台发布
8. **design-spec.md 按需查阅**：只搜索选定主题名定位 CSS 变量块和 Header/Footer 变体代码段，**不要全文读取**

## Step 1：获取 → 提炼 → 确定方案

> 本步骤在 **一个回合内** 完成：抓取内容 → 提炼 4-6 个要点 → 选定主题包 → 确定布局和分页。

### 1.1 内容获取（URL 输入时）

优先 Chrome DevTools MCP 打开页面提取正文；失败按以下回退：

| URL 类型                                     | 回退链                                      |
| -------------------------------------------- | ------------------------------------------- |
| `arxiv.org/abs/`                             | `arxiv.org/html/{id}v1` → `r.jina.ai` + PDF |
| `x.com` / `twitter.com` / `mp.weixin.qq.com` | `r.jina.ai`                                 |
| 其他网页                                     | `r.jina.ai` → `defuddle.md`                 |

如果 Chrome DevTools MCP 只拿到导航/页脚/登录壳层，视为失败，走回退。

### 1.2 内容提炼

**目标**：读者只看图片就能理解文章核心，不需要点进原文。

**提炼五步**：

1. 找**核心论点**（最反直觉的 1 个观点）→ 主标题
2. 找**关键数据**（具体数字、百分比、倍数）
3. 找**因果链**（A→B→C，每个环节是一个要点）
4. 砍到 **4-6 个要点**，每个 ≤ 2 句；每个要点默认写到 `30-55` 个中文字，保证卡片在手机上可读且不空
5. 为每个要点标注**角色**（🔴问题 / 🟡成因 / 🟢洞察 / 🔵证据 / ⚡转折），确保不全是同类

**主标题**：必须是结论性的——读者看完想问"为什么？"说明对了，反应"哦"说明错了。

- ✅ 用数字/动词驱动："把品牌面积放大100倍"、"雅痞拯救了机械表"
- ❌ 描述性/名词性："关于品牌的思考"、"表壳即品牌的进化"
- 产品/工具/项目类：主标题**必须包含主体名**（或使用 `split-top-title` 双层大字）

**Label**：产品/工具类格式 `品牌 · 产品名`，不能省略。
**Subtitle**：`[是什么]——[核心差异化]`。
**主体名**：必须进入 header 大字区（`main-title` 或 `subject_display + main-title`）；仅在 label 中出现视为不合格。

**⚠️ 平铺检测**：4+ 个要点都是「证据/功能描述」→ 合并同类为 1 条洞察 + 补 1 条问题 + 只留最强 1 条证据。

**排序弧线**：问题 → 洞察 → 证据 → 转折。前 2 条制造疑问，最后 1 条收束升华。

**领域叙事模板**：

| 类型      | 弧线                                                   |
| --------- | ------------------------------------------------------ |
| 工具/产品 | 🔴痛点 → 🟢核心思路 → 🟢🔵关键能力(2-3) → 🔵规模证据   |
| 研究论文  | 🔴研究缺口 → 🟢方法创新 → 🔵实验发现(1-2) → ⚡意外发现 |
| 商业/新闻 | ⚡反直觉 → 🟡背景 → 🔵关键数据(1-2) → 🟢终极洞察       |
| 观点/评论 | 🟢核心论点 → 🔵论据 → ⚡张力 → 🟢升华                  |

> 多层架构特例：产品由独立命名的分层构成（如身份层/权限层/供应链层）时，每层独立占一个要点，不压缩合并。

**金句**：从原文找最有冲击力的 1 句放引用块，可重新组织表达但不改事实。

**来源 Footer（必填）**：原始 URL + 来源类型/作者 + 发布日期 + License（有则填），用 `<br />` 分行。

**数据准确性**：引用数字忠实原文；不混用 ARR 与单月收入；保留"约""据报道"等修饰。
**内容原则**：100% 来自原文，禁止编造。Hook 改写只改表达不改事实。

### 1.2.1 内部卡片规划（不输出给用户）

生成 HTML 前必须先在内部完成 `card_plan`，但不要单独展示给用户。`card_plan` 至少覆盖：

- `page_count`：计划页数，默认 `2-6`
- `theme_id`：选定主题包
- `header_shell` / `footer_variant`：全页一致的页眉页脚方案
- `pages[]`：每页的 `role`、`core_claim`、`payload_blocks`、`density`、`layout_template`、`risk`
- `publish_target`：`both` / `wechat` / `xiaohongshu` / `none`

每页规划规则：

- `lead` 页必须有主体名、主结论、核心证据和 `2-3` 个支撑点
- `detail` 页必须有 `2-4` 个实质信息块；每块要是完整判断或解释，不是关键词堆叠
- `closing` 页必须有 `closing_title + closing_note`；若内容不足以独立成页，就并入上一页轻量收束
- 每页标记风险：`sparse` / `overflow` / `flat` / `ok`
- `sparse` 页在写 HTML 前先处理：合并页面、补充原文支持解释、或换成 P4 轻卡片块；不要靠增大 margin、拉高 gap、放大空标题来填版
- `overflow` 页在写 HTML 前先处理：拆页、删次要细节、压缩措辞，或改用 `.card-body.is-dense`；不要把正文缩到 24px 以下
- `flat` 表示要点全是同类功能/证据描述，必须补问题、洞察或转折后再分页

**编辑式终章收尾**（默认最后一张卡）：

- `closing_title`：1 句终章标题，承担真正的收束，不重复正文摘要
- `closing_note`：1-2 句编辑式补记，解释这件事为什么值得记住/转给相关人
- `closing_reflection`：可选 1 句轻量余味；只有真的自然、具体时才出现，不做评论区钩子
- 不要写“不是……而是……”这类对撞句，避免模板腔和说教感
- 跨平台中性，不写"点赞关注""三连"
- 收尾卡只做收束，不追加新知识点，不引入正文外新事实

### 1.3 主题与布局

**主题选取**：

1. 默认从 `[alert/biz/create/ember/life/midnight/neutral/ocean/rose/sci/tech]` **纯随机**选取 1 个主题包，不根据内容类别、语气、风险等级、行业属性做映射
2. 为避免连续撞同一主题，优先避开最近一次刚用过的主题；做不到时允许重复
3. 如需一个确定性备选计算，用：`(要点数 × 页数) mod 11` 取池中索引
4. 用户明确指定颜色/风格时直接覆盖随机结果

**布局**：固定 `4:5`（900×1125），只允许通过增加页数（2-6 页）来容纳内容；禁止退回单张长图或后切分流程。默认用中等密度单栏或轻卡片块结构，让内容占据页面主视觉高度的约 `72-86%`。
**密度 → 模板**：低密度(1点) → A（大字符，仅用于真正单观点）；默认中密度(2-4) → B/P4（单栏/轻卡片块）；高密度(5+) → D（列表）。密度与主题默认 header 冲突时，密度优先。能做成中密度时不要退成低密度。

**内容不足时的处理顺序**：

1. 先确认是否把原文要点压得过狠；能补充来源支持解释时，补到 `30-55` 字
2. 仍不足时，合并相邻页或把 closing 并入上一页
3. 再不足时，改为 P4 轻卡片块或加入来源中的关键数据/引用块
4. 不允许用大空白、超大标题、孤立图标或装饰线冒充内容

**内容过载时的处理顺序**：

1. 先删掉弱证据、重复背景和平台化套话
2. 仍过载时拆页，保持总页数不超过 `6`
3. 接近裁切时使用 `.card-body.is-dense` 上对齐和更紧凑的块间距
4. 不允许降低正文、引语、说明文字的字号底线

**Lucide 图标**：总量 3-6 个。优先从当前主题包的视觉气质出发，做克制、单色的装饰与导航；不要因为内容语义去推导整套风格。仅用 Lucide 官方内联 SVG，`currentColor` 单色，线宽 `1.75-2`。每页最多 1 个强色块。

从 `references/design-spec.md` 中**按主题名搜索**查阅 CSS 变量和 Header/Footer 变体代码（不全文读取）。

## Step 2：生成 HTML → 导出 PNG

> 本步骤在 **一个回合内** 完成：写 `card.html` → 使用 Chrome DevTools MCP 逐页截图 → 快速确认。

### 2.1 HTML 结构

保存路径：`outputs/[YYYYMMDD]-[主题关键词]/card.html`

**字体路径**：`@font-face` 必须使用当前仓库中 `skills/info-card-designer/assets/` 下字体文件的绝对 `file:///...` URL。不要复制 `design-spec.md` 里示例的旧机器路径；在 Windows 上要把反斜杠路径转换成浏览器可读的 `file:///D:/.../font.ttf`。

**多页结构**：`.card-deck > .card-page * N`

- 第 1 张：**lead card**（主体 + 主结论 + 核心证据 + 2-3 要点）
- 第 2 张起：**detail cards**（按主题分组，不是正文延续）
- 最后一张：**closing editorial card**（title + note + optional reflection）
  - 总页数 2-5 → 独立成页；已达 6 页 → 并入最后一张细节卡底部，用轻量终章区块收束，不把大号 `.accent-panel-strong` 当默认主容器
- 每页显式页序：`01/03`、`02/03`
- 每页必须使用同一套页眉/页脚骨架：`.card-header` 固定在页顶，`.footer` 或同一 `.footer-wrap` 固定在页底；不要第 1 页一种页眉、详情页另一种页眉、收尾页再换页脚

**硬约束**：

- `<meta name="viewport" content="width=900">`
- `--card-ratio: 4/5; --card-height: 1125px`
- 背景色用主题包 `--color-bg`
- 字号 `clamp()` 写法；**下列尺寸为下限，严禁低于**：正文 `point-body` / `pull-quote-text` / `closing-note` / `closing-reflection` / `subtitle` **≥ 24px**（目标 `24-28px`）；条目标题 `point-title` **≥ 28px**（目标 `28-34px`，用 `clamp(28px, 3.2vw, 34px)`）；accent-panel 内文字 **≥ 20px**；`stat-label` **≥ 17px**；`label` / `icon-chip` / `footer` **≥ 14px**（目标 `15-18px`）；`subject-display` 默认 `clamp(64px, 8vw, 88px)`，`main-title` 默认 `clamp(44px, 5.5vw, 58px)`。除封面强标题外，不为填满画面随意放大字号
- 图标：Lucide 内联 SVG，`24x24` viewBox，`currentColor`
- 不用 `height + overflow: hidden` 强压内容
- 产品/工具/项目类：主体名必须在第 1 张 header 大字区
- 色块只承载一种主功能（引用/核心数据/关键结论/操作提示），每页最多 1 个强色块
- Header/Footer 一致性：`card.html` 中每个 `.card-page` 的第一层结构必须同构，推荐顺序为 `.card-header` → `.card-body` → `.footer`；`.card-header` 的高度、padding、左右对齐、label 样式和 `.page-index` 位置全页一致；footer 的变体、分隔线、字号、对齐、来源字段顺序全页一致
- 允许变化的只有页码文本、当前页短标签和正文内容；不允许某页隐藏 footer、某页改居中、某页加装饰符、某页改来源格式

### 2.2 默认中密度饱满骨架（强制优先）

> ⚠️ 首次生成时先用"中等密度 + 整组内容纵向居中"的骨架，而不是给每个块硬分等高。普通页至少包含 `2` 个实质信息块；只有列表明显偏长、内容接近溢出时，再切到上对齐密排。

```css
.card-page {
  display: flex;
  flex-direction: column;
  min-height: var(--card-height);
  padding: 38px;
}
.card-header {
  min-height: 34px;
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
}
.deck-label,
.page-index {
  font-family: var(--font-label);
  font-size: 16px;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--color-muted);
}
.card-body {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 18px;
}
.card-body > * {
  flex: 0 0 auto;
  display: flex;
  flex-direction: column;
}
/* 高密度页再切到上对齐 */
.card-body.is-dense {
  justify-content: flex-start;
}
/* 强调块通过内边距和字号增重，不靠等高拉伸 */
.card-body > .quote-block,
.card-body > .accent-panel,
.card-body > .accent-panel-strong {
  flex: 0 0 auto;
}
/* Footer 贴底 */
.footer {
  margin-top: auto;
}
```

**使用顺序**：

1. 先确定全套卡片的 `.card-header` 和 `.footer` 变体，复制到每一页，只替换页码；
2. 再让 `.card-body` 整体纵向居中；
3. 若正文块达到 `5+`、出现连续列表、或导出时接近裁切，再改为 `.card-body.is-dense` 上对齐；
4. 若 footer 上方纯空白超过页面高度约 `12%`，优先补足要点解释、合并/拆分页面或换成 P4 轻卡片块，不用大 margin 撑版；
5. 收尾卡也要饱满：至少包含 `closing_title + closing_note`，过空时补 `closing_reflection` 或并入上一页轻量收束。

**内容观感目标**：单页主内容区占页面主视觉高度约 `72-86%`；条目描述尽量达到 `1.5-2.5` 行（约 `30-55` 字）；普通详情页至少 `2` 个信息块，理想为 `3` 个；`stat-num` `40-46px`。内容偏少时优先补信息、合并页面或改成轻卡片块，不靠拉伸间距造饱满感。

### 2.3 视觉精修

- 三层纹理：底色 → `::after` 洗色层 → `::before` 噪点层
- 装饰线圆端 + 渐变；色块对角微渐变
- `.accent-panel-strong`：保留为其他场景的强强调块，不再作为收尾卡默认主容器
- `.stat-number`：渐变文字（`background-clip: text`）
- Footer 分隔线：`border-image: linear-gradient(...)` 渐变消隐
- `.icon-chip`：`1px border`（`--color-accent-mid`）+ 极轻阴影
- H2 header：`--color-accent-gradient` 背景 + 白字 `text-shadow`；负边距出血 `margin: -38px -38px 0`
- H3 竖条：上深下浅渐变 + `border-radius: 4px`
- `body`：`-webkit-font-smoothing: antialiased; text-rendering: optimizeLegibility`
- 多页可逐页微调洗色层角度（±8°），制造光感呼吸差异

### 2.4 导出

**默认截图链路**：必须直接使用 **Chrome DevTools MCP**；不要把 `export_pages.py`、Playwright、Puppeteer 或其他独立无头浏览器当成默认导出步骤。

`scripts/export_pages.py` 只是旧的手动/诊断辅助脚本；除非用户明确要求调试该脚本或未来说明改为允许，否则不要把它作为技能默认导出路径。

**执行流程**：

1. 先把最终 HTML 保存到 `outputs/[YYYYMMDD]-[topic]/card.html`
2. 通过 Chrome DevTools MCP 单独打开这个本地 HTML，不与其他页面混用标签上下文
3. 等待页面 `load` 完成，再等待 `document.fonts.ready`，然后额外等待一次布局稳定（约 `1500-2000ms`）
4. 用页面脚本确认 `.card-page` 至少存在 1 个，并读取总页数；未找到时直接失败
5. 按 DOM 顺序逐页导出 PNG，文件名固定为 `card-01.png`、`card-02.png` ...；保持 2x 输出，单页最终尺寸为 `1800 x 2250`
6. 导出后快速核对页数、顺序、尺寸、裁切、饱满度与页眉页脚一致性；同时目测正文字号是否清晰可读（正文在截图中应达到约 `16px` 等效手机渲染尺寸，即 900px 画布中对应 ≥ 24px）；内容完整、无裁切、无明显半页空白、字号可读、header/footer 全页一致才视为合格，可进入发布

**截图验收清单**：

- PNG 数量与 `.card-page` 数量一致
- 文件名连续：`card-01.png`、`card-02.png` ...
- 每张 PNG 为 `1800 x 2250`
- 没有裁切、重叠、错序、空白尾页或只有半页内容的独立页
- 正文、引用、说明文字在手机缩放后仍可读
- 每页 `.card-header` 和 `.footer` 结构、位置、字号、来源字段顺序一致
- 首图承担封面和主结论职责；末图自然收束，不追加正文外新事实

**失败处理**：

- Chrome DevTools MCP 不可用、未连接到可操作的 Chrome、无法打开本地 HTML、无法保存截图、或未找到 `.card-page` 时，直接报告失败
- 截图失败后**不允许**回退到 Playwright、Puppeteer、`export_pages.py` 或其他渲染器
- 缺页、错序、裁切、明显半页空白、单页内容稀疏、页眉页脚结构或视觉不一致都算导出失败，必须回到 HTML 重排

## Step 3：双平台发布

### 微信公众号（newspic）

```bash
.\.venv\Scripts\python.exe .agents\skills\wechat-draft\scripts\publish_draft.py ^
  --appid "%WECHAT_APP_ID%" --secret "%WECHAT_APP_SECRET%" ^
  --article-type newspic ^
  --title "[主标题，≤64 UTF-8 字节]" ^
  --content "[一句话总结]" ^
  --image-dir "[输出目录]"
```

- `title` ≤ 64 UTF-8 字节（~21 中文字）；压缩时优先保留主体名
- 凭据从 `.env` / 环境变量读取；缺失时提示用户
- 首张图即封面；最多 20 张

### 小红书

进入 `xiaohongshu-publisher` skill，复用同一输出目录：

- `title`：包含主体名的主标题
- `description`：一句话总结
- `topics`：仅在来源明确时传（不臆造话题）
- 依赖 Chrome DevTools MCP；未登录时暂停等待用户登录

### 向用户汇报

- 本地输出目录 + 图片数量
- 微信草稿 `media_id`
- 小红书发布状态

---

> **所有视觉参数（字号、配色、布局模板）的唯一真相源是 `references/design-spec.md`。**
