#!/usr/bin/env bash
# 更新 farfarfun 组织下仓库的 description / homepage / topics。
# 修复两类问题：
#   1. 近期活跃仓库缺少描述与 topics（funflix / funflix-web / nltcache / nltlog / utools-*）
#   2. nlt* 系列仓库的 homepage 仍指向重命名前的旧 PyPI 包（funbuild / funget / funfile / funsecret）
#
# 用法: bash script/update_repo_meta.sh
set -euo pipefail

ORG=farfarfun

meta() {
  local repo="$1" desc="$2" home="$3"
  gh api -X PATCH "repos/$ORG/$repo" -f description="$desc" -f homepage="$home" --silent
  echo "  meta  ✓ $repo"
}

topics() {
  local repo="$1"; shift
  local args=()
  for t in "$@"; do args+=(-f "names[]=$t"); done
  gh api -X PUT "repos/$ORG/$repo/topics" "${args[@]}" --silent
  echo "  topic ✓ $repo"
}

echo "== 近期活跃仓库：补齐描述与 topics =="

meta funflix \
  "影视资源分享文本的结构化采集、解析与网盘链接校验 - 采集/抽取/校验分层幂等，可单独重跑" \
  "https://pypi.org/project/funflix/"
topics funflix python farfarfun scraper telegram llm media pipeline sqlite

meta funflix-web \
  "funflix 的 Web 界面 - 单进程同时提供 Vue 3 前端与后端接口，含作品检索与流水线大盘" \
  "https://pypi.org/project/funflix-web/"
topics funflix-web vue3 fastapi python web-ui farfarfun funflix

meta nltcache \
  "轻量的 Python 函数缓存装饰器库 - 内存 / 磁盘 / Pickle 多种缓存策略，原生支持 async" \
  "https://pypi.org/project/nltcache/"
topics nltcache python cache decorator memoization lru-cache async farfarfun

meta nltlog \
  "基于 Loguru 的轻量日志库 - 按名称拆分日志文件，内置按日轮转、gzip 压缩与保留策略" \
  "https://pypi.org/project/nltlog/"
topics nltlog python logging loguru log-rotation farfarfun

meta utools-funchat \
  "uTools AI 聊天插件 - 多角色 AI 好友、内置角色市场、话题回溯与一键导出，本地优先" \
  ""
topics utools-funchat utools vue3 ai llm chatgpt plugin farfarfun

meta utools-funlink \
  "uTools 网址收藏与导航插件 - 分类与拖拽排序、废纸篓、站内搜索占位符、指定浏览器打开" \
  ""
topics utools-funlink utools vue3 bookmarks plugin productivity farfarfun

echo "== 描述与实际内容不符：修正 =="

# 原描述 "构建和部署工具包"，且 homepage 指向已改名的 funbuild
meta funbuild \
  "Python / 混合仓库的构建与发布工具 - 自动匹配 UV、Poetry、npm 等构建策略，串联版本递增、发布与 Git 标签" \
  "https://pypi.org/project/funbuild/"

# 原描述 "文档阅读和解析工具包"，实际是 Legado 书源管理
meta funread \
  "Legado（阅读 APP）书源与 RSS 源的管理工具库 - 支持书源解析、校验与批量处理" \
  "https://pypi.org/project/funread/"
topics funread legado bookstore rss python farfarfun

echo "== homepage 仍指向改名前的旧 PyPI 包：修正 =="

gh api -X PATCH "repos/$ORG/funget"    -f homepage="https://pypi.org/project/funget/"    --silent && echo "  home  ✓ funget    (funget → funget)"
gh api -X PATCH "repos/$ORG/funfile"   -f homepage="https://pypi.org/project/funfile/"   --silent && echo "  home  ✓ funfile   (funfile → funfile)"
gh api -X PATCH "repos/$ORG/funsecret" -f homepage="https://pypi.org/project/funsecret/" --silent && echo "  home  ✓ funsecret (funsecret → funsecret)"

echo "全部完成。"
