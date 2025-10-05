#!/bin/bash

# 确保脚本在错误时退出
set -e

# 创建应用程序目录
build_app_dir="build_app"
rm -rf "$build_app_dir"
mkdir -p "$build_app_dir"

# 复制应用程序到构建目录
# 当前是onedir模式，需要正确复制
cp -R dist/PhotoWatermark2 "$build_app_dir/PhotoWatermark2.app"

# 添加Applications链接
ln -s /Applications "$build_app_dir/Applications"

# 设置权限
chmod -R +x "$build_app_dir/PhotoWatermark2.app"
chmod +x "$build_app_dir/PhotoWatermark2.app/PhotoWatermark2"

# 移除隔离属性和扩展属性
xattr -cr "$build_app_dir/PhotoWatermark2.app"

# 创建一个简单的说明文件，解释如何绕过Gatekeeper
cat > "$build_app_dir/首次运行说明.txt" << EOF
首次运行 PhotoWatermark2 应用程序时，如果遇到无法打开的情况，请按照以下步骤操作：

1. 右键点击应用程序图标，选择"打开"
2. 在弹出的对话框中，点击"打开"按钮
3. 这样系统会记住这个应用程序是可信的，以后双击即可正常打开

这是因为 macOS 的 Gatekeeper 安全机制默认只允许运行来自 App Store 或已识别开发者的应用程序。
EOF

# 创建启动脚本，确保双击能够正确运行
cat > "$build_app_dir/启动PhotoWatermark2.sh" << 'EOF'
#!/bin/bash

# 设置中文环境
export LANG="zh_CN.UTF-8"
export LC_ALL="zh_CN.UTF-8"

# 获取应用程序目录 - 使用绝对路径
APP_DIR="$(cd "$(dirname "$0")"; pwd)/PhotoWatermark2.app"

# 输出调试信息
echo "启动脚本路径: $(cd "$(dirname "$0")"; pwd)"
echo "应用程序目录: $APP_DIR"

# 创建临时日志目录（使用/tmp目录，确保任何用户都有写权限）
TEMP_LOG_DIR="/tmp/PhotoWatermark2_logs"
mkdir -p "$TEMP_LOG_DIR"
echo "已创建临时日志目录: $TEMP_LOG_DIR"

# 设置日志环境变量，让应用程序知道去哪里写日志
export PHOTOWATERMARK2_LOG_DIR="$TEMP_LOG_DIR"
echo "已设置日志环境变量: PHOTOWATERMARK2_LOG_DIR=$TEMP_LOG_DIR"

# 确保应用程序内部的日志目录存在（使用绝对路径）
mkdir -p "$APP_DIR/logs"
echo "已确保应用程序内部日志目录存在"

# 确保resources目录存在（使用绝对路径）
mkdir -p "$APP_DIR/resources/fonts"
mkdir -p "$APP_DIR/resources/icons"
echo "已确保所有必要的资源目录存在"

# 复制资源文件
RESOURCES_SOURCE="$(cd "$(dirname "$0")"; pwd)/resources"
if [ -d "$RESOURCES_SOURCE" ]; then
    echo "正在从 $RESOURCES_SOURCE 复制资源文件到 $APP_DIR/resources/"
    cp -R "$RESOURCES_SOURCE"/* "$APP_DIR/resources/"
else
    echo "警告：资源目录 $RESOURCES_SOURCE 不存在，跳过复制"
fi

# 输出启动信息
clear
echo "正在启动 PhotoWatermark2 应用程序..."
echo "应用程序目录: $APP_DIR"
echo "临时日志目录: $TEMP_LOG_DIR"
echo "已确保所有必要的目录都已创建"
echo ""
echo "如果应用程序正常启动但看不到窗口，请按Command+Tab查看是否在后台运行。"
echo ""
echo "启动日志将显示在终端中..."
echo "-----------------------------------------------"

# 检查应用程序文件是否存在
if [ ! -f "$APP_DIR/PhotoWatermark2" ]; then
    echo "错误：应用程序主文件不存在: $APP_DIR/PhotoWatermark2"
    echo "-----------------------------------------------"
    echo "应用程序文件缺失。请尝试以下方法："
    echo "1. 右键点击PhotoWatermark2.app，选择'打开'"
    echo "2. 在弹出的对话框中点击'打开'按钮"
    echo "3. 如果问题依然存在，请联系开发者获取帮助。"
    read -p "按Enter键退出..."
    exit 1
fi

# 添加执行权限
chmod +x "$APP_DIR/PhotoWatermark2"

# 进入应用程序目录并启动
cd "$APP_DIR"
./PhotoWatermark2

# 检查启动结果
if [ $? -ne 0 ]; then
    echo "-----------------------------------------------"
    echo "应用程序启动失败。请尝试以下方法："
    echo "1. 右键点击PhotoWatermark2.app，选择'打开'"
    echo "2. 在弹出的对话框中点击'打开'按钮"
    echo "3. 如果问题依然存在，请联系开发者获取帮助。"
    read -p "按Enter键退出..."
fi
EOF
chmod +x "$build_app_dir/启动PhotoWatermark2.sh"

# 复制resources目录到DMG根目录，确保资源文件可用
if [ -d "resources" ]; then
    cp -R "resources" "$build_app_dir/"
fi

# 清理旧的DMG
rm -f dist/PhotoWatermark2_1.0.0.dmg

# 创建新的DMG
hdiutil create -volname "PhotoWatermark2" -srcfolder "$build_app_dir" -ov -format UDZO dist/PhotoWatermark2_1.0.0.dmg

# 清理临时目录
rm -rf "$build_app_dir"

# 输出成功信息
echo "DMG创建成功: dist/PhotoWatermark2_1.0.0.dmg"
echo "
重要提示：
1. 双击DMG文件，将应用程序拖到Applications文件夹完成安装
2. 首次运行时，请右键点击应用程序图标，选择"打开"
3. 在弹出的对话框中，再次点击"打开"按钮以绕过Gatekeeper安全检查
4. 以后双击即可正常打开应用程序
5. 您也可以使用DMG中的"启动PhotoWatermark2.sh"脚本直接启动应用程序"