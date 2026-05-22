# Alfred 有道翻译工作流

关键字 **`yd`**，调用有道智云文本翻译 API。

## 翻译规则

| 输入示例 | 方向 |
|----------|------|
| `yd 你好` | 中文 → 英文 |
| `yd hello` | 英文 → 中文 |
| `yd bonjour` / `yd こんにちは` | 其它语言（自动识别）→ 中文 |

按 **Enter** 复制译文并粘贴到前台应用（自动关闭 Alfred）。

## 配置 API 密钥

1. 打开 [有道智云控制台](https://ai.youdao.com/console/)
2. 创建应用，绑定 **文本翻译** 服务
3. 记下 **应用ID**（appKey）和 **应用密钥**（appSecret）

任选一种配置方式：

**方式 A — Alfred 环境变量（推荐）**

Workflows → Youdao Translate → 右上角 `[x]` → 环境变量：

- `youdao_app_key` = 应用ID
- `youdao_app_secret` = 应用密钥

**方式 B — 配置文件**

```bash
cp config.example.json config.json
# 编辑 config.json 填入 app_key、app_secret
```

## 安装

双击 `Youdao.alfredworkflow` 导入 Alfred。

## 本地测试

```bash
# 先配置 config.json 或导出环境变量
export youdao_app_key="你的ID"
export youdao_app_secret="你的密钥"

python3 yd.py "你好"
python3 yd.py "hello"
python3 yd.py "bonjour"
```

## 打包

```bash
cd workflows/alfred-youdao
python3 make_icon.py
zip -r Youdao.alfredworkflow info.plist yd.py icon.png config.example.json README.md
```
