# Alfred UUID 工作流

关键字 **`uuid`**，生成随机 **UUID v4**（每次打开都会重新生成）。

## 用法

1. 在 Alfred 输入 `uuid`
2. 选中结果，按 **Enter** 复制到剪贴板并粘贴到前台应用

## 安装

双击 `UUID.alfredworkflow` 导入 Alfred。

## 本地测试

```bash
python3 gen_uuid.py
```

## 打包

```bash
cd alfred-uuid
python3 make_icon.py
zip -r UUID.alfredworkflow info.plist gen_uuid.py icon.png README.md
```
