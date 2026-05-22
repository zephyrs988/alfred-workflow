# alfred-workflows

个人 Alfred 工作流集合。

## 工作流

| 目录 | 关键字 | 说明 | 安装 |
|------|--------|------|------|
| [alfred-timestamp](alfred-timestamp) | `time` | Unix 时间戳 ↔ 日期互转 | 双击 `Timestamp.alfredworkflow` |
| [alfred-youdao](alfred-youdao) | `yd` | 有道翻译（中↔英、其它→中） | 双击 `Youdao.alfredworkflow` |
| [alfred-uuid](alfred-uuid) | `uuid` | 生成 UUID v4 | 双击 `UUID.alfredworkflow` |

## 配置说明

- **时间戳 / UUID**：开箱即用
- **有道翻译**：需在有道智云申请 API，见 [alfred-youdao/README.md](alfred-youdao/README.md)。密钥请用环境变量或本地 `config.json`（已在 `.gitignore` 中忽略，不会提交）

## 目录结构

```
alfred-workflows/
├── alfred-timestamp/
├── alfred-youdao/
└── alfred-uuid/
```
