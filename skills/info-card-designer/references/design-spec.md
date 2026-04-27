# 信息卡设计规范

面向 `info-card-designer` 的执行型速查规范。只保留必须遵守的视觉与结构规则，不提供教学式展开。

## Core Rules

### 固定约束

| 项       | 规则                                                                  |
| -------- | --------------------------------------------------------------------- |
| 结构     | 仅允许 `.card-deck > .card-page`                                      |
| 比例     | 固定 `4:5`，单页 `900 x 1125`                                         |
| 导出     | 2x 截图，输出 `1800 x 2250`                                           |
| 容量     | 内容变多时只允许加页，不允许退回长图                                  |
| 页数     | 默认 `2-6` 页                                                         |
| 默认观感 | 中等信息密度、字号合适、内容饱满；避免海报式空页和长文式密排          |
| 页眉页脚 | 同一套卡片全页使用同一 header shell 和 footer 变体；只允许页码变化    |
| 失败处理 | 缺少 `.card-page`、分页异常、空白尾页都视为失败，直接重排 HTML 后重导 |

### 字体与字体变量

**默认字体**：`TsangerJinKai`
**楷宋混排时正文**：`NotoSerifSC`

```html
<style>
  @font-face {
    font-family: "TsangerJinKai";
    src: url("file:///Users/joe/.claude/skills/qiaomu-info-card-designer/assets/TsangerJinKai02-W04.ttf")
      format("truetype");
    font-weight: normal;
    font-style: normal;
    font-display: block;
  }

  @font-face {
    font-family: "NotoSerifSC";
    src: url("file:///Users/joe/.claude/skills/qiaomu-info-card-designer/assets/NotoSerifSC-Regular.ttf")
      format("truetype");
    font-weight: normal;
    font-style: normal;
    font-display: block;
  }
</style>
```

```css
:root {
  --font-title: "TsangerJinKai", serif;
  --font-body: "TsangerJinKai", serif;
  --font-label: "TsangerJinKai", serif;
  --font-mono: "SF Mono", "Menlo", monospace;
}
```

### 字号底线

> 卡片在手机上观看时，900px 画布被缩放至 ~375px 宽（≈2.4 倍），
> 所有字号需在缩放后仍保持清晰可读。以下底线按此适配确定。

| 层级                                                | 默认值                     | 下限   | 说明                                  |
| --------------------------------------------------- | -------------------------- | ------ | ------------------------------------- |
| 主标题 `main-title`                                 | `clamp(44px, 5.5vw, 58px)` | `42px` | 楷体不加粗，封面可放大，详情页克制     |
| `subject-display`                                   | `clamp(64px, 8vw, 88px)`   | `60px` | 产品/工具名，视觉冲击点，不无限放大     |
| 条目标题 `h3` / `point-title`                       | `clamp(28px,3.2vw,34px)`   | `28px` | 扫读锚点，必须明显大于正文；严禁低于 28px |
| 正文 `point-desc` / `feature-text p` / `skill-desc` | `24-28px`                  | `24px` | **严禁低于 24px**；目标 24-26px           |
| 副标题 / 金句 / `quote-text` / `pull-quote-text`    | `24-28px`                  | `24px` | 不得低于正文字号                           |
| 数据锚点 `stat-num`                                 | `40-46px`                  | `38px` | 渐变文字，足够醒目但不挤占正文         |
| `closing-title`                                     | `clamp(48px,6vw,64px)`     | `44px` | 收尾卡视觉中心，不做空海报             |
| `closing-note` / `closing-reflection`               | `24-28px`                  | `24px` | 收尾卡正文与余味                       |
| `subtitle`                                          | `24-28px`                  | `24px` | 主标题下方一行                         |
| `label` / `icon-chip`                               | `16-18px`                  | `15px` | 全大写/高字距                          |
| `stat-lab`                                          | `17px`                     | `15px` | 数据标签                               |
| `skill-cmd` / 代码标签                              | `18px`                     | `16px` | monospace                              |
| 页脚 `footer`                                       | `14-16px`                  | `14px` | 保持可读即可                           |

### 基础 CSS 骨架

```css
:root {
  --card-ratio: 4 / 5;
  --card-height: 1125px;
  --color-bg: #f5f3ed;
  --color-text: #1a1a1a;
  --color-accent: #2c2c2c;
  --color-muted: #555555;
  --color-accent-soft: rgba(44, 44, 44, 0.06);
  --color-accent-mid: rgba(44, 44, 44, 0.14);
  --color-accent-gradient: linear-gradient(155deg, #2c2c2c, #444444);
}

* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body {
  margin: 0;
  background: var(--color-bg);
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-rendering: optimizeLegibility;
}

.card-deck {
  width: 900px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.card-page {
  width: 900px;
  aspect-ratio: var(--card-ratio);
  min-height: var(--card-height);
  background: var(--color-bg);
  padding: 38px;
  display: flex;
  flex-direction: column;
  gap: 24px;
  position: relative;
  overflow: hidden;
}

.card-page::before {
  content: "";
  position: absolute;
  inset: 0;
  pointer-events: none;
  z-index: 0;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.75' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.035'/%3E%3C/svg%3E");
}

.card-page::after {
  content: "";
  position: absolute;
  inset: 0;
  pointer-events: none;
  z-index: 0;
  opacity: 0.45;
  background: linear-gradient(
    168deg,
    transparent 0%,
    var(--color-accent-soft) 50%,
    transparent 100%
  );
}

.card-page > * {
  position: relative;
  z-index: 1;
}

.card-header {
  min-height: 34px;
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 16px;
}

.card-body {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 16px;
}

.card-body > * {
  flex: 0 0 auto;
  display: flex;
  flex-direction: column;
}

.card-body.is-dense {
  justify-content: flex-start;
}

.card-body > .quote-block,
.card-body > .accent-panel,
.card-body > .accent-panel-strong {
  flex: 0 0 auto;
}

.deck-label,
.page-index {
  font-family: var(--font-label);
  font-size: 16px;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--color-muted);
}

.main-title {
  font-family: var(--font-title);
  font-size: clamp(44px, 5.5vw, 58px);
  font-weight: normal;
  line-height: 1.22;
  color: var(--color-text);
  letter-spacing: 0.01em;
}

.subject-display {
  font-family: var(--font-title);
  font-size: clamp(64px, 8vw, 88px);
  font-weight: 300;
  line-height: 1.05;
  color: var(--color-accent);
  letter-spacing: -0.02em;
}

.content-body,
.point-body,
.subtitle {
  font-family: var(--font-body);
  font-size: 26px;
  line-height: 1.55;
  color: var(--color-text);
}

/* 条目正文——严禁低于 24px */
.point-desc,
.skill-desc {
  font-family: var(--font-body);
  font-size: 25px;
  line-height: 1.55;
  color: var(--color-muted);
}

/* 条目标题 */
.point-title {
  font-family: var(--font-title);
  font-size: 30px;
  font-weight: 500;
  line-height: 1.3;
  color: var(--color-text);
}

/* 数据锚点 */
.stat-num {
  font-family: var(--font-title);
  font-size: 46px;
  font-weight: 500;
}

/* 终章收尾卡 */
.closing-kicker {
  font-family: var(--font-label);
  font-size: 16px;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--color-muted);
}

.closing-mark {
  width: 36px;
  height: 4px;
  border-radius: 999px;
  background: linear-gradient(90deg, var(--color-accent), var(--color-accent-mid));
}

.closing-title {
  font-family: var(--font-title);
  font-size: clamp(58px, 7vw, 76px);
  font-weight: normal;
  line-height: 1.16;
  color: var(--color-text);
  letter-spacing: 0.01em;
}

.closing-note {
  max-width: 720px;
  font-family: var(--font-body);
  font-size: 28px;
  line-height: 1.55;
  color: var(--color-text);
}

.closing-reflection {
  max-width: 620px;
  padding: 16px 18px;
  border-left: 3px solid var(--color-accent);
  border-radius: 0 10px 10px 0;
  background: var(--color-accent-soft);
  font-family: var(--font-body);
  font-size: 26px;
  line-height: 1.55;
  color: var(--color-muted);
}

.label {
  font-family: var(--font-label);
  font-size: 16px;
  font-weight: 500;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--color-muted);
}

.accent-bar {
  width: 72px;
  height: 5px;
  border-radius: 3px;
  background: linear-gradient(
    90deg,
    var(--color-accent),
    var(--color-accent-mid)
  );
}

.accent-bar-full {
  width: 100%;
  height: 3px;
  border-radius: 2px;
  background: linear-gradient(
    90deg,
    var(--color-accent),
    var(--color-accent-mid),
    transparent
  );
}

.bg-block,
.accent-panel {
  border-radius: 10px;
  padding: 18px 20px;
  background: linear-gradient(
    135deg,
    rgba(0, 0, 0, 0.025),
    var(--color-accent-soft)
  );
}

.accent-panel-strong {
  border-radius: 12px;
  padding: 22px 24px;
  background: linear-gradient(
    135deg,
    var(--color-accent-soft),
    color-mix(in srgb, var(--color-accent) 16%, #fff)
  );
  box-shadow: 0 4px 16px var(--color-accent-mid);
}

.lucide-icon {
  width: var(--icon-size, 20px);
  height: var(--icon-size, 20px);
  fill: none;
  stroke: currentColor;
  stroke-width: var(--icon-stroke, 1.85);
  stroke-linecap: round;
  stroke-linejoin: round;
  flex-shrink: 0;
}

.icon-chip {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  width: fit-content;
  padding: 6px 12px;
  border-radius: 999px;
  background: var(--color-accent-soft);
  border: 1px solid var(--color-accent-mid);
  color: var(--color-accent);
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.04);
}

.footer {
  margin-top: auto;
  padding-top: 15px;
  font-size: 17px;
  color: var(--color-muted);
  letter-spacing: 0.05em;
  border-top: 1px solid transparent;
  border-image: linear-gradient(90deg, var(--color-accent-mid), transparent 80%)
    1;
}
```

### 页眉页脚一致性

| 项 | 规则 |
| --- | --- |
| 结构 | 每页第一层结构同构，推荐 `.card-header` → `.card-body` → `.footer` |
| 页眉 | `.card-header` 的高度、padding、左右对齐、label 样式、页码位置全页一致 |
| 页脚 | 全套卡片只选 `F1` 或 `F2` 之一；分隔线、装饰符、字号、对齐方式全页一致 |
| 文案 | 来源字段顺序固定为 `来源/作者或机构/日期/License`；缺失字段可省略但不能每页换格式 |
| 允许变化 | 页码文本、当前页短标签、正文内容 |
| 禁止 | 第 1 页隐藏页脚、收尾页换居中页脚、某页添加额外装饰符、某页把页码移动到底部 |

### 导出与验收

导出方式必须是：用 **Chrome DevTools MCP** 单独打开本地 `card.html`，并将每个 `.card-page` 按 DOM 顺序单独导出成 PNG。

导出时必须满足：

- 至少有 2 页，且文件名连续：`card-01.png`, `card-02.png` ...
- 单页尺寸为 `1800 x 2250`
- 截图前已等待页面加载、字体完成与额外布局稳定
- 缺页、裁切、错序、空白尾页都视为失败
- 不允许回退到 Playwright、Puppeteer 或其他独立渲染器
- 无裁切、无空白尾页、无只有半页内容的独立收尾页
- 每页 `.card-header` 与 `.footer` 结构和视觉一致；不一致视为失败
- 页面异常时回到 HTML 重排，不做长图切分补救

## Layout & Pagination

### 密度到模板

| 密度            | 内容量              | 默认模板 | 标题 (`main-title`)    | 正文      | 备注                     |
| --------------- | ------------------- | -------- | ---------------------- | --------- | ------------------------ |
| 低密度          | `1` 个核心观点      | 模板 `A` | `clamp(48,6vw,64px)`   | `28-30px` | 仅真正单观点使用         |
| 中密度          | `2-4` 要点          | 模板 `B/P4` | `clamp(44,5.5vw,58px)` | `24-28px` | 默认目标，单栏或轻卡片块 |
| 高密度          | `5-6` 要点          | 模板 `D` | `clamp(42,5vw,54px)`   | `24-26px` | 单栏列表，正文严禁 <24px |
| 极高密度        | `7+` 要点           | 模板 `D` | `clamp(40,5vw,52px)`   | `24px`    | 继续加页而非缩字         |
| 极高密度 + 桌面 | `7+` 且用户明确要求 | 模板 `C` | `clamp(40,5vw,52px)`   | `24px`    | 仅桌面端多栏             |

### 分页规则

| 情况           | 处理                                 |
| -------------- | ------------------------------------ |
| `1` 个核心观点 | 输出 `2` 张：主卡 + 补充/互动；若第二页过空则合并为强收尾 |
| `2-4` 要点     | 输出 `2-3` 张，优先保证每页至少 `2` 个实质信息块 |
| `5-6` 要点     | 输出 `3-4` 张                        |
| `7+` 要点      | 输出 `4-6` 张                        |
| 最后一页过空   | 合并到上一页或重排，不单独保留半空页 |
| 已达 `6` 页    | 收尾块并入最后一张细节页底部         |

### 默认纵向布局策略

| 情况 | 默认处理 |
| --- | --- |
| 低密度页 | 只在确实只有 `1` 个核心观点时使用，需配引用/数据/短注补足画面 |
| 中密度页 | 默认模板；`.card-body` 整组纵向居中，内容群占主视觉高度约 `72-86%` |
| 高密度列表页 | 改用 `.card-body.is-dense` 上对齐，避免底部裁切 |
| 收尾页内容偏少 | 先把 `closing_title + note + reflection` 当成一个纵向居中堆叠组；仍过空则并入上一页 |
| 出现空白感 | 先补足信息或合并页面，再考虑改字号；禁止只靠空白间距撑版 |

### 主体识别规则

对产品 / 工具 / 项目 / 机构 / 人物类卡片，主体名必须进入 header 顶部大字号区域。

| 合格                                        | 不合格                   |
| ------------------------------------------- | ------------------------ |
| `subject-display + main-title` 都能看出主体 | 主体名只在 `label`       |
| 只看首屏大字就知道“这张卡讲谁”              | 读完整段正文才知道主角   |
| `label` 只做辅助锚点                        | `label` 承担唯一识别职责 |

### 终章收尾规则

| 项 | 规则 |
| --- | --- |
| 位置 | 默认最后一张独立成页；若自然分页已达 `6` 页则内嵌到最后一页底部 |
| 内容顺序 | `closing_title` → `closing_note` → `optional closing_reflection` → `footer` |
| 版式 | 默认整组纵向居中；只有标题足够长、自然能撑住高度时，才改成更明显的“上重下轻” |
| 视觉 | 复用当前主题，不新增主题色；允许弱色块或短分隔承重，但 `.accent-panel-strong` 不再是默认主容器 |
| 文案 | 终章感优先于互动感；`closing_reflection` 默认可省略；避免对撞句和说教腔 |
| 禁止 | 把 2-3 段短文案等高拉满、为了填高而强行 `space-between`、空泛提问、平台腔 CTA、追加新事实、`不是……而是……` 句式 |

### 模板最小骨架

#### 模板 A

```html
<div class="card-page">
  <div class="card-header">
    <div class="deck-label">主题名</div>
    <div class="page-index">01/03</div>
  </div>
  <div class="card-body">
    <div>
      <div class="accent-bar"></div>
      <div class="subject-display">主体名</div>
      <h1 class="main-title">主结论</h1>
    </div>
    <p class="content-body">一句补充说明。</p>
  </div>
  <div class="footer">来源</div>
</div>
```

#### 模板 B

```html
<div class="card-page">
  <div class="card-header">
    <div class="deck-label">主题名</div>
    <div class="page-index">02/03</div>
  </div>
  <div class="card-body">
    <div>
      <div class="icon-chip"><span class="label">品牌 · 产品</span></div>
      <h1 class="main-title">主标题</h1>
      <p class="subtitle">一句摘要</p>
    </div>
    <div class="accent-bar-full"></div>
    <div class="bg-block"><p class="content-body">核心补充。</p></div>
  </div>
  <div class="footer">来源</div>
</div>
```

#### 模板 C

```html
<div class="card-page">
  <div class="card-header">
    <div class="deck-label">主题名</div>
    <div class="page-index">03/03</div>
  </div>
  <div class="card-body">
    <div>
      <div class="subject-display">主体名</div>
      <h1 class="main-title">主标题</h1>
    </div>
    <div class="grid-2col">
      <div>
        <div class="label">Part 01</div>
        <p class="content-body">内容</p>
      </div>
      <div>
        <div class="label">Part 02</div>
        <p class="content-body">内容</p>
      </div>
    </div>
  </div>
  <div class="footer">来源</div>
</div>
```

#### 模板 D

```html
<div class="card-page">
  <div class="card-header">
    <div class="deck-label">主题名</div>
    <div class="page-index">04/04</div>
  </div>
  <div class="card-body">
    <div>
      <h1 class="main-title">主标题</h1>
      <div class="accent-bar-full"></div>
    </div>
    <div class="points">
      <div class="point">
        <h3 class="point-title">条目标题</h3>
        <p class="point-body">描述</p>
      </div>
      <div class="point">
        <h3 class="point-title">条目标题</h3>
        <p class="point-body">描述</p>
      </div>
    </div>
  </div>
  <div class="footer">来源</div>
</div>
```

## Theme Packages

### 主题选取规则

主题包采用纯随机策略，不根据内容类别、行业、情绪、风险等级做风格推断。

主题池：

```text
alert / biz / create / ember / life / midnight / neutral / ocean / rose / sci / tech
```

执行规则：

1. 随机从主题池中选一个。
2. 优先避开最近一次完全重复；做不到时允许重复。
3. 如需确定性备选：`(要点数 × 页数) mod 11`。
4. 用户明确指定颜色/风格时直接覆盖。
5. 一旦选定主题，后续风格、字体、默认组合都沿用该主题预设。

### 主题变量总表

| theme_id   | bg        | text      | accent    | muted     | accent_soft            | accent_mid             | gradient                                  | 风格 | 字体     |
| ---------- | --------- | --------- | --------- | --------- | ---------------------- | ---------------------- | ----------------------------------------- | ---- | -------- |
| `alert`    | `#faf2f1` | `#1a0a09` | `#a82318` | `#6b3030` | `rgba(168,35,24,0.07)` | `rgba(168,35,24,0.15)` | `linear-gradient(155deg,#a82318,#c43020)` | 经典 | 全楷体   |
| `biz`      | `#faf5ec` | `#1a1206` | `#7c5800` | `#6b5030` | `rgba(124,88,0,0.07)`  | `rgba(124,88,0,0.15)`  | `linear-gradient(155deg,#7c5800,#96700a)` | 杂志 | 楷宋混排 |
| `create`   | `#f4f1f8` | `#130c1e` | `#52248a` | `#5a4070` | `rgba(82,36,138,0.07)` | `rgba(82,36,138,0.14)` | `linear-gradient(155deg,#52248a,#6b35a8)` | 杂志 | 楷宋混排 |
| `ember`    | `#f9f2ea` | `#1c0c04` | `#9c3c0e` | `#6a3c22` | `rgba(156,60,14,0.07)` | `rgba(156,60,14,0.15)` | `linear-gradient(155deg,#9c3c0e,#bc5020)` | 经典 | 全楷体   |
| `life`     | `#f2f5f2` | `#0e1a0e` | `#1a4a35` | `#3d5c45` | `rgba(26,74,53,0.07)`  | `rgba(26,74,53,0.15)`  | `linear-gradient(155deg,#1a4a35,#256b4a)` | 经典 | 全楷体   |
| `midnight` | `#f0eef8` | `#0c0a1e` | `#2a1a82` | `#4a4870` | `rgba(42,26,130,0.07)` | `rgba(42,26,130,0.15)` | `linear-gradient(155deg,#2a1a82,#3c2aaa)` | 杂志 | 楷宋混排 |
| `neutral`  | `#f5f3ed` | `#1a1a1a` | `#2c2c2c` | `#555555` | `rgba(44,44,44,0.06)`  | `rgba(44,44,44,0.14)`  | `linear-gradient(155deg,#2c2c2c,#444444)` | 经典 | 全楷体   |
| `ocean`    | `#edf4f8` | `#06202e` | `#0a6090` | `#2c607a` | `rgba(10,96,144,0.07)` | `rgba(10,96,144,0.16)` | `linear-gradient(155deg,#0a6090,#1278b0)` | 杂志 | 楷宋混排 |
| `rose`     | `#f8f0f4` | `#1c0a12` | `#8a3858` | `#6a3a50` | `rgba(138,56,88,0.07)` | `rgba(138,56,88,0.14)` | `linear-gradient(155deg,#8a3858,#a04870)` | 杂志 | 楷宋混排 |
| `sci`      | `#f0f4f5` | `#0c1a20` | `#15566e` | `#3d6070` | `rgba(21,86,110,0.07)` | `rgba(21,86,110,0.16)` | `linear-gradient(155deg,#15566e,#1a6e82)` | 杂志 | 楷宋混排 |
| `tech`     | `#f0f2f5` | `#0d1117` | `#1e3f7a` | `#4a5568` | `rgba(30,63,122,0.08)` | `rgba(30,63,122,0.18)` | 无必需                                    | 经典 | 全楷体   |

### 默认组合速查

| 主题       | Header | 条目 | Footer | 备注                               |
| ---------- | ------ | ---- | ------ | ---------------------------------- |
| `tech`     | `H2`   | `P2` | `F1`   | 低密度改 `H1`                      |
| `sci`      | `H3`   | `P2` | `F2`   |                                    |
| `biz`      | `H4`   | `P3` | `F2`   | 无核心数字改 `H1`；中密度可用 `P4` |
| `life`     | `H1`   | `P1` | `F1`   |                                    |
| `create`   | `H3`   | `P3` | `F2`   | 中密度可用 `P4`                    |
| `alert`    | `H1`   | `P1` | `F1`   |                                    |
| `neutral`  | `H1`   | `P1` | `F1`   |                                    |
| `ocean`    | `H2`   | `P3` | `F1`   | 低密度改 `H1`                      |
| `rose`     | `H1`   | `P3` | `F2`   | 中密度可用 `P4`                    |
| `ember`    | `H2`   | `P2` | `F1`   | 低密度改 `H1`                      |
| `midnight` | `H3`   | `P4` | `F2`   | 仅中密度用 `P4`                    |

密度优先于主题默认组合。若主题默认样式与页面容量冲突，先保证可读性与分页成立。

### 多页色彩呼吸

系列卡允许在同主题内微调 accent：

- 第 `1` 张用主题基准色。
- 中间页可做色相 `±10-20°` 或明度 `±10%` 微调。
- 背景色保持稳定，只调整 accent、洗色角度、局部强调块。
- 对比度必须保持 `>= 4.5:1`。

## Variant Cheat Sheet

### Label / Icon / Footer 共用规则

| 项               | 规则                                            |
| ---------------- | ----------------------------------------------- |
| header shell     | 全页固定同一 `.card-header` 结构，页码只改文本  |
| `label` 默认必加 | 产品 / 工具 / 项目 / 机构 / 人物类              |
| `label` 可省略   | 纯观点、单一数据、金句卡                        |
| 系列卡 `label`   | 可用 `主题名 · 2/5` 这类编号                    |
| 图标来源         | 仅 Lucide 官方内联 SVG，`viewBox="0 0 24 24"`   |
| 图标颜色         | 仅 `currentColor` 单色                          |
| 图标线宽         | `1.75-2`                                        |
| 图标预算         | 单页总量 `3-6`；低密度页 `0-2`                  |
| 页脚内容         | 来源、作者/机构、日期；必要时可用 `<br />` 分行 |
| footer 变体      | 全页固定 `F1` 或 `F2`；不能逐页混用             |

### Header 变体速查

| 变体 | 适用密度           | 结构特征                               | 必须遵守的限制                                                    | 默认绑定主题              |
| ---- | ------------------ | -------------------------------------- | ----------------------------------------------------------------- | ------------------------- |
| `H1` | 低/中/高           | 短 `accent-bar` + 主标题               | 最通用；主体驱动时主体名仍需进大字区                              | `neutral` `alert` `life`  |
| `H2` | 中/高              | 渐变色块底 + 白字标题 + 可选右上几何线 | 若用于页眉标题块则全页同构；否则放入 `.card-body`，不要只让封面页眉出血 | `tech` `ocean` `ember`    |
| `H3` | 中/高              | 左侧粗竖条 + 标题右置                  | 竖条是主结构，不再堆叠额外装饰线；主体名仍需进大字区              | `sci` `create` `midnight` |
| `H4` | 中密度且有核心数字 | 数字大字驱动 + 次级说明                | 无核心数字时退回 `H1`；主体名不能退回 `label`                     | `biz`                     |

### 条目变体速查

| 变体 | 适用密度          | 结构特征              | 必须遵守的限制                         | 默认绑定主题                  |
| ---- | ----------------- | --------------------- | -------------------------------------- | ----------------------------- |
| `P1` | 中/高             | 左边线 + 浅底块       | 图标只放标题行，不再叠加装饰线         | `neutral` `alert` `life`      |
| `P2` | 中/高             | 编号圆圈 + 无边线     | 必须保留左侧编号圆点；图标不能替代编号 | `tech` `sci` `ember`          |
| `P3` | 高密度            | 奇偶交替条 + 序号标签 | 适合扫描型列表；不要求每条都带图标     | `biz` `create` `ocean` `rose` |
| `P4` | 中密度 `2-4` 要点 | 卡片块 + 圆角阴影     | 高密度退回 `P2/P3`；总图标量仍守 `3-6` | `biz` `create` `midnight`     |

### Footer 变体速查

| 变体 | 结构特征                         | 限制                                 | 默认绑定主题                                    |
| ---- | -------------------------------- | ------------------------------------ | ----------------------------------------------- |
| `F1` | 标准渐变分隔线 + 左对齐正文      | 选定后每页都用 F1，字段顺序一致      | `tech` `life` `alert` `neutral` `ocean` `ember` |
| `F2` | `· · ·` 装饰符 + 无上边线 + 居中 | 选定后每页都用 F2，装饰符不能缺页    | `sci` `biz` `create` `rose` `midnight`          |

### 最小结构骨架

#### H1 / H3 / H4 通用骨架

```html
<div>
  <div class="icon-chip"><span class="label">品牌 · 对象</span></div>
  <div class="subject-display">主体名</div>
  <h1 class="main-title">主结论</h1>
  <p class="subtitle">一句摘要</p>
</div>
```

#### H2 最小骨架

```html
<div
  style="background: var(--color-accent-gradient); margin: -38px -38px 0; padding: 42px 38px 36px; overflow: hidden;"
>
  <div class="label" style="color: rgba(255,255,255,0.65);">品牌 · 对象</div>
  <div class="subject-display" style="color: #fff;">主体名</div>
  <h1 class="main-title" style="color: #fff;">主结论</h1>
</div>
```

#### P1 / P2 / P3 / P4 最小骨架

```html
<div class="point">
  <div class="point-title-row">
    <span class="icon-point">
      <svg
        class="lucide-icon"
        style="--icon-size: 18px;"
        viewBox="0 0 24 24"
        aria-hidden="true"
      ></svg>
    </span>
    <h3 class="point-title">条目标题</h3>
  </div>
  <p class="point-body">条目描述。</p>
</div>
```

#### F1 / F2 最小骨架

```html
<div class="footer">来源名称 · 作者 @handle · 日期</div>
```

```html
<div>
  <div
    style="text-align: center; color: var(--color-accent); opacity: 0.4; font-size: 14px; letter-spacing: 0.5em; margin-bottom: 4px;"
  >
    · · ·
  </div>
  <div
    class="footer"
    style="border-top: none; padding-top: 8px; text-align: center;"
  >
    来源名称 · 作者 @handle · 日期
  </div>
</div>
```

#### 终章收尾卡最小骨架

```html
<div class="card-page">
  <div style="display: flex; align-items: center; justify-content: space-between;">
    <div class="closing-kicker">Final Note</div>
    <div class="page-index">04/04</div>
  </div>

  <div class="closing-mark" style="margin-top: 10px;"></div>

  <div style="flex: 1; display: flex; flex-direction: column; justify-content: center; gap: 24px;">
    <h2 class="closing-title">真正该被记住的，是它把工作流重新收拢回同一条线。</h2>
    <p class="closing-note">当一个工具能接住切换上下文时流失的注意力，它的价值就已经超过了“更方便”这件事本身，也更接近长期可用。</p>
    <div class="closing-reflection">如果这张卡只留下一个余味，那应该是：很多团队真正卡住的地方，往往就是那些持续消耗注意力的摩擦。</div>
  </div>

  <div class="footer">来源名称 · 作者 @handle · 日期</div>
</div>
```

## Refinement Rules

### 视觉层级

| 目标     | 推荐                      | 禁止                   |
| -------- | ------------------------- | ---------------------- |
| 主锚点   | `header` + `1` 个核心色块 | 同页多个同权重大色块   |
| 内容区分 | 浅底块、留白、结构节奏    | 堆叠很多边框线         |
| 图标角色 | 扫读导航                  | 图标替代结构或主配色   |
| 收尾页   | 有明确终章重心与余味      | 把短文案硬拉成大空块   |

### 经典风格 vs 杂志风格

| 元素     | 经典风格                                | 杂志风格                                       |
| -------- | --------------------------------------- | ---------------------------------------------- |
| padding  | `38px`                                  | `44px 42px`                                    |
| 页内 gap | `24px`                                  | `28px`                                         |
| 正文     | `26px / 1.55`                           | `24px / 1.65`                                  |
| `label`  | `18px / 0.12em`                         | `17px / 0.18em`                                |
| 条目列表 | 统一节奏                                | 奇偶交替底色                                   |
| 页脚     | `F1` 更常见                             | `F2` 更常见                                    |
| 适合主题 | `alert` `life` `neutral` `tech` `ember` | `biz` `create` `sci` `ocean` `rose` `midnight` |

### 字体方案

| 方案     | 标题            | 正文            | 标签            | 适用               |
| -------- | --------------- | --------------- | --------------- | ------------------ |
| 全楷体   | `TsangerJinKai` | `TsangerJinKai` | `TsangerJinKai` | 通用、国风、克制型 |
| 楷宋混排 | `TsangerJinKai` | `NotoSerifSC`   | `TsangerJinKai` | 商业、正式、杂志风 |

楷宋混排只替换正文 `--font-body`，不要替换标题或标签。

### Pull Quote 规则

```css
.pull-quote {
  position: relative;
  padding: 24px 24px 20px;
  border-left: 4px solid var(--color-accent);
  border-radius: 0 10px 10px 0;
  background: linear-gradient(
    135deg,
    rgba(0, 0, 0, 0.025),
    var(--color-accent-soft)
  );
}

.pull-quote::before {
  content: "\201C";
  position: absolute;
  top: -4px;
  left: 12px;
  font-size: 56px;
  line-height: 1;
  color: var(--color-accent);
  opacity: 0.15;
}
```

限制：

- 金句是点睛，不是视觉重心。
- 禁止使用满底 `accent` + 白字的重反转引用块。
- 仅在页面已有明确主锚点时加入引用块。

### 阴影 / 渐变 / 圆角

| 元素                   | 规则                                                                                                            |
| ---------------------- | --------------------------------------------------------------------------------------------------------------- |
| `.icon-chip`           | `0 1px 4px rgba(0,0,0,0.04)`                                                                                    |
| `.accent-panel`        | `0 1px 6px rgba(0,0,0,0.03)`                                                                                    |
| `.accent-panel-strong` | `0 4px 16px var(--color-accent-mid)`；保留为可选强强调块，不是收尾卡默认主容器                                  |
| `P4` 卡片块            | `0 1px 3px rgba(0,0,0,0.04), 0 4px 16px var(--color-accent-mid)`                                                |
| H2 标题白字            | 可加 `text-shadow: 0 2px 12px rgba(0,0,0,0.15)`                                                                 |
| H2 装饰线              | 仅科技/学术向主题；`1px` 白线、容器 `opacity: 0.08`                                                             |
| 渐变方向               | 色块 `135deg`；H2 `155deg`；洗色层 `168deg`；整页分隔线 `90deg`                                                 |
| 圆角                   | `.accent-bar 3px`；`.bg-block 8-10px`；`.accent-panel 10px`；`.accent-panel-strong/P4 12px`；`.closing-reflection 10px`；`.icon-chip 999px` |

### 移动端紧凑与密度底线

| 项             | 规则                                   |
| -------------- | -------------------------------------- |
| 页脚以下纯空白 | 通常不应超过页面高度约 `10%`           |
| 主卡职责       | 第 `1` 页必须明显承担封面和主结论职责  |
| 高密度时优先级 | 先加页，再重组条目，最后才微调字号     |
| 多栏模板 `C`   | 仅用户明确要求桌面展示时使用           |
| 收尾页         | 允许更克制的留白，但不能只剩标题和一句话；过空时并入上一页 |

### 内容饱和度

卡片在移动端观看，最终宽度约 `375px`；所有字号被缩放约 `2.4` 倍。默认成品应是中等信息密度：看起来有内容、有层次、能一屏读完，不是空海报，也不是长文截图。

| 规则 | 说明 |
| ---- | ---- |
| 主视觉占比 | `header + card-body` 应占页面主视觉高度约 `72-86%`；footer 上方纯空白超过约 `12%` 需要重排 |
| 普通详情页块数 | 每页至少 `2` 个实质信息块，理想 `3` 个；单块页只用于强数据/强引用 |
| 条目描述 `1.5-2.5` 行 | 每个 `point-body` / `point-desc` 通常写 `30-55` 个中文字，避免短标题 + 一行释义的稀疏感 |
| 收尾页不空 | 优先把 `closing-title`、`closing-note`、`closing-reflection` 作为一个居中堆叠组；仍显空时并入上一页，不用单独半空收尾 |
| 禁止纯空间撑高 | 不依赖 `margin`、等高拉伸、或强行 `space-between` 在页面底部制造大面积空白 |
| 字号不靠极端 | 先通过内容组织和分页解决空/挤；除封面主视觉外，不用超大标题掩盖内容不足 |
| stat 数字要视觉抢眼 | `stat-num` 通常 `40-46px`，在有 `3` 个以上数据时可适当缩到 `38px`，但不能比条目标题小 |

### 输出目录与产物

默认目录：`<workspace>/outputs/[YYYYMMDD]-[topic]/`

目录内只保留：

- `card.html`
- `card-01.png`, `card-02.png` ...

生成流程：

1. 生成多页 HTML。
2. Chrome DevTools MCP 逐页截图。
3. 检查无裁切、无大面积留白、无分页异常。
4. 不合格则回到 HTML 重排。
