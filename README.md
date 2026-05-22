# alfred-workflow

个人 Alfred 工作流集合。

## 工作流

| 目录 | 关键字 | 说明 | 安装 |
|------|--------|------|------|
| [workflows/alfred-timestamp](workflows/alfred-timestamp) | `time` | Unix 时间戳 ↔ 日期互转 | 双击 `Timestamp.alfredworkflow` |
| [workflows/alfred-youdao](workflows/alfred-youdao) | `yd` | 有道翻译（中↔英、其它→中） | 双击 `Youdao.alfredworkflow` |

## 配置说明

- **时间戳**：开箱即用
- **有道翻译**：需在有道智云申请 API，见 [workflows/alfred-youdao/README.md](workflows/alfred-youdao/README.md)。密钥请用环境变量或本地 `config.json`（已在 `.gitignore` 中忽略，不会提交）

## 目录结构

```
workflows/
├── alfred-timestamp/
└── alfred-youdao/
```
