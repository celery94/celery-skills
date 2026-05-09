# Cover Prompt Template

创建文章封面时，先用这个模板生成**封面 brief**和第一轮 prompt，再选择可用的图像生成 / 编辑技能执行。默认不要在这里预设某个固定 backend；只有用户明确要求 Azure 时才点名 `azure-image-gen`。

不要默认“一次生成 = 最终封面”。先确认主题、摘要弧线、主体、构图和漫画方向是否成立，再根据问题做一次定向编辑或重生。

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
  "summary_angle": "这张封面要用什么主结论或主反差讲文章",
  "narrative_flow": "before-after | 3-beat process | conflict-to-resolution | layered reveal",
  "information_blocks": [
    {
      "role": "problem | mechanism | evidence | step | contrast | takeaway",
      "source_anchor": "对应原文段落、事实或章节",
      "visual_idea": "这一块在画面里如何表达",
      "visible_label": "可选；<= 6 个汉字，或 1 个必要的产品/模型名",
      "numeric_fact": "可选；只能使用原文真实数字、比例、年份，或序号 1/2/3"
    }
  ],
  "main_metaphor": "用什么视觉隐喻表达主题",
  "primary_subject": "画面里最重要的 1 个主体",
  "subject_action": "主体正在做什么，或处于什么关系里",
  "composition": "居中主物体 / 左右对照 / 斜向推进 / 等距空间 / 单点聚焦",
  "style_direction": "按类型映射表填写",
  "comic_style": "auto | japanese-manga | american-comic",
  "comic_style_reason": "为什么选这个漫画叙事方向",
  "allowed_visible_text": ["默认 1-3 个中文短标签或数字；确有必要时最多 4 个"],
  "color_palette": ["2-4 个主色"],
  "avoid": ["和主题无关、但模型容易乱加的东西"],
  "reference_strategy": "纯文本生成 / 使用 1-2 张允许复用的本地参考图 / 编辑上一轮结果",
  "draft_goal": "第一轮先验证什么",
  "revision_targets": ["如果第一轮要改，优先改哪 1-3 项"],
  "final_prompt": "最终用于生图的 prompt"
}
```

补充要求：

- `information_blocks` 默认 `2-4` 个；宽封面不要超过 `4` 个
- 每个信息块都必须能映射回原文锚点；不能编造指标、节点名或结论
- 如果文章需要 `5+` 个点才能讲清，先压缩叙事弧线，再写 prompt
- 宽封面必须保留 `1` 个主焦点；其余信息块只承担摘要叙事，不把画面做成长图海报

## 3. 类型到基础风格的固定映射

按这个表直接选，不要重新发明基础风格。

| 类型 | 基础风格 | 主体规则 | 构图规则 | 气质 |
|---|---|---|---|---|
| `tutorial` | editorial technical illustration | 一个主工具 + 一个明确动作 | 单点聚焦或轻微斜向推进 | 清晰、可执行、不过度戏剧化 |
| `release` | product-poster style illustration | 一个主产品或主符号 | 居中主物体 + 少量辅助符号 | 新鲜、克制、有登场感 |
| `architecture` | isometric conceptual systems scene | 2-4 个模块化实体 | 等距空间或层级式关系 | 理性、结构化、非真实图表 |
| `analysis` | conceptual editorial illustration | 一个核心冲突或对照关系 | 左右对照、拉扯或边界式构图 | 有判断力，但不煽情 |
| `research` | abstract technical concept art | 一个机制或结构主意象 | 单点主结构 + 少量流动辅助线索 | 精确、克制、少人物 |

## 4. 漫画叙事方向

封面的**最终落地风格**必须明确是 `japanese-manga` 或 `american-comic` 之一；不要最后退回普通 editorial illustration、产品广告图或抽象科技氛围图。

### 4.1 选择规则

1. 用户明确指定“日漫 / manga / japanese-manga”时，直接使用 `japanese-manga`
2. 用户明确指定“美漫 / american-comic / comic-book”时，直接使用 `american-comic`
3. 用户未指定时，按下面规则自动选择：
   - `tutorial` / `release`：默认 `japanese-manga`
   - `analysis` / `research`：默认 `american-comic`
   - `architecture`：如果 `narrative_flow` 是流程推进、分层展开、左到右 pipeline，则选 `japanese-manga`；如果主叙事是冲突、对照、判断，则选 `american-comic`
4. 仍然模糊时，用这个 tie-breaker：**需要“顺着看完 2-4 个步骤/节点”时选 `japanese-manga`；否则选 `american-comic`**
5. 每次自动选择都要把原因写进 `comic_style_reason`

### 4.2 两种方向的含义

- `japanese-manga`：分镜化、墨线、速度线、黑白或有限色漫画叙事；强调节奏、流程、推进感。**不是**萌系角色海报，也不是泛“动漫头像”
- `american-comic`：粗轮廓、halftone、graphic-novel 式张力、强对照与编辑感；强调判断、冲突、结论。**不是**超级英雄电影海报

额外规则：

- 不要默认写 `pixel-art`
- 不要把“manga / comic”理解成角色海报；先满足“摘要弧线清楚、主体明确、信息块可读”
- `architecture` 与 `research` 类型可以使用漫画分镜或 callout，但不要做成真实系统图、真实仪表盘或论文图表截图

## 5. 选择生图技能

- 默认保持 backend-agnostic：根据当前环境里**可用**的图像生成 / 编辑技能完成封面，不要把模板写死到某一个特定生成器
- 封面默认是宽图，prompt 里写明 `wide cover illustration, aspect ratio 2.35:1`
- 如果所选工具先把图片输出到临时目录、默认目录或中间路径，最终选中后移动或复制到 `src/assets/{ID}/01-cover.{ext}`
- 不要让 `ogImage`、正文图片引用或微信封面引用继续指向临时生成目录
- 如果第一轮主题对但细节有问题，优先编辑或定向重生一次；每轮只改 1-3 个明确问题
- 如果第一轮主题就不对，回到 brief，至少改“摘要角度 / 主隐喻 / 构图方式”中的两项后重新生成
- 如果用户明确要求 Azure / `azure-image-gen` / Azure OpenAI，必须尊重该要求

仅在使用 `azure-image-gen` 时，参考这些参数：

- 草图阶段：`size 1504x640`，`quality low`
- 终稿阶段：`size 2256x960`，`quality medium`
- `background` 只用 `auto` 或 `opaque`
- 当前脚本即使传 `--n > 1` 也只保存第一张，所以多方案探索要分多次生成或改走编辑流

## 6. 允许信息与统一禁令

每个 prompt 都必须同时说明**允许什么**和**禁止什么**，避免“信息图摘要”和“防伪造限制”互相打架。

### 6.1 允许的可见信息

- 默认最多 `1-3` 个中文短标签 / 数字 chip，确有必要时最多 `4` 个，全部来自 `information_blocks`
- 每个标签默认 `<= 6` 个汉字；或 `1` 个必要的产品 / 模型名
- 允许 `1/2/3`、`①②③`、原文真实数字、比例、年份
- 允许箭头、panel gutter、编号贴片、callout chip、轻量对照框

### 6.2 仍然禁止的内容

- poster title / hero slogan / 长段说明文字
- 英文口号、拟声词、无关 SFX、整句英文标签
- watermark
- prompt residue
- UI screenshot
- dashboard
- fake diagram labels
- fake chart axes / legends
- fake terminal output
- fake architecture node names
- fabricated metrics or percentages
- collage of unrelated icons
- decorative clutter

默认还要避免这些常见废元素：

- 漂浮芯片
- 无意义代码雨
- 霓虹高楼背景
- 通用机器人站姿
- 赛博朋克紫蓝光污染
- 巨量 HUD 浮层

如果第一轮结果里出现这些元素，优先在第二轮 prompt 里明确写 `remove / no / avoid`，不要寄希望于模型自己悟出来。

## 7. Prompt 骨架

### 7.1 第一轮：草图生成 prompt

用下面这套结构输出**第一轮草图 prompt**：

```text
Use case: infographic-story
Asset type: wide cover infographic illustration for a Chinese tech blog article
Primary request: Create a wide cinematic infographic-story cover illustration that summarizes the article. Theme: {核心主题}. The reader should quickly feel {读者收获}.

Summary angle: {摘要角度}.
Narrative flow: {叙事弧线}. In a 2.35:1 frame, keep one dominant focal subject and 2-4 supporting narrative beats. Each beat must map to the article's information blocks rather than generic decoration.
Information blocks:
- {信息块 1：role + source-grounded summary + visible label + numeric fact}
- {信息块 2：role + source-grounded summary + visible label + numeric fact}
- {信息块 3：可选}
- {信息块 4：可选}

Main metaphor: {封面主隐喻}.
Subject: {主视觉主体}, {主体动作}.
Composition/framing: {构图方式}. Prefer horizontal or radial storytelling that stays legible in a wide cover.
Style/medium: final style must be {漫画叙事方向}, interpreted through {基础风格}. Stylized, polished, editorial, visually strong, and clearly readable as an infographic-style summary cover.
Color palette: {色彩限制}.
Visible text policy: allow only 1-3 short Chinese labels or number chips by default, and no more than 4 when strictly necessary, all sourced from the information blocks. Each label <= 6 Chinese characters or one required product/model name. No poster title, no long sentences, no English slogans, no fake UI labels, no fake chart axes, no fake architecture node names.
Constraints: no watermark, no prompt residue, no screenshots, no dashboards, no fake diagrams, no fake charts, no fake terminal output, no fabricated metrics, no unrelated icon collage, no decorative clutter.
Avoid: {禁用元素}.
```

### 7.2 第二轮：编辑 / 精修 prompt

当第一轮已经有可用方向，但需要修主体、背景、风格、误生成元素时，优先用这套结构写**编辑或定向重生 prompt**：

```text
Use the current cover direction as the base.
Keep the strongest part of the composition and preserve the summary angle: {摘要角度}.
Preserve the core metaphor: {封面主隐喻}.

Keep these information beats readable and source-grounded:
- {信息块 1}
- {信息块 2}
- {信息块 3：可选}

Change only these points:
- {第二轮修正点 1}
- {第二轮修正点 2}
- {第二轮修正点 3}

Make the image feel more like {基础风格} with {漫画叙事方向}. Preserve one clear focal subject and 2-4 supporting narrative beats in a wide 2.35:1 frame.
Primary subject should remain: {主视觉主体}, {主体动作}.
Simplify the background so that only {背景元素} remains as supporting context.
Color palette: {色彩限制}.

Visible text policy: keep only the approved 1-3 short Chinese labels or number chips from the brief, and never exceed 4 items. No poster title, no long sentence captions, no English slogans, no fake UI labels, no fake chart axes, and no fake architecture node names.
Remove any watermark, prompt residue, screenshots, dashboards, fake diagrams, fake charts, fake terminal output, fabricated metrics, unrelated icons, and decorative clutter.
Avoid {禁用元素}.
```

### 7.3 何时用参考图

- 如果已经有**允许复用的本地图片**，而且它能明确帮助模型抓住主体关系、空间结构或关键对象，可以把它作为参考图
- 第三方版权海报、品牌 KV、原站营销插画、需要精确复刻的产品界面不能作为像素级临摹对象
- 如果参考图只是原网页截图，要防止最终图看起来像“网页截图换滤镜”
- 如果第一轮主题就不对，不要强行编辑；回到 brief 重写

## 8. 使用要求

- prompt 里必须同时包含“主题”“摘要角度”“信息块”“主体”“动作”“构图”“基础风格”“漫画方向”“禁令”
- 宽封面必须保持 `1` 个主焦点 + `2-4` 个叙事信息块；不要退化成多页拼贴，也不要变成纵向长海报
- `visible_label` 和 `numeric_fact` 都必须来自 `information_blocks`；如果找不到来源依据，就删掉，不要硬加
- `architecture` 类型可以画抽象节点、连接线和分镜，但不能伪造真实系统图、模块名、坐标轴或仪表盘
- `research` 类型可以做机制示意和 callout，但不能伪造论文图表、公式结果或实验指标
- 默认不要用对话气泡；只有原文真的有一句短引语必须上图时，才允许 `1` 个极短中文引语
- 不要把“多堆一点风格词”当成唯一优化方式；清楚的摘要弧线、信息块压缩和删减杂物通常更有效

验收逻辑固定为：

- **主题不对**：回到 brief 重写，再生成
- **主题对但摘要不清楚**：压缩 `information_blocks`，重写 `summary_angle` / `narrative_flow`
- **主题对但细节不对**：优先编辑或定向重生
- **只有局部出错**：只修局部问题，不推倒整张图
- **已经合格**：移动或复制到 `src/assets/{ID}/01-cover.{ext}`，更新 Markdown / `ogImage` / 微信封面路径

合格封面的最低标准：

- 至少包含 `2` 个能映射回 brief 的叙事节点
- 只允许 `1-3` 处少量中文短标签 / 数字，不出现主标题、长句和英文长标签
- 不像真实产品截图、真实架构图、真实 dashboard 或网页截图
- 一眼能读出这是在**概括文章内容**，而不是泛科技氛围图

## 9. 示例

### 示例 1：教程类（自动选择 `japanese-manga`）

输入槽位：

- `文章标题`：在 Claude Code 里直接调用 OpenAI Codex：codex-plugin-cc 上手指南
- `文章类型`：`tutorial`
- `核心主题`：在 Claude Code 中安装和使用 OpenAI Codex 插件
- `读者收获`：快速理解安装流程和核心命令
- `摘要角度`：把“装上插件 -> 配好命令 -> 跑通工作流”压成一张封面
- `叙事弧线`：`3-beat process`
- `信息块`：
  1. `step`：装插件，标签 `装插件`
  2. `step`：补配置，标签 `配命令`
  3. `takeaway`：直接在工作台调用 Codex，标签 `跑起来`
- `封面主隐喻`：一个开发者工作台上，插件模块被接入主流程并点亮
- `主视觉主体`：终端工作台与插件模块
- `主体动作`：插件模块插入侧边槽位后，三段流程依次点亮
- `构图方式`：单点聚焦，左到右分镜推进
- `背景元素`：少量命令流线、一个简化工具徽记、柔和界面轮廓
- `基础风格`：editorial technical illustration
- `漫画方向`：`japanese-manga`
- `色彩限制`：charcoal, soft teal, warm orange, off-white
- `禁用元素`：floating robots, neon city, dense code rain

输出 prompt：

```text
Use case: infographic-story
Asset type: wide cover infographic illustration for a Chinese tech blog article
Primary request: Create a wide cinematic infographic-story cover illustration that summarizes the article. Theme: installing and using an OpenAI Codex plugin inside Claude Code. The reader should quickly feel that this is a practical hands-on workflow they can follow immediately.

Summary angle: compress the whole article into one cover that shows install, configure, and run as a clean three-beat workflow.
Narrative flow: 3-beat process. In a 2.35:1 frame, keep one dominant focal subject and 3 supporting narrative beats. Each beat must map to the article's information blocks rather than generic decoration.
Information blocks:
- step: install the plugin, visible label "装插件"
- step: wire the key commands and settings, visible label "配命令"
- takeaway: run the workflow from the workstation, visible label "跑起来"

Main metaphor: a developer workstation where one plugin module snaps into the main workflow and lights up the whole path.
Subject: a terminal-centric workstation with a plugin module, the module sliding into a side slot while a three-beat sequence lights up from left to right.
Composition/framing: single focal point with left-to-right panelized storytelling. Prefer horizontal storytelling that stays legible in a wide cover.
Style/medium: final style must be japanese-manga, interpreted through editorial technical illustration. Stylized, polished, editorial, visually strong, and clearly readable as an infographic-style summary cover.
Color palette: charcoal, soft teal, warm orange, off-white.
Visible text policy: allow at most 3 short Chinese labels sourced from the information blocks, each label <= 6 Chinese characters. No poster title, no long sentences, no English slogans, no fake UI labels, no fake chart axes, no fake architecture node names.
Constraints: no watermark, no prompt residue, no screenshots, no dashboards, no fake diagrams, no fake charts, no fake terminal output, no fabricated metrics, no unrelated icon collage, no decorative clutter.
Avoid: floating robots, neon city, dense code rain.
```

### 示例 2：架构 / 工作流类（按流程自动选择 `japanese-manga`）

输入槽位：

- `文章标题`：用 GitHub Copilot SDK 在 C# 中构建多智能体代码分析系统
- `文章类型`：`architecture`
- `核心主题`：多个专职 agent 组成顺序执行的代码分析流水线
- `读者收获`：理解多 agent 如何分工协作并汇总结果
- `摘要角度`：把“采集 -> 分析 -> 汇总”做成一张可读的工作流封面
- `叙事弧线`：`3-beat process`
- `信息块`：
  1. `step`：采集代码上下文，标签 `采集`
  2. `step`：分工分析，标签 `分析`
  3. `takeaway`：汇总成报告，标签 `汇总`
- `封面主隐喻`：一个模块化分析工厂，多个处理单元串联成流水线
- `主视觉主体`：三个分析节点与一个汇总节点
- `主体动作`：代码片段从左到右流经节点后汇总成报告
- `构图方式`：等距空间，左到右层级推进
- `背景元素`：少量连接线、结果卡片轮廓、简化数据流光带
- `基础风格`：isometric conceptual systems scene
- `漫画方向`：`japanese-manga`
- `色彩限制`：deep navy, steel blue, amber, pale cyan
- `禁用元素`：real dashboards, fake charts, hologram overload

输出 prompt：

```text
Use case: infographic-story
Asset type: wide cover infographic illustration for a Chinese tech blog article
Primary request: Create a wide cinematic infographic-story cover illustration that summarizes the article. Theme: a sequential multi-agent code analysis pipeline built with GitHub Copilot SDK in C#. The reader should quickly feel how separate agents collaborate and merge their outputs into one report.

Summary angle: compress the architecture article into one readable left-to-right workflow cover.
Narrative flow: 3-beat process. In a 2.35:1 frame, keep one dominant focal subject and 3 supporting narrative beats.
Information blocks:
- step: gather the code context, visible label "采集"
- step: specialize the analysis across dedicated agents, visible label "分析"
- takeaway: merge the results into one report, visible label "汇总"

Main metaphor: a modular analysis factory where specialized units form one clear pipeline.
Subject: three distinct analysis nodes and one final synthesis node, with code fragments moving through them from left to right and becoming a finished report.
Composition/framing: isometric scene with left-to-right staged progression. Prefer horizontal storytelling that stays legible in a wide cover.
Style/medium: final style must be japanese-manga, interpreted through isometric conceptual systems scene. Stylized, polished, editorial, visually strong, and clearly readable as an infographic-style summary cover.
Color palette: deep navy, steel blue, amber, pale cyan.
Visible text policy: allow only the approved short Chinese labels from the brief, keep them minimal, and do not exceed 3 items in this cover. No poster title, no long sentences, no fake node names, no fake chart axes, no UI labels.
Constraints: no watermark, no prompt residue, no screenshots, no dashboards, no fake diagrams, no fake charts, no fake terminal output, no fabricated metrics, no unrelated icon collage, no decorative clutter.
Avoid: real dashboards, fake charts, hologram overload.
```

### 示例 3：观点 / 分析类（自动选择 `american-comic`）

输入槽位：

- `文章标题`：GitHub Spec Kit：用规格说明驱动 AI 编程的开源工具包
- `文章类型`：`analysis`
- `核心主题`：用结构化规格约束 AI 编程过程，减少纯 prompt 驱动的混乱
- `读者收获`：理解为什么 specification 比临时 prompt 更能稳定驱动实现
- `摘要角度`：把“先写规格 -> 再交给 AI -> 返工更少”的判断做成强对照封面
- `叙事弧线`：`conflict-to-resolution`
- `信息块`：
  1. `contrast`：碎片 prompt 容易漂移，标签 `先别乱写`
  2. `mechanism`：规格蓝图提供边界，标签 `先写规格`
  3. `takeaway`：实现更稳、返工更少，标签 `少返工`
- `封面主隐喻`：一张清晰蓝图正在压住四散的草稿和碎片指令
- `主视觉主体`：中央规格蓝图与周围散乱草稿
- `主体动作`：蓝图向外施加秩序，把碎片收束成清晰路径
- `构图方式`：中心主物体，四周轻微对照与收拢
- `背景元素`：少量草稿纸边缘、路径线、被整理的碎片卡片
- `基础风格`：conceptual editorial illustration
- `漫画方向`：`american-comic`
- `色彩限制`：ink black, paper white, muted blue, restrained coral
- `禁用元素`：robot mascots, floating code blocks everywhere, poster slogans

输出 prompt：

```text
Use case: infographic-story
Asset type: wide cover infographic illustration for a Chinese tech blog article
Primary request: Create a wide cinematic infographic-story cover illustration that summarizes the article. Theme: structured specifications bringing order to AI coding workflows that would otherwise drift under pure prompt-driven development. The reader should quickly feel that clear specs create control, alignment, and execution stability.

Summary angle: turn the article into a strong editorial contrast between chaotic prompting and spec-driven execution.
Narrative flow: conflict-to-resolution. In a 2.35:1 frame, keep one dominant focal subject and 3 supporting narrative beats.
Information blocks:
- contrast: fragmented prompting drifts, visible label "先别乱写"
- mechanism: the specification defines the path, visible label "先写规格"
- takeaway: steadier execution with less rework, visible label "少返工"

Main metaphor: a precise blueprint pressing down on scattered drafts and fragmented instructions, forcing them into an ordered path.
Subject: a central specification blueprint surrounded by loose sketch pages and fragmented instruction cards, the blueprint imposing structure outward.
Composition/framing: centered main object with restrained surrounding contrast and inward convergence. Prefer wide editorial storytelling with readable contrast beats.
Style/medium: final style must be american-comic, interpreted through conceptual editorial illustration. Stylized, polished, editorial, visually strong, and clearly readable as an infographic-style summary cover.
Color palette: ink black, paper white, muted blue, restrained coral.
Visible text policy: allow at most 3 short Chinese labels sourced from the information blocks. No poster title, no long sentences, no English slogans, no fake UI labels, no fake chart axes, no fake architecture node names.
Constraints: no watermark, no prompt residue, no screenshots, no dashboards, no fake diagrams, no fake charts, no fake terminal output, no fabricated metrics, no unrelated icon collage, no decorative clutter.
Avoid: robot mascots, floating code blocks everywhere, poster slogans.
```
