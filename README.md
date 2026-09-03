# .github

farfarfun 组织的组织级元配置仓库：托管组织主页（`profile/README.md`，即
[github.com/farfarfun](https://github.com/farfarfun) 展示的内容）与批量维护组织下
仓库元信息（description / homepage / topics）的脚本。

## 安装

```bash
uv sync
```

## 最小可运行示例

预览会给哪些仓库的 description / homepage / topics 打上什么变更，不做任何写入：

```bash
uv run python script/update_keyword/update_repo_keywords.py --dry-run
```

确认无误后加 `--apply` 才会真正调用 GitHub API 写入。批量重建 `repo_config.json`
快照（按线上仓库状态）用：

```bash
bash script/update_repo_meta.sh
```

更多细节见 [script/update_keyword/REPO_UPDATER_README.md](script/update_keyword/REPO_UPDATER_README.md)。

## 关于 farfarfun

[farfarfun](https://github.com/farfarfun) 是一个专注于实用工具库的开源组织，
涵盖云存储、数据处理、AI、多媒体与开发工具链等方向。

- 🏠 组织主页：<https://github.com/farfarfun>
- 📦 PyPI：<https://pypi.org/user/niuliangtao/>
- 📧 联系：farfarfun@qq.com

本项目基于 [MIT](LICENSE) 协议开源。
