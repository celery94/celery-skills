# Cover Prompt Template

创建文章封面时，先用这个模板生成**封面 brief**和第一轮 prompt，再调用 `imagegen`。`azure-image-gen` 只作为明确回退路径。

不要默认“一次生成 = 最终封面”。先确认主题、主体、动作和构图是否成立，再根据问题做一次定向编辑或重生。

## 1. 先判断封面类型

只能在下面 5 类里选 1 类，不要自创新分类：

- `tutorial`：教程 / 实操
- `release`：产品更新 / 工具发布
- `architecture`：架构 / 系统设计 / 工作流
- `analysis`：观点 / 评论 / 趋势判断
- `research`：论文 / 算法 / 技术原理解读

如果拿不准：

- 明显在教人操作、配置、排错：用 `tutorial`
- 明显在介绍一个新工具、新能力、新发布：用 `release`
- 明显在讲系统关系、模块协作、agent/workflow 结构：用 `architecture`
- 明显在做判断、比较、批评、趋势分析：用 `analysis`
- 明显在拆机制、模型、算法、论文结论：用 `research`

## 2. 先保存封面 brief

生成 prompt 前先写出这些信息，并保存到 `src/assets/{ID}/cover-brief.json`。不要跳过 brief 直接写 prompt。

```json
{
  "article_title": "中文标题",
  "cover_type": "tutorial | release | architecture | analysis | research",
  "core_theme": "这篇文章到底在讲什么",
  "reader_takeaway": "读完之后能理解什么或做成什么",
  "main_metaphor": "用什么视觉隐喻表达主题",
  "primary_subject": "画面里最重要的 1 个主体",
  "subject_action": "主体正在做什么，或处于什么关系里",
  "composition": "居中主物体 / 左右对照 / 斜向推进 / 等距空间 / 单点聚焦",
  "background_elements": ["只保留 1-3 个辅助元素"],
  "style_direction": "按类型映射表填写",
  "color_palette": ["2-4 个主色"],
  "avoid": ["和主题无关、但模型容易乱加的东西"],
  "reference_strategy": "纯文本生成 / 使用 1-2 张允许复用的本地参考图 / 编辑上一轮结果",
  "draft_goal": "第一轮先验证什么",
  "revision_targets": ["如果第一轮要改，优先改哪 1-3 项"],
  "final_prompt": "最终用于生图的 prompt"
}
```

## 3. 类型到风格的固定映射

按这个表直接选，不要重新发明风格。

| 类型 | 默认风格 | 主体规则 | 构图规则 | 气质 |
|---|---|---|---|---|
| `tutorial` | editorial technical illustration | 一个主工具 + 一个明确动作 | 单点聚焦或轻微斜向推进 | 清晰、可执行、不过度戏剧化 |
| `release` | product-poster style illustration | 一个主产品或主符号 | 居中主物体 + 少量辅助符号 | 新鲜、克制、有登场感 |
| `architecture` | isometric conceptual systems scene | 2-4 个模块化实体 | 等距空间或层级式关系 | 理性、结构化、非真实图表 |
| `analysis` | conceptual editorial illustration | 一个核心冲突或对照关系 | 左右对照、拉扯或边界式构图 | 有判断力，但不煽情 |
| `research` | abstract technical concept art | 一个机制或结构主意象 | 单点主结构 + 少量流动辅助线索 | 精确、克制、少人物 |

额外规则：

- 不要默认写 `pixel-art` 或 `anime`
- 只有文章天然适合时，才允许显式加入这类风格词
- 如果用了像素风或动漫感，也要先满足“主隐喻清楚、主体明确、构图简洁”

## 4. 默认生图后端

优先使用 `imagegen`：

- 用内置 `image_gen` 工具生成第一轮封面
- 封面默认是宽图，prompt 里写明 `wide cover illustration, aspect ratio 2.35:1`
- 如果工具输出在 `$CODEX_HOME/generated_images/...`，最终选中后移动或复制到 `src/assets/{ID}/01-cover.{ext}`
- 不要让 `ogImage`、正文图片引用或微信封面引用默认生成目录
- 如果第一轮主题对但细节有问题，优先编辑或定向重生一次；每轮只改 1-3 个明确问题
- 如果第一轮主题就不对，回到 brief，至少改“主隐喻 / 主体动作 / 构图方式”中的两项后重新生成

只有在这些情况下回退到 `azure-image-gen`：

- `imagegen` 明显不可用
- `imagegen` 连续失败，且失败不是 prompt 可修正的问题
- 用户明确要求 Azure / `azure-image-gen` / Azure OpenAI

Azure 回退参数：

- 草图阶段：`size 1504x640`，`quality low`
- 终稿阶段：`size 2256x960`，`quality medium`
- `background` 只用 `auto` 或 `opaque`
- 当前脚本即使传 `--n > 1` 也只保存第一张，所以多方案探索要分多次生成或改走编辑流

## 5. 统一禁令

每个 prompt 都必须明确包含下面这些限制：

- no text
- no title
- no watermark
- no prompt residue
- no UI screenshot
- no dashboard
- no fake diagram labels
- no fake terminal output
- no collage of unrelated icons
- no decorative clutter

默认还要避免这些常见废元素：

- 漂浮芯片
- 无意义代码雨
- 霓虹高楼背景
- 通用机器人站姿
- 赛博朋克紫蓝光污染
- 巨量 HUD 浮层

如果第一轮结果里出现这些元素，优先在第二轮 prompt 里明确写 `remove / no / avoid`，不要寄希望于模型自己悟出来。

## 6. Prompt 骨架

### 6.1 第一轮：草图生成 prompt

用下面这套结构输出**第一轮草图 prompt**：

```text
Use case: stylized-concept
Asset type: wide cover illustration for a Chinese tech blog article
Primary request: Create a wide cinematic cover illustration. Theme: {核心主题}. The reader should quickly feel {读者收获}.

Main metaphor: {封面主隐喻}.
Subject: {主视觉主体}, {主体动作}.
Composition/framing: {构图方式}. Wide 2.35:1 cover composition with one clear focal point. Use {背景元素} only as supporting context.
Style/medium: {风格方向}. Stylized, polished, editorial, visually strong, suitable for a modern engineering article cover.
Color palette: {色彩限制}.
Constraints: no visible text, no title, no letters, no UI labels, no prompt residue, no watermark, no screenshots, no dashboards, no fake diagrams, no fake charts, no fake terminal output, no unrelated icons, no decorative clutter.
Avoid: {禁用元素}.
```

### 6.2 第二轮：编辑 / 精修 prompt

当第一轮已经有可用方向，但需要修主体、背景、风格、误生成元素时，优先用这套结构写**编辑或定向重生 prompt**：

```text
Use the current cover direction as the base.
Keep the strongest part of the composition and preserve the core metaphor: {封面主隐喻}.

Change only these points:
- {第二轮修正点 1}
- {第二轮修正点 2}
- {第二轮修正点 3}

Make the image feel more like {风格方向}. Preserve one clear focal point.
Primary subject should remain: {主视觉主体}, {主体动作}.
Simplify the background so that only {背景元素} remains as supporting context.
Color palette: {色彩限制}. Wide 2.35:1 cover composition.

Remove any visible text, title, letters, UI labels, fake screenshots, fake charts, fake terminal output, watermark, prompt residue, unrelated icons, and decorative clutter.
Avoid {禁用元素}.
```

### 6.3 何时用参考图

- 如果已经有**允许复用的本地图片**，而且它能明确帮助模型抓住主体关系、空间结构或关键对象，可以把它作为参考图
- 第三方版权海报、品牌 KV、原站营销插画、需要精确复刻的产品界面不能作为像素级临摹对象
- 如果参考图只是原网页截图，要防止最终图看起来像“网页截图换滤镜”
- 如果第一轮主题就不对，不要强行编辑；回到 brief 重写

## 7. 使用要求

- prompt 里必须同时包含“主题”“主体”“动作”“构图”“风格”“禁令”
- 同主题文章不能只替换名词，至少在“主隐喻 / 主体动作 / 构图方式”里改动两项
- 非教程类文章，默认不要画出操作界面截图感
- 非发布类文章，默认不要做成广告横幅
- 架构类文章可以表达“连接关系”，但不要伪造真实系统图
- 研究类文章可以抽象，但不能抽象到完全看不出主题
- 不要把“多堆一点风格词”当成唯一优化方式；清楚的主隐喻、主体关系和删减杂物通常更有效

验收逻辑固定为：

- **主题不对**：回到 brief 重写，再生成
- **主题对但细节不对**：优先编辑或定向重生
- **只有局部出错**：只修局部问题，不推倒整张图
- **已经合格**：移动或复制到 `src/assets/{ID}/01-cover.{ext}`，更新 Markdown / `ogImage` / 微信封面路径

## 8. 示例

### 示例 1：教程类

输入槽位：

- `文章标题`：在 Claude Code 里直接调用 OpenAI Codex：codex-plugin-cc 上手指南
- `文章类型`：`tutorial`
- `核心主题`：在 Claude Code 中安装和使用 OpenAI Codex 插件
- `读者收获`：快速理解安装流程和核心命令
- `封面主隐喻`：一个开发者工作台上，两套 AI 工具能力被接到同一条操作链路里
- `主视觉主体`：终端工作台与插件模块
- `主体动作`：插件模块正在插入工作台侧边槽位并点亮
- `构图方式`：单点聚焦，略微斜向推进
- `背景元素`：少量命令流线、一个简化工具徽记、柔和界面轮廓
- `风格方向`：editorial technical illustration
- `色彩限制`：charcoal, soft teal, warm orange, off-white
- `禁用元素`：floating robots, neon city, dense code rain

输出 prompt：

```text
Use case: stylized-concept
Asset type: wide cover illustration for a Chinese tech blog article
Primary request: Create a wide cinematic cover illustration. Theme: installing and using an OpenAI Codex plugin inside Claude Code. The reader should quickly feel that this is a practical hands-on workflow they can follow immediately.

Main metaphor: two AI coding capabilities connected into one developer workflow on a single workstation.
Subject: a terminal-centric developer workstation with a plugin module, the plugin module sliding into a side slot and lighting up as it connects.
Composition/framing: single focal point with a slight diagonal forward motion. Wide 2.35:1 cover composition with one clear focal point. Use a few command-like motion lines, one simplified tool emblem, and soft interface silhouettes only as supporting context.
Style/medium: editorial technical illustration. Stylized, polished, editorial, visually strong, suitable for a modern engineering article cover.
Color palette: charcoal, soft teal, warm orange, off-white.
Constraints: no visible text, no title, no letters, no UI labels, no prompt residue, no watermark, no screenshots, no dashboards, no fake diagrams, no fake charts, no fake terminal output, no unrelated icons, no decorative clutter.
Avoid: floating robots, neon city, dense code rain.
```

### 示例 2：架构 / 工作流类

输入槽位：

- `文章标题`：用 GitHub Copilot SDK 在 C# 中构建多智能体代码分析系统
- `文章类型`：`architecture`
- `核心主题`：多个专职 agent 组成顺序执行的代码分析流水线
- `读者收获`：理解多 agent 如何分工协作并汇总结果
- `封面主隐喻`：一个模块化分析工厂，多个处理单元串联成流水线
- `主视觉主体`：三个分析节点与一个汇总节点
- `主体动作`：代码片段从左到右流经节点后汇总成报告
- `构图方式`：等距空间，左到右层级推进
- `背景元素`：少量连接线、结果卡片轮廓、简化数据流光带
- `风格方向`：isometric conceptual systems scene
- `色彩限制`：deep navy, steel blue, amber, pale cyan
- `禁用元素`：real dashboards, fake charts, hologram overload

输出 prompt：

```text
Use case: stylized-concept
Asset type: wide cover illustration for a Chinese tech blog article
Primary request: Create a wide cinematic cover illustration. Theme: a sequential multi-agent code analysis pipeline built with GitHub Copilot SDK in C#. The reader should quickly feel how separate agents collaborate and merge their outputs into one report.

Main metaphor: a modular analysis factory where specialized processing units form one clear pipeline.
Subject: three distinct analysis nodes and one final synthesis node, with code fragments flowing through them from left to right and becoming a finished report.
Composition/framing: isometric scene with left-to-right staged progression. Wide 2.35:1 cover composition with one clear focal point. Use thin connection lines, report-card silhouettes, and a restrained data-flow light band only as supporting context.
Style/medium: isometric conceptual systems scene. Stylized, polished, editorial, visually strong, suitable for a modern engineering article cover.
Color palette: deep navy, steel blue, amber, pale cyan.
Constraints: no visible text, no title, no letters, no UI labels, no prompt residue, no watermark, no screenshots, no dashboards, no fake diagrams, no fake charts, no fake terminal output, no unrelated icons, no decorative clutter.
Avoid: real dashboards, fake charts, hologram overload.
```

### 示例 3：观点 / 分析类

输入槽位：

- `文章标题`：GitHub Spec Kit：用规格说明驱动 AI 编程的开源工具包
- `文章类型`：`analysis`
- `核心主题`：用结构化规格约束 AI 编程过程，减少纯 prompt 驱动的混乱
- `读者收获`：理解为什么 specification 比临时 prompt 更能稳定驱动实现
- `封面主隐喻`：一张清晰蓝图正在压住四散的草稿和碎片指令
- `主视觉主体`：中央规格蓝图与周围散乱草稿
- `主体动作`：蓝图向外施加秩序，把碎片收束成清晰路径
- `构图方式`：中心主物体，四周轻微对照与收拢
- `背景元素`：少量草稿纸边缘、路径线、被整理的碎片卡片
- `风格方向`：conceptual editorial illustration
- `色彩限制`：ink black, paper white, muted blue, restrained coral
- `禁用元素`：robot mascots, floating code blocks everywhere, poster slogans

输出 prompt：

```text
Use case: stylized-concept
Asset type: wide cover illustration for a Chinese tech blog article
Primary request: Create a wide cinematic cover illustration. Theme: structured specifications bringing order to AI coding workflows that would otherwise drift under pure prompt-driven development. The reader should quickly feel that clear specs create control, alignment, and execution stability.

Main metaphor: a precise blueprint pressing down on scattered drafts and fragmented instructions, forcing them into an ordered path.
Subject: a central specification blueprint surrounded by loose sketch pages and fragmented instruction cards, the blueprint imposing structure outward.
Composition/framing: centered main object with restrained surrounding contrast and inward convergence. Wide 2.35:1 cover composition with one clear focal point. Use a few paper edges, path lines, and partially organized fragment cards only as supporting context.
Style/medium: conceptual editorial illustration. Stylized, polished, editorial, visually strong, suitable for a modern engineering article cover.
Color palette: ink black, paper white, muted blue, restrained coral.
Constraints: no visible text, no title, no letters, no UI labels, no prompt residue, no watermark, no screenshots, no dashboards, no fake diagrams, no fake charts, no fake terminal output, no unrelated icons, no decorative clutter.
Avoid: robot mascots, floating code blocks everywhere, poster slogans.
```
