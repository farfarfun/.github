# farfarfun 品牌标识

六个组织和四个 uTools 插件共用一套标识。图形是 **`ff` 连字**——两个 f 共享一道横杠，
笔画在底部连成微笑弧：`ff` 取自 **far far**，底部的弧线是 **fun**。独立应用是例外，
见下面的[独立应用](#独立应用)一节。

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

### uTools 插件

同一套机制再往下一层：四个插件共用 `ff` 与角标位，角标换成各自的功能。

<table>
<tr>
<td align="center"><img src="png/icon/funchat-256.png" width="92"><br><code>funchat</code><br><sub>气泡 · AI 好友聊天</sub></td>
<td align="center"><img src="png/icon/fundoc-256.png" width="92"><br><code>fundoc</code><br><sub>文稿 · Markdown 文档</sub></td>
<td align="center"><img src="png/icon/funlink-256.png" width="92"><br><code>funlink</code><br><sub>书签 · 网址收藏</sub></td>
<td align="center"><img src="png/icon/funotp-256.png" width="92"><br><code>funotp</code><br><sub>盾 · 两步验证</sub></td>
</tr>
</table>

插件没有锁在 utools 组织那支青绿里——家族感由 `ff` 和角标机制保证，而插件是在 uTools
启动器里四个排一行被人扫一眼认出来的，色相拉开比凑成一家更要紧。`fundoc` 尤其不能再用
青绿：它和 utools 的头像会同时出现在 farfarfun-utools 的 README 里。

### 独立应用

上面那条「家族感由 `ff` 和角标机制保证」对组织和插件成立，对独立应用不成立——这里是
唯一可以整个换掉主图形的地方。

<table>
<tr>
<td align="center"><img src="png/icon/funclash-256.png" width="92"><br><code>funclash</code><br><sub>闸口 · 代理客户端</sub></td>
</tr>
</table>

FunClash 装在别人的 Dock、托盘和手机桌面上，跟一堆来历不同的应用挤在一起，不是
farfarfun 工具链里的一环。`ff` 是给「这是 farfarfun 做的东西」用的记号，对一个有自己
用户群的产品来说那不是它要说的第一句话。所以它换一个图形：**闸口**——两条竖腿架一道
平顶、脚向外撇，流量从一侧进、穿过闸口、从另一侧出，代理就是这么一件事。

换掉主图形的同时角标也是 `None`：角标存在的意义是在同一个 `ff` 上区分产品线，图形都
换了就没有要区分的东西了。

它跟家族共享的是**容器（圆角方 / 圆 / 反白 / 无底）、135° 渐变和尺寸矩阵**，四种格式
和组合标一个不少，排在家族里尺寸和墨色重量也是对着 `ff` 调的。洋红→紫罗兰避开了上面
所有组织和插件的色相段。

**新主体默认还是走 `ff`。**`Subject.mark` 的默认值就是 `ff_mark`，不传就是家族样式；
要换图形得有 funclash 这样的理由——独立分发、自己的用户群、不靠 farfarfun 的名字被认出来。

---

## 一、四种格式

四种容器，按场景取用。每组最后一枚是 funclash——它换掉了主图形，容器一样照用。

### icon —— 主图标

渐变圆角方。**组织头像、应用图标、favicon 都用它。**

<p>
<img src="png/icon/farfarfun-128.png" width="84">
<img src="png/icon/drive-128.png" width="84">
<img src="png/icon/skill-128.png" width="84">
<img src="png/icon/skills-128.png" width="84">
<img src="png/icon/utools-128.png" width="84">
<img src="png/icon/action-128.png" width="84">
<img src="png/icon/funclash-128.png" width="84">
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
<img src="png/icon-inverse/funclash-128.png" width="84">
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
<img src="png/icon-circle/funclash-128.png" width="84">
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
<img src="png/mark/funclash-128.png" width="84">
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
| <img src="png/lockup/funchat-160.png" width="250"> | <img src="png/lockup-on-dark/funchat-160.png" width="250"> |
| <img src="png/lockup/fundoc-160.png" width="250"> | <img src="png/lockup-on-dark/fundoc-160.png" width="250"> |
| <img src="png/lockup/funlink-160.png" width="250"> | <img src="png/lockup-on-dark/funlink-160.png" width="250"> |
| <img src="png/lockup/funotp-160.png" width="250"> | <img src="png/lockup-on-dark/funotp-160.png" width="250"> |
| <img src="png/lockup/funclash-160.png" width="250"> | <img src="png/lockup-on-dark/funclash-160.png" width="250"> |

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

小尺寸实测：16px 下 `ff` 的两道竖画与底部笑弧仍然分得开，角标收成一个圆点；
funclash 的闸口是竖笔画，正好落在像素格上，16px 下腿和平顶都不糊——它要去的
favicon、系统托盘和 Android 通知栏全在那个尺寸上。
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

插件另起一组，四个色相互相拉到最开：

| 插件 | 渐变起 | 渐变止 | 角标深色 |
|------|--------|--------|----------|
| `funchat` | `#06B6D4` | `#0E7490` | `#0E7490` |
| `fundoc` | `#4F46E5` | `#3730A3` | `#3730A3` |
| `funlink` | `#22C55E` | `#15803D` | `#15803D` |
| `funotp` | `#F43F5E` | `#BE123C` | `#BE123C` |

独立应用再另起一组，避开上面所有人的色相段：

| 应用 | 渐变起 | 渐变止 | 深色 |
|------|--------|--------|------|
| `funclash` | `#D946EF` | `#7E22CE` | `#7E22CE` |

funclash 没有角标，那列的深色改用在别处——它是品牌的单色值，Android 快捷方式底色、
PWA `theme_color` 这类只收一个纯色的地方用它。

---

## 五、文件

文件名里的 `<主体>` 是六个组织之一（`farfarfun` `drive` `skill` `skills` `utools`
`action`）、四个插件之一（`funchat` `fundoc` `funlink` `funotp`），或独立应用
`funclash`，共十一个，每个都出齐下面所有格式与尺寸。

```
brand/
├── gen_logos.py                  所有图形的唯一来源
├── svg/<格式>/<主体>.svg          矢量母版，1024×1024
├── png/<格式>/<主体>-<尺寸>.png
├── png/lockup{,-on-dark}/<主体>-<高>.png
└── favicon/<主体>.ico             多尺寸合一
```

重新生成：

```bash
uv run python brand/gen_logos.py
```

依赖 `cairosvg`（出 PNG）与 `pillow`（量组合标文字宽度、打包 `.ico`）。脚本每次会先清空
`svg/` `png/` `favicon/` 再整体重建，**不要往这三个目录里手工放文件**。要改图形就改
`gen_logos.py`：主图形（`ff` 连字和 funclash 的闸口）在「主图形」一节，容器与角标
几何在「角标与容器」，容器形态在 `FORMATS`，色板在 `ORGS` / `PLUGINS` / `APPS`，
角标图形在 `glyph()`。

---

## 六、落地情况

- [x] uTools 四个插件各出一枚自己的图标，`utools/logo.png` 已换
      （funchat 另有一份 `public/logo.png`）
- [x] funotp 的内联 SVG favicon 换成 `ff` 图形
- [x] farfarfun 与 farfarfun-drive 的组织主页加上横版组合标
- [x] 四个插件 README 加上图标页眉
- [ ] **六个组织的 GitHub 头像**——只能手工传，REST API 没有组织头像的端点
      （`PATCH /orgs/{org}` 的参数里没有任何 avatar 字段）。到
      `https://github.com/organizations/<组织>/settings/profile` 上传对应的
      `png/icon/<主体>-512.png`。
- [ ] 其余四个子组织（skill / skills / utools / action）的 profile 仓库本地没有，
      建好之后再套组合标页眉
- [ ] 真正的 Web 项目接入 `favicon/<主体>.ico`（插件走的是内联 SVG 和 logo.png，
      用不上 ico）
- [ ] **funclash 把闸口铺到各平台产物上**——桌面、托盘、Android 启动器、favicon
      的栅格图都在 `farfarfun/funclash` 仓库里，矢量源从这里的 `svg/` 取过去
      vendored 一份。另外 maskable 的 PWA 图标这边没有对应格式（现有四种容器
      都带透明角，当 maskable 用会被裁），funclash 那边自己出满版的一版
