#!/bin/bash

# 这是一个运行脚本，帮助用户直接启动PhotoWatermark2应用程序

# 确保应用程序的可执行权限
echo "正在设置应用程序权限..."
chmod -R +x dist/PhotoWatermark2.app
chmod +x dist/PhotoWatermark2.app/Contents/MacOS/PhotoWatermark2

# 移除隔离属性
echo "正在移除应用程序隔离属性..."
xattr -dr com.apple.quarantine dist/PhotoWatermark2.app

# 启动应用程序
echo "正在启动PhotoWatermark2应用程序..."
open dist/PhotoWatermark2.app

# 等待应用程序启动
sleep 2

# 检查应用程序是否正在运行
if pgrep -x "PhotoWatermark2" > /dev/null
then
    echo "
应用程序已成功启动！

重要提示：
- 首次运行后，macOS会记住这个应用程序是可信的
- 以后您可以直接双击应用程序图标启动
- 如果仍然遇到问题，请尝试右键点击应用图标并选择"打开"
"
else
    echo "
应用程序启动失败。请尝试以下方法：

1. 右键点击dist/PhotoWatermark2.app，选择"打开"
2. 在弹出的对话框中点击"打开"按钮

如果问题依然存在，请联系开发者获取帮助。
"
fi