# CHANGELOG

## 未发布

### 修复

- 移除 `pyproject.toml` 中与仓库名 `.github` 不一致、从未发布过的 hatchling 构建
  配置；保留 `[tool.uv] package = false`，明确本仓库只用 uv 管理脚本依赖。
- 用 `build_repo_config.py` 按线上 GitHub 状态重新生成 `repo_config.json`
  快照，修正 `fundb` 已改名为 `fardb` 等过期条目。
- 修掉 `tests/` 中新增的 ruff 回归（可变类属性默认值、嵌套 `with` 语句）。
- （此前已落地）`update_repo_keywords.py` 的 `dry_run` 属性与方法同名遮蔽、未知
  仓库更新退出码为 0、`DEFAULT_CONFIG_FILE` 相对路径在非脚本目录下解析失败等问题。

## 0.1.0 - 2026-09-03

### 新增

- 补充仓库根目录 `README.md`、`LICENSE`（MIT）、`pyproject.toml` + `uv.lock`、本
  CHANGELOG，补齐组织规范要求的基础文件。

### 变更

- `script/update_keyword/update_repo_keywords.py` 日志改用 `farlog`（原来误用
  `funutil`），类型注解改为 Python 3.10 内置泛型（`dict`/`list`/`X | None`）。
- 依赖管理从 `requirements.txt` 迁移到 `pyproject.toml` + `uv`。

### 修复

- `load_config` 不再吞掉配置文件读取/解析异常静默返回空字典，改为记录日志后抛出，
  避免配置损坏时脚本"看起来跑成功了"但实际什么都没做。
