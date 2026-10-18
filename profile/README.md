<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)"
            srcset="https://raw.githubusercontent.com/farfarfun/.github/master/brand/svg/lockup-on-dark/farfarfun.svg">
    <img src="https://raw.githubusercontent.com/farfarfun/.github/master/brand/svg/lockup/farfarfun.svg"
         height="80" alt="farfarfun">
  </picture>
</p>

## 🚀 关于 farfarfun

我们是一个专注于开发实用 Python 工具包的开源组织，致力于为 Python 开发者提供高质量、易用的工具库。

### 🎯 我们的使命
- **🔧 简化开发** - 提供开箱即用的工具包
- **🌟 提升效率** - 让开发者专注于核心业务逻辑
- **🤝 开源共享** - 构建活跃的开源社区
- **📈 持续创新** - 跟上技术发展趋势

### 📊 项目概览
- 🏗️ **139 个公开仓库** - 涵盖工具链、数据、AI、多媒体等领域
- 📦 **20+ 活跃 PyPI 包** - 持续维护并发布到 Python 包索引
- 🌟 **100+ GitHub Stars** - 获得社区认可
- 🧰 **两条产品线** - `far*` 基础工具链 + `fun*` 领域应用库

---

## 🗂️ 组织矩阵

本组织是 farfarfun 的主组织，新项目默认在此孵化；当某一方向的仓库数量与功能完整度达到一定规模后，即从本组织毕业、独立为子组织。`farfarfun-drive` 与 `farfarfun-utools` 均由此路径独立，原 `farfarfun/<repo>` 链接继续重定向。规划阶段已确定为独立产品线的，则直接建立子组织，`farfarfun-skill` 与 `farfarfun-skills` 属于此类。因此下表并非预先划定的固定分类，会随产品线演进持续调整。

| 组织 | 产物 | 定位 | 仓库数 |
|------|------|------|--------|
| **[farfarfun](https://github.com/farfarfun)**（本组织） | Python 包 | 新项目孵化地，以及 `far*` 基础工具链与 `fun*` 领域应用库，发布至 PyPI | 139 |
| [farfarfun-drive](https://github.com/farfarfun-drive) | 网盘 / 云存储 | `fundrive` 统一接口框架、各网盘驱动，以及蓝奏云 SDK 与客户端 | 11 |
| [farfarfun-skill](https://github.com/farfarfun-skill) | AI Agent Skill | **自研** Skill 的源头仓库，覆盖项目治理、服务规范与多语言开发规范 | 7 |
| [farfarfun-skills](https://github.com/farfarfun-skills) | Skill 镜像 | 社区 Skill 与上述自研 Skill 的聚合镜像，每小时与上游同步并镜像至 Gitee | 26 |
| [farfarfun-utools](https://github.com/farfarfun-utools) | uTools 插件 | 自研 uTools 插件，覆盖 AI 聊天、网址导航与两步验证码 | 5 |

> **如何定位所需仓库**：通用 Python 工具见本组织；网盘与云存储见 `farfarfun-drive`；提交 Skill 的 issue 或 PR 见 `farfarfun-skill`（镜像组织不接受 PR）；批量安装 Skill（含社区项目）见 `farfarfun-skills`；uTools 插件见 `farfarfun-utools`。
>
> 未在上述组织中找到的项目，通常仍在本组织孵化，可直接按仓库名检索。

---

## 🆕 近期在做

| 项目 | 用途 | 链接 |
|------|------|------|
| [funflix](https://github.com/farfarfun/funflix) | 影视资源分享文本的结构化采集、解析与网盘链接校验，采集 / 抽取 / 校验分层幂等 | [![PyPI](https://img.shields.io/pypi/v/funflix?style=flat-square)](https://pypi.org/project/funflix/) |
| [funflix-web](https://github.com/farfarfun/funflix-web) | funflix 的 Web 界面，单进程同时提供 Vue 3 前端与后端接口 | [![PyPI](https://img.shields.io/pypi/v/funflix-web?style=flat-square)](https://pypi.org/project/funflix-web/) |
| [utools-funchat](https://github.com/farfarfun-utools/utools-funchat) | uTools AI 聊天插件，多角色 AI 好友、角色市场、话题回溯，本地优先 | ![Vue](https://img.shields.io/badge/Vue-3-42b883?style=flat-square) |
| [utools-funotp](https://github.com/farfarfun-utools/utools-funotp) | uTools 两步验证码插件，本地管理 TOTP 账号，离线生成动态码 | ![Vue](https://img.shields.io/badge/Vue-3-42b883?style=flat-square) |
| [farcache](https://github.com/farfarfun/farcache) | 轻量函数缓存装饰器库，内存 / 磁盘 / Pickle 多种策略，原生支持 async | [![PyPI](https://img.shields.io/pypi/v/farcache?style=flat-square)](https://pypi.org/project/farcache/) |
| [funread](https://github.com/farfarfun/funread) | Legado（阅读 APP）书源与 RSS 源的管理、解析与校验 | [![PyPI](https://img.shields.io/pypi/v/funread?style=flat-square)](https://pypi.org/project/funread/) |

---

## 🧱 far\* — 基础工具链

面向工程基建的一组小而专的库，互相解耦、可单独使用。

| 项目 | 用途 | PyPI |
|------|------|------|
| [funbuild](https://github.com/farfarfun/funbuild) | 构建与发布：自动匹配 UV / Poetry / npm 策略，串联版本递增、发布与打标签 | [![PyPI](https://img.shields.io/pypi/v/funbuild?style=flat-square)](https://pypi.org/project/funbuild/) |
| [farcache](https://github.com/farfarfun/farcache) | 函数缓存装饰器：内存、磁盘与 Pickle 缓存 | [![PyPI](https://img.shields.io/pypi/v/farcache?style=flat-square)](https://pypi.org/project/farcache/) |
| [funget](https://github.com/farfarfun/funget) | HTTP 文件传输：并发、断点续传与命令行 | [![PyPI](https://img.shields.io/pypi/v/funget?style=flat-square)](https://pypi.org/project/funget/) |
| [funfile](https://github.com/farfarfun/funfile) | 文件、归档与序列化实用工具 | [![PyPI](https://img.shields.io/pypi/v/funfile?style=flat-square)](https://pypi.org/project/funfile/) |
| [funsecret](https://github.com/farfarfun/funsecret) | 本地密钥管理与可选的 MySQL 同步 | [![PyPI](https://img.shields.io/pypi/v/funsecret?style=flat-square)](https://pypi.org/project/funsecret/) |
| [farlog](https://github.com/farfarfun/farlog) | 基于 Loguru 的日志库：按名称拆分文件，按日轮转与压缩 | [![PyPI](https://img.shields.io/pypi/v/farlog?style=flat-square)](https://pypi.org/project/farlog/) |
| [fundeploy](https://github.com/farfarfun/fundeploy) | 本机开发与服务管理的 Bash 脚本集：统一 `fundeploy` 命令入口，一键安装开发环境、部署常驻服务与 AI 工具 | - |

---

## 📈 核心项目统计

|    | title                                               | stars                                                                                                               | forks                                                                                                               | watchers                                                                                                                  | download                                                                                                                                                                                                | version                                                    | format                                                         | pypi                                                                                                                  |
|---:|:----------------------------------------------------|:--------------------------------------------------------------------------------------------------------------------|:--------------------------------------------------------------------------------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:-----------------------------------------------------------|:---------------------------------------------------------------|:----------------------------------------------------------------------------------------------------------------------|
|  0 | [fundrive](https://github.com/farfarfun-drive/fundrive)   | <img alt="Stars" src="https://img.shields.io/github/stars/farfarfun-drive/fundrive?style=flat-square&labelColor=black"/>  | <img alt="Forks" src="https://img.shields.io/github/forks/farfarfun-drive/fundrive?style=flat-square&labelColor=black"/>  | <img alt="Watchers" src="https://img.shields.io/github/watchers/farfarfun-drive/fundrive?style=flat-square&labelColor=black"/>  | [![fundrive](https://static.pepy.tech/personalized-badge/fundrive?period=total&units=international_system&left_color=black&right_color=red&left_text=Downloads)](https://pepy.tech/project/fundrive)    | ![PyPI - Version](https://img.shields.io/pypi/v/fundrive)  | ![PyPI - Format](https://img.shields.io/pypi/format/fundrive)  | [![PyPi](https://img.shields.io/badge/PyPi-black?style=flat-square&logo=pypi)](https://pypi.org/project/fundrive)  |
|  1 | [funrec](https://github.com/farfarfun/funrec)       | <img alt="Stars" src="https://img.shields.io/github/stars/farfarfun/funrec?style=flat-square&labelColor=black"/>    | <img alt="Forks" src="https://img.shields.io/github/forks/farfarfun/funrec?style=flat-square&labelColor=black"/>    | <img alt="Watchers" src="https://img.shields.io/github/watchers/farfarfun/funrec?style=flat-square&labelColor=black"/>    | [![funrec](https://static.pepy.tech/personalized-badge/funrec?period=total&units=international_system&left_color=black&right_color=red&left_text=Downloads)](https://pepy.tech/project/funrec)          | ![PyPI - Version](https://img.shields.io/pypi/v/funrec)    | ![PyPI - Format](https://img.shields.io/pypi/format/funrec)    | [![PyPi](https://img.shields.io/badge/PyPi-black?style=flat-square&logo=pypi)](https://pypi.org/project/funrec)    |
|  2 | [fundata](https://github.com/farfarfun/fundata)     | <img alt="Stars" src="https://img.shields.io/github/stars/farfarfun/fundata?style=flat-square&labelColor=black"/>   | <img alt="Forks" src="https://img.shields.io/github/forks/farfarfun/fundata?style=flat-square&labelColor=black"/>   | <img alt="Watchers" src="https://img.shields.io/github/watchers/farfarfun/fundata?style=flat-square&labelColor=black"/>   | [![fundata](https://static.pepy.tech/personalized-badge/fundata?period=total&units=international_system&left_color=black&right_color=red&left_text=Downloads)](https://pepy.tech/project/fundata)       | ![PyPI - Version](https://img.shields.io/pypi/v/fundata)   | ![PyPI - Format](https://img.shields.io/pypi/format/fundata)   | [![PyPi](https://img.shields.io/badge/PyPi-black?style=flat-square&logo=pypi)](https://pypi.org/project/fundata)   |
|  3 | [funbuild](https://github.com/farfarfun/funbuild)   | <img alt="Stars" src="https://img.shields.io/github/stars/farfarfun/funbuild?style=flat-square&labelColor=black"/>  | <img alt="Forks" src="https://img.shields.io/github/forks/farfarfun/funbuild?style=flat-square&labelColor=black"/>  | <img alt="Watchers" src="https://img.shields.io/github/watchers/farfarfun/funbuild?style=flat-square&labelColor=black"/>  | [![funbuild](https://static.pepy.tech/personalized-badge/funbuild?period=total&units=international_system&left_color=black&right_color=red&left_text=Downloads)](https://pepy.tech/project/funbuild)    | ![PyPI - Version](https://img.shields.io/pypi/v/funbuild)  | ![PyPI - Format](https://img.shields.io/pypi/format/funbuild)  | [![PyPi](https://img.shields.io/badge/PyPi-black?style=flat-square&logo=pypi)](https://pypi.org/project/funbuild)  |
|  4 | [funcoin](https://github.com/farfarfun/funcoin)     | <img alt="Stars" src="https://img.shields.io/github/stars/farfarfun/funcoin?style=flat-square&labelColor=black"/>   | <img alt="Forks" src="https://img.shields.io/github/forks/farfarfun/funcoin?style=flat-square&labelColor=black"/>   | <img alt="Watchers" src="https://img.shields.io/github/watchers/farfarfun/funcoin?style=flat-square&labelColor=black"/>   | [![funcoin](https://static.pepy.tech/personalized-badge/funcoin?period=total&units=international_system&left_color=black&right_color=red&left_text=Downloads)](https://pepy.tech/project/funcoin)       | ![PyPI - Version](https://img.shields.io/pypi/v/funcoin)   | ![PyPI - Format](https://img.shields.io/pypi/format/funcoin)   | [![PyPi](https://img.shields.io/badge/PyPi-black?style=flat-square&logo=pypi)](https://pypi.org/project/funcoin)   |
|  5 | [funread](https://github.com/farfarfun/funread)     | <img alt="Stars" src="https://img.shields.io/github/stars/farfarfun/funread?style=flat-square&labelColor=black"/>   | <img alt="Forks" src="https://img.shields.io/github/forks/farfarfun/funread?style=flat-square&labelColor=black"/>   | <img alt="Watchers" src="https://img.shields.io/github/watchers/farfarfun/funread?style=flat-square&labelColor=black"/>   | [![funread](https://static.pepy.tech/personalized-badge/funread?period=total&units=international_system&left_color=black&right_color=red&left_text=Downloads)](https://pepy.tech/project/funread)       | ![PyPI - Version](https://img.shields.io/pypi/v/funread)   | ![PyPI - Format](https://img.shields.io/pypi/format/funread)   | [![PyPi](https://img.shields.io/badge/PyPi-black?style=flat-square&logo=pypi)](https://pypi.org/project/funread)   |
|  6 | [funget](https://github.com/farfarfun/funget)       | <img alt="Stars" src="https://img.shields.io/github/stars/farfarfun/funget?style=flat-square&labelColor=black"/>    | <img alt="Forks" src="https://img.shields.io/github/forks/farfarfun/funget?style=flat-square&labelColor=black"/>    | <img alt="Watchers" src="https://img.shields.io/github/watchers/farfarfun/funget?style=flat-square&labelColor=black"/>    | [![funget](https://static.pepy.tech/personalized-badge/funget?period=total&units=international_system&left_color=black&right_color=red&left_text=Downloads)](https://pepy.tech/project/funget)          | ![PyPI - Version](https://img.shields.io/pypi/v/funget)    | ![PyPI - Format](https://img.shields.io/pypi/format/funget)    | [![PyPi](https://img.shields.io/badge/PyPi-black?style=flat-square&logo=pypi)](https://pypi.org/project/funget)    |
|  7 | [funutil](https://github.com/farfarfun/funutil)     | <img alt="Stars" src="https://img.shields.io/github/stars/farfarfun/funutil?style=flat-square&labelColor=black"/>   | <img alt="Forks" src="https://img.shields.io/github/forks/farfarfun/funutil?style=flat-square&labelColor=black"/>   | <img alt="Watchers" src="https://img.shields.io/github/watchers/farfarfun/funutil?style=flat-square&labelColor=black"/>   | [![funutil](https://static.pepy.tech/personalized-badge/funutil?period=total&units=international_system&left_color=black&right_color=red&left_text=Downloads)](https://pepy.tech/project/funutil)       | ![PyPI - Version](https://img.shields.io/pypi/v/funutil)   | ![PyPI - Format](https://img.shields.io/pypi/format/funutil)   | [![PyPi](https://img.shields.io/badge/PyPi-black?style=flat-square&logo=pypi)](https://pypi.org/project/funutil)   |
|  8 | [funtable](https://github.com/farfarfun/funtable)   | <img alt="Stars" src="https://img.shields.io/github/stars/farfarfun/funtable?style=flat-square&labelColor=black"/>  | <img alt="Forks" src="https://img.shields.io/github/forks/farfarfun/funtable?style=flat-square&labelColor=black"/>  | <img alt="Watchers" src="https://img.shields.io/github/watchers/farfarfun/funtable?style=flat-square&labelColor=black"/>  | [![funtable](https://static.pepy.tech/personalized-badge/funtable?period=total&units=international_system&left_color=black&right_color=red&left_text=Downloads)](https://pepy.tech/project/funtable)    | ![PyPI - Version](https://img.shields.io/pypi/v/funtable)  | ![PyPI - Format](https://img.shields.io/pypi/format/funtable)  | [![PyPi](https://img.shields.io/badge/PyPi-black?style=flat-square&logo=pypi)](https://pypi.org/project/funtable)  |
|  9 | [funimage](https://github.com/farfarfun/funimage)   | <img alt="Stars" src="https://img.shields.io/github/stars/farfarfun/funimage?style=flat-square&labelColor=black"/>  | <img alt="Forks" src="https://img.shields.io/github/forks/farfarfun/funimage?style=flat-square&labelColor=black"/>  | <img alt="Watchers" src="https://img.shields.io/github/watchers/farfarfun/funimage?style=flat-square&labelColor=black"/>  | [![funimage](https://static.pepy.tech/personalized-badge/funimage?period=total&units=international_system&left_color=black&right_color=red&left_text=Downloads)](https://pepy.tech/project/funimage)    | ![PyPI - Version](https://img.shields.io/pypi/v/funimage)  | ![PyPI - Format](https://img.shields.io/pypi/format/funimage)  | [![PyPi](https://img.shields.io/badge/PyPi-black?style=flat-square&logo=pypi)](https://pypi.org/project/funimage)  |
| 10 | [funserver](https://github.com/farfarfun/funserver) | <img alt="Stars" src="https://img.shields.io/github/stars/farfarfun/funserver?style=flat-square&labelColor=black"/> | <img alt="Forks" src="https://img.shields.io/github/forks/farfarfun/funserver?style=flat-square&labelColor=black"/> | <img alt="Watchers" src="https://img.shields.io/github/watchers/farfarfun/funserver?style=flat-square&labelColor=black"/> | [![funserver](https://static.pepy.tech/personalized-badge/funserver?period=total&units=international_system&left_color=black&right_color=red&left_text=Downloads)](https://pepy.tech/project/funserver) | ![PyPI - Version](https://img.shields.io/pypi/v/funserver) | ![PyPI - Format](https://img.shields.io/pypi/format/funserver) | [![PyPi](https://img.shields.io/badge/PyPi-black?style=flat-square&logo=pypi)](https://pypi.org/project/funserver) |
| 11 | [funpush](https://github.com/farfarfun/funpush)     | <img alt="Stars" src="https://img.shields.io/github/stars/farfarfun/funpush?style=flat-square&labelColor=black"/>   | <img alt="Forks" src="https://img.shields.io/github/forks/farfarfun/funpush?style=flat-square&labelColor=black"/>   | <img alt="Watchers" src="https://img.shields.io/github/watchers/farfarfun/funpush?style=flat-square&labelColor=black"/>   | [![funpush](https://static.pepy.tech/personalized-badge/funpush?period=total&units=international_system&left_color=black&right_color=red&left_text=Downloads)](https://pepy.tech/project/funpush)       | ![PyPI - Version](https://img.shields.io/pypi/v/funpush)   | ![PyPI - Format](https://img.shields.io/pypi/format/funpush)   | [![PyPi](https://img.shields.io/badge/PyPi-black?style=flat-square&logo=pypi)](https://pypi.org/project/funpush)   |

---

## 🌟 更多精彩项目

上表仅列出核心项目，其余工具包按领域分类如下：

### ☁️ 存储与数据
- **[funtable](https://github.com/farfarfun/funtable)** - SQLite / TinyDB / SQLModel 的统一表存储抽象
- **[fardb](https://github.com/farfarfun/fardb)** - 多种数据库的统一操作接口
- **[fundataworks](https://github.com/farfarfun/fundataworks)** - 数据处理工作流与管道
- **[funseries](https://github.com/farfarfun/funseries)** - 时间序列数据处理与分析
- **[funstock](https://github.com/farfarfun/funstock)** - 股票数据获取、分析与处理

### 🤖 AI & 机器学习
- **[funrec](https://github.com/farfarfun/funrec)** - 推荐系统算法与开发工具
- **[funai](https://github.com/farfarfun/funai)** - AI 模型集成与机器学习工具
- **[funkeras](https://github.com/farfarfun/funkeras)** - Keras 深度学习增强功能与实用工具
- **[funmodel](https://github.com/farfarfun/funmodel)** - 机器学习模型训练、部署与管理
- **[fartts](https://github.com/farfarfun/fartts)** - 语音合成工具包
- **[funpaper](https://github.com/farfarfun/funpaper)** - 学术论文检索、下载与管理

### 🎨 多媒体处理
- **[funimage](https://github.com/farfarfun/funimage)** - 图像格式转换与处理
- **[funvideo](https://github.com/farfarfun/funvideo)** - 视频编辑、转换与处理
- **[funmedia](https://github.com/farfarfun/funmedia)** - 音视频与图像的综合处理
- **[funvtk](https://github.com/farfarfun/funvtk)** - VTK 3D 与科学计算可视化

### 🌐 网络与服务
- **[funserver](https://github.com/farfarfun/funserver)** - 跨平台服务器应用管理框架
- **[funapi](https://github.com/farfarfun/funapi)** - API 开发、测试与管理
- **[funfake](https://github.com/farfarfun/funfake)** - 真实 HTTP 请求头生成
- **[funproxy](https://github.com/farfarfun/funproxy)** - 代理池的管理与使用
- **[funpush](https://github.com/farfarfun/funpush)** - 钉钉、微信等多平台机器人消息推送

### 🔐 安全与加密
- **[funsecret](https://github.com/farfarfun/funsecret)** - 本地密钥管理与可选的 MySQL 同步
- **[funtool](https://github.com/farfarfun/funtool)** - 加密、解密等安全相关工具函数

### 💼 企业应用
- **[funwork](https://github.com/farfarfun/funwork)** - 任务调度与工作流程管理
- **[funnotice](https://github.com/farfarfun/funnotice)** - 多种通知方式的统一接口
- **[funuser](https://github.com/farfarfun/funuser)** - 用户认证、授权与管理
- **[funapp](https://github.com/farfarfun/funapp)** - 快速构建 Python 应用的框架

### 🛠️ 开发与运维
- **[funutil](https://github.com/farfarfun/funutil)** - 常用工具函数与实用程序
- **[funshell](https://github.com/farfarfun/funshell)** - Shell 流程封装
- **[funinstall](https://github.com/farfarfun/funinstall)** - 开发工具一键安装
- **[fartask](https://github.com/farfarfun/fartask)** - 任务创建、跟踪与管理

---

## 🔭 其他组织的产物

本组织以通用 Python 工具为主，以下产品线分属各子组织（`fundrive` 系列与 uTools 插件已由本组织迁出，原 `farfarfun/<repo>` 链接继续重定向）：

### ☁️ 网盘 / 云存储 → [farfarfun-drive](https://github.com/farfarfun-drive)
- **[fundrive](https://github.com/farfarfun-drive/fundrive)** - 统一的网盘 / 云存储操作接口框架，一套 API 打通 20+ 服务
- **[fundrive-alipan](https://github.com/farfarfun-drive/fundrive-alipan)** / **[-baidu](https://github.com/farfarfun-drive/fundrive-baidu)** / **[-lanzou](https://github.com/farfarfun-drive/fundrive-lanzou)** / **[-quark](https://github.com/farfarfun-drive/fundrive-quark)** - 阿里云盘 / 百度网盘 / 蓝奏云 / 夸克网盘驱动
- **[funlanzou](https://github.com/farfarfun-drive/funlanzou)** - 蓝奏云 Python SDK 与 PyQt6 桌面客户端

```bash
pip install fundrive fundrive-alipan fundrive-quark   # 主框架与按需安装的驱动
```

### 🧩 uTools 插件 → [farfarfun-utools](https://github.com/farfarfun-utools)
- **[utools-funchat](https://github.com/farfarfun-utools/utools-funchat)** - 多角色 AI 聊天，内置角色市场、话题回溯
- **[utools-funlink](https://github.com/farfarfun-utools/utools-funlink)** - 网址收藏与导航，分类拖拽排序、废纸篓
- **[utools-funotp](https://github.com/farfarfun-utools/utools-funotp)** - 两步验证码，离线生成 TOTP 动态码

### 🤖 AI Agent Skill → [farfarfun-skill](https://github.com/farfarfun-skill)（自研源头）
- **[project-manager](https://github.com/farfarfun-skill/project-manager)** - 项目全生命周期治理门禁
- **[service-governance](https://github.com/farfarfun-skill/service-governance)** - 服务发布、Bash 生命周期、子模块编排
- **[lang-spec-hub](https://github.com/farfarfun-skill/lang-spec-hub)** - Python / Java 开发规范
- **[paperclip-governance](https://github.com/farfarfun-skill/paperclip-governance)** - Paperclip 平台执行隔离与任务协调
- **[skill-router](https://github.com/farfarfun-skill/skill-router)** - 全组织 Skill 路由表，用于选择适用的 Skill

### 📦 Skill 聚合镜像 → [farfarfun-skills](https://github.com/farfarfun-skills)
聚合 20 个社区 Skill 仓库与上述 4 个自研仓库的镜像，每小时与上游同步，并整体镜像至 Gitee。本地批量安装可使用
[`fundeploy tool skills-sync`](https://github.com/farfarfun/fundeploy)。

## 🚀 快速开始

```bash
# 安装任意工具包
pip install <package-name>

# 例如安装近期维护的工具包
pip install fundrive funtable funget farcache
```

## 📞 联系我们

- 📧 **Email**: farfarfun@qq.com
- 🐙 **GitHub**: [@farfarfun](https://github.com/farfarfun)
- 📦 **PyPI**: [niuliangtao](https://pypi.org/user/niuliangtao/)

---


<div align="center">

**🎯 活到老，学到老，玩到老，老牛老牛了 🎯**

**让编程更简单，让开发更高效！**

<br/>
<a href="https://github.com/farfarfun">
    <img src="https://img.shields.io/badge/Website-farfarfun-red?style=flat-square">
</a>

<a href="mailto:farfarfun@qq.com">
    <img src="https://img.shields.io/badge/Email-farfarfun@qq.com-red?style=flat-square&logo=gmail&logoColor=white">
</a>

<a href="https://pypi.org/user/niuliangtao/">
    <img src="https://img.shields.io/badge/PyPi-niuliangtao-blue?style=flat-square&logo=pypi&logoColor=white">
</a>
<br/>


[![Visitors](https://api.visitorbadge.io/api/visitors?path=https%3A%2F%2Fgithub.com%2Ffarfarfun&label=Profile%20Views&countColor=%23263759&style=flat)](https://visitorbadge.io/status?path=https%3A%2F%2Fgithub.com%2Ffarfarfun)

</div>
