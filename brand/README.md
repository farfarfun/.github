# farfarfun 品牌标识

六个组织共用一套标识。图形是 **`ff` 连字**——两个 f 共享一道横杠，笔画在底部连成微笑弧：
`ff` 取自 **far far**，底部的弧线是 **fun**。

主组织用纯 `ff`，五个子组织沿用同一个 `ff`，只在右下角挂一枚角标区分产品线。
六个头像排在一起能看出是一家，单独拿出来又各有身份。

<table>
<tr>
<td align="center"><img src="png/icon/farfarfun-256.png" width="92"><br><code>farfarfun</code><br><sub>主组织 · 无角标</sub></td>
<td align="center"><img src="png/icon/drive-256.png" width="92"><br><code>-drive</code><br><sub>云 · 网盘</sub></td>
<td align="center"><img src="png/icon/skill-256.png" width="92"><br><code>-skill</code><br><sub>星芒 · 自研 Skill</sub></td>
</tr>
<tr>
<td align="center"><img src="png/icon/skills-256.png" width="92"><br><code>-skills</code><br><sub>叠层 · 聚合镜像</sub></td>
<td align="center"><img src="png/icon/utools-256.png" width="92"><br><code>-utools</code><br><sub>拼图 · 插件</sub></td>
<td align="center"><img src="png/icon/action-256.png" width="92"><br><code>-action</code><br><sub>播放 · Action</sub></td>
</tr>
</table>

角标的取义：网盘是云，自研 Skill 是从零迸出的星芒，聚合镜像是一摞副本，uTools 是插件，
GitHub Action 是「跑起来」。

---

## 一、四种格式

同一个图形的四种容器，按场景取用。

### icon —— 主图标

渐变圆角方。**组织头像、应用图标、favicon 都用它。**

<p>
<img src="png/icon/farfarfun-128.png" width="84">
<img src="png/icon/drive-128.png" width="84">
<img src="png/icon/skill-128.png" width="84">
<img src="png/icon/skills-128.png" width="84">
<img src="png/icon/utools-128.png" width="84">
<img src="png/icon/action-128.png" width="84">
</p>

### icon-inverse —— 反白

浅底配渐变图形。深色页眉、贴纸与印刷物上用。

<p>
<img src="png/icon-inverse/farfarfun-128.png" width="84">
<img src="png/icon-inverse/drive-128.png" width="84">
<img src="png/icon-inverse/skill-128.png" width="84">
<img src="png/icon-inverse/skills-128.png" width="84">
<img src="png/icon-inverse/utools-128.png" width="84">
<img src="png/icon-inverse/action-128.png" width="84">
</p>

### icon-circle —— 圆形容器

头像被裁成圆形的平台上不会切角。

<p>
<img src="png/icon-circle/farfarfun-128.png" width="84">
<img src="png/icon-circle/drive-128.png" width="84">
<img src="png/icon-circle/skill-128.png" width="84">
<img src="png/icon-circle/skills-128.png" width="84">
<img src="png/icon-circle/utools-128.png" width="84">
<img src="png/icon-circle/action-128.png" width="84">
</p>

### mark —— 无容器

透明底的纯图形。README 页眉、文档水印用。

<p>
<img src="png/mark/farfarfun-128.png" width="84">
<img src="png/mark/drive-128.png" width="84">
<img src="png/mark/skill-128.png" width="84">
<img src="png/mark/skills-128.png" width="84">
<img src="png/mark/utools-128.png" width="84">
<img src="png/mark/action-128.png" width="84">
</p>

---

## 二、横版组合标

图形 + 组织名，用在 README 页眉和文档封面。深浅两套，对应 GitHub 的亮色与暗色主题。

| 浅色底 | 深色底 |
|---|---|
| <img src="png/lockup/farfarfun-160.png" width="250"> | <img src="png/lockup-on-dark/farfarfun-160.png" width="250"> |
| <img src="png/lockup/drive-160.png" width="250"> | <img src="png/lockup-on-dark/drive-160.png" width="250"> |
| <img src="png/lockup/skill-160.png" width="250"> | <img src="png/lockup-on-dark/skill-160.png" width="250"> |
| <img src="png/lockup/skills-160.png" width="250"> | <img src="png/lockup-on-dark/skills-160.png" width="250"> |
| <img src="png/lockup/utools-160.png" width="250"> | <img src="png/lockup-on-dark/utools-160.png" width="250"> |
| <img src="png/lockup/action-160.png" width="250"> | <img src="png/lockup-on-dark/action-160.png" width="250"> |

> 右列在 GitHub 亮色主题下看着是白字悬空，属正常——它本来就是放进深色页眉里的。

README 页眉按主题自动切换：

```html
<picture>
  <source media="(prefers-color-scheme: dark)"
          srcset="https://raw.githubusercontent.com/farfarfun/.github/master/brand/png/lockup-on-dark/farfarfun-160.png">
  <img src="https://raw.githubusercontent.com/farfarfun/.github/master/brand/png/lockup/farfarfun-160.png"
       height="80" alt="farfarfun">
</picture>
```

---

## 三、尺寸矩阵

| 格式 | SVG | PNG 尺寸 |
|------|-----|----------|
| `icon` | 1024 母版 | 16 · 32 · 48 · 64 · 96 · 128 · 180 · 192 · 256 · 384 · 512 · 1024 |
| `icon-inverse` | 1024 母版 | 64 · 128 · 256 · 512 · 1024 |
| `icon-circle` | 1024 母版 | 64 · 128 · 256 · 512 · 1024 |
| `mark` | 1024 母版 | 32 · 64 · 128 · 256 · 512 · 1024 |
| `lockup` / `lockup-on-dark` | 宽度随组织名变化 | 高 80 · 160 · 320 |
| `favicon/<组织>.ico` | — | 单文件内含 16 · 32 · 48 · 64 · 128 · 256 |

尺寸是按实际用途挑的，不是凑数：

| 尺寸 | 用途 |
|------|------|
| 16 · 32 · 48 | favicon，浏览器标签页与书签栏 |
| 64 · 96 | GitHub 仓库列表、PR 与 issue 里的头像 |
| 128 · 180 | 桌面应用图标、iOS `apple-touch-icon` |
| 192 · 256 | PWA manifest、uTools 插件的 `logo.png` |
| 384 · 512 | GitHub 组织头像（要求 ≥ 500×500） |
| 1024 | 母版，用于再加工与印刷 |

小尺寸实测：16px 下 `ff` 的两道竖画与底部笑弧仍然分得开，角标收成一个圆点。
日常用矢量 SVG 即可，PNG 是给不吃 SVG 的地方准备的。

---

## 四、色板

每个组织一条 135° 的线性渐变，另配一个深色用于角标里的图形。

| 组织 | 渐变起 | 渐变止 | 角标深色 |
|------|--------|--------|----------|
| `farfarfun` | `#06B6D4` | `#7C3AED` | `#6D28D9` |
| `farfarfun-drive` | `#0EA5E9` | `#1D4ED8` | `#1D4ED8` |
| `farfarfun-skill` | `#8B5CF6` | `#6D28D9` | `#6D28D9` |
| `farfarfun-skills` | `#6366F1` | `#4338CA` | `#4338CA` |
| `farfarfun-utools` | `#14B8A6` | `#0F766E` | `#0F766E` |
| `farfarfun-action` | `#F97316` | `#C2410C` | `#C2410C` |

主组织横跨青到紫，子组织各占其中一段色相，排在一起是一条连续的光谱。

---

## 五、文件

```
brand/
├── gen_logos.py                  所有图形的唯一来源
├── svg/<格式>/<组织>.svg          矢量母版，1024×1024
├── png/<格式>/<组织>-<尺寸>.png
├── png/lockup{,-on-dark}/<组织>-<高>.png
└── favicon/<组织>.ico             多尺寸合一
```

重新生成：

```bash
uv run python brand/gen_logos.py
```

依赖 `cairosvg`（出 PNG）与 `pillow`（量组合标文字宽度、打包 `.ico`）。脚本每次会先清空
`svg/` `png/` `favicon/` 再整体重建，**不要往这三个目录里手工放文件**。要改图形就改
`gen_logos.py`：几何参数集中在「图形几何」一节，容器形态在 `FORMATS`，色板在 `ORGS`。

---

## 六、待办

- [ ] 六个组织的 GitHub 头像换成 `png/icon/<组织>-512.png`
- [ ] uTools 四个插件的 `utools/logo.png` 换成 `png/icon/utools-256.png`
- [ ] 各仓库 README 页眉换上横版组合标
- [ ] Web 项目接入 `favicon/<组织>.ico`
