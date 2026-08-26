# GitHub 仓库关键词批量更新工具

这个工具用于批量更新 farfarfun 组织下所有仓库的关键词(topics)、描述和主页链接。

## 🚀 功能特性

- **批量更新**: 一次性更新多个仓库的元数据
- **配置驱动**: 通过JSON配置文件管理仓库信息
- **预览模式**: 支持dry-run模式，预览更改而不实际执行
- **单仓库更新**: 支持更新指定的单个仓库
- **完整日志**: 详细的操作日志和错误处理
- **API限制处理**: 自动处理GitHub API速率限制

## 📋 前置要求

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 设置GitHub Token

创建GitHub Personal Access Token并设置环境变量：

```bash
export GITHUB_TOKEN="your_github_token_here"
```

**Token权限要求**:
- `repo` - 完整的仓库访问权限
- `public_repo` - 公共仓库访问权限（如果只更新公共仓库）

### 3. 创建日志目录

```bash
mkdir -p logs
```

## 📝 配置文件

脚本使用 `repo_config.json` 文件来管理仓库配置。配置文件结构如下：

```json
{
  "organization": "farfarfun",
  "repositories": {
    "repo-name": {
      "description": "仓库描述",
      "keywords": ["keyword1", "keyword2", "keyword3"],
      "homepage": "https://example.com"
    }
  },
  "default_keywords": ["python", "farfarfun"],
  "settings": {
    "rate_limit_delay": 1,
    "max_retries": 3,
    "log_level": "INFO"
  }
}
```

### 配置说明

- `organization`: GitHub组织名称
- `repositories`: 仓库配置对象
  - `description`: 仓库描述文本
  - `keywords`: 关键词数组（会自动转换为小写并替换空格为连字符）
  - `homepage`: 仓库主页链接（可选）
- `default_keywords`: 默认关键词，会添加到所有仓库
- `settings`: 脚本设置
  - `rate_limit_delay`: API调用间隔（秒）
  - `max_retries`: 最大重试次数
  - `log_level`: 日志级别

## ⚠️ 先读这段

这套脚本会一次性改 140+ 个仓库的元信息，历史上出过两次事故，现在的默认行为都是针对它们收紧过的：

| 出过的问题 | 现在的行为 |
| --- | --- |
| `repo_config.json` 存的是批量生成的模板文案，跑一遍把手工写好的准确描述覆盖回错的 | 配置改为由 `build_repo_config.py` **从线上真实状态生成**。改完线上要重新生成，否则下次跑会覆盖回旧值 |
| `PUT /topics` 是整体替换，会抹掉线上手工加的 topics | **默认并集追加**，只有显式 `--replace-topics` 才整体替换 |
| 不加参数直接就写 GitHub | **默认只打印**将要做的改动，必须显式 `--apply` 才写入 |

### 重新生成配置基线

```bash
python build_repo_config.py     # 从 GitHub 线上状态重建 repo_config.json
```

## 🛠️ 使用方法

### 1. 看看会改什么（默认，不写入）

```bash
python update_repo_keywords.py
```

### 2. 确认无误后真正写入

```bash
python update_repo_keywords.py --apply
```

### 3. 只对比配置与线上现状

```bash
python update_repo_keywords.py --dry-run
```

### 4. 更新指定仓库

```bash
python update_repo_keywords.py --repo funutil --apply
```

### 5. 整体替换 topics（会抹掉线上手工加的，慎用）

```bash
python update_repo_keywords.py --replace-topics --apply
```

### 6. 指定组织

```bash
python update_repo_keywords.py --org your-org-name
```

## 📊 输出示例

### 正常执行输出

```
2024-01-15 10:30:15 - INFO - Found 9 repositories in farfarfun organization
2024-01-15 10:30:16 - INFO - Starting batch update for 9 repositories
2024-01-15 10:30:17 - INFO - Updating repository: fundrive
2024-01-15 10:30:18 - INFO - Successfully updated description for fundrive
2024-01-15 10:30:19 - INFO - Successfully updated topics for fundrive: ['python', 'cloud-storage', 'drive', 'storage', 'api', 'sdk', 'farfarfun']
2024-01-15 10:30:20 - INFO - Update completed: 9/9 repositories updated successfully

=== Update Results ===
fundrive: ✅ Success
fundata: ✅ Success
funsecret: ✅ Success
funbuild: ✅ Success
funcoin: ✅ Success
funread: ✅ Success
funget: ✅ Success
funutil: ✅ Success
funkeras: ✅ Success
```

### 预览模式输出

```
2024-01-15 10:25:10 - INFO - === DRY RUN MODE - No changes will be made ===

Repository: fundrive
  Description: 云存储驱动工具包 - 支持多种云存储服务的统一接口
  Homepage: https://pypi.org/project/fundrive/
  Keywords: ['python', 'cloud-storage', 'drive', 'storage', 'api', 'sdk', 'farfarfun']
  Current topics: ['python', 'storage']
```

## 📁 文件结构

```
.
├── update_repo_keywords.py    # 主脚本文件
├── repo_config.json          # 仓库配置文件
├── requirements.txt          # Python依赖
├── REPO_UPDATER_README.md    # 使用文档
└── logs/
    └── repo_update.log       # 操作日志
```

## 🔧 高级用法

### 自定义配置文件

```python
from script.update_keyword.update_repo_keywords import GitHubRepoUpdater

updater = GitHubRepoUpdater(
    org_name="your-org",
    config_file="custom_config.json"
)
updater.update_all_repos()
```

### 程序化使用

```python
from script.update_keyword.update_repo_keywords import GitHubRepoUpdater, RepoConfig

updater = GitHubRepoUpdater()

# 更新单个仓库
config = RepoConfig(
    name="test-repo",
    description="测试仓库",
    keywords=["python", "test"],
    homepage="https://example.com"
)

success = updater.update_single_repo("test-repo", config)
print(f"Update result: {success}")
```

## ⚠️ 注意事项

1. **API限制**: GitHub API有速率限制，脚本会自动处理并添加延迟
2. **权限要求**: 确保GitHub Token有足够的权限访问和修改仓库
3. **关键词格式**: GitHub topics必须是小写，脚本会自动转换
4. **备份**: 建议在大批量更新前先使用dry-run模式预览
5. **日志**: 所有操作都会记录到日志文件中，便于追踪和调试

## 🐛 故障排除

### 常见错误

1. **401 Unauthorized**: 检查GitHub Token是否正确设置
2. **403 Forbidden**: Token权限不足，需要repo权限
3. **404 Not Found**: 仓库不存在或无访问权限
4. **422 Unprocessable Entity**: 关键词格式不正确

### 调试技巧

1. 使用 `--dry-run` 模式预览更改
2. 检查 `logs/repo_update.log` 文件获取详细错误信息
3. 使用 `--repo` 参数测试单个仓库
4. 验证配置文件JSON格式是否正确

## 📞 支持

如有问题或建议，请联系：
- Email: farfarfun@qq.com
- GitHub: [@farfarfun](https://github.com/farfarfun)

## 📄 许可证

MIT License - 详见项目根目录的LICENSE文件。
