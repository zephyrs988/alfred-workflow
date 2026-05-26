# Alfred Timestamp Workflow

在 Alfred 中输入 `time` 关键字，进行 Unix 时间戳与日期时间互转。

## 用法

| 输入 | 结果 |
|------|------|
| `time` | 显示用法 + 当前时间 |
| `time now` | 当前 10 位秒、13 位毫秒、紧凑时间（如 `20260526111213`）、本地时间 |
| `time 2025-01-01` | 转为 10 位 Unix 秒（及毫秒） |
| `time 1779357292` | 10 位秒 → `YYYY-MM-DD HH:mm:ss` |
| `time 1779357292000` | 13 位毫秒 → `YYYY-MM-DD HH:mm:ss` |

按 **Enter** 复制到剪贴板；若开启「自动粘贴到前台应用」还会粘贴并关闭 Alfred。

支持的日期格式示例：`2025-01-01`、`2025-01-01 12:30:00`、`2025/01/01`。

## 安装

1. 双击 `Timestamp.alfredworkflow` 导入 Alfred；或
2. 在 Alfred → Workflows 中拖入 `alfred-timestamp-workflow` 文件夹内的 `info.plist` 与 `time.py`（需保持同目录）。

重新打包：

```bash
cd alfred-timestamp
zip -r Timestamp.alfredworkflow info.plist time.py icon.png README.md
```

## 本地测试

```bash
python3 time.py now
python3 time.py "2025-01-01"
python3 time.py 1779357292
python3 time.py 1779357292000
```
