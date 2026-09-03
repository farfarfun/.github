# CHANGELOG

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
