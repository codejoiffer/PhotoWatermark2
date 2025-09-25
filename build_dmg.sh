#!/bin/bash

# 构建DMG安装包脚本
# 这个脚本会使用PyInstaller打包应用程序，然后创建DMG安装包

# 设置项目根目录
PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"

# 设置输出目录
OUTPUT_DIR="${PROJECT_DIR}/dist"
BUILD_DIR="${PROJECT_DIR}/build"

# 确保输出目录存在
mkdir -p "${OUTPUT_DIR}"

# 安装构建依赖
echo "安装构建依赖..."
pip install pyinstaller

# 检查是否安装了create-dmg工具
if ! command -v create-dmg &> /dev/null
then
    echo "create-dmg工具未安装，尝试安装..."
    if command -v brew &> /dev/null
    then
        brew install create-dmg
    else
        echo "错误: 未找到Homebrew包管理器。请先安装Homebrew，然后使用 'brew install create-dmg' 安装create-dmg工具。"
        exit 1
    fi
fi

# 使用PyInstaller打包应用程序
echo "使用PyInstaller打包应用程序..."
pyinstaller --name="PhotoWatermark2" \
            --windowed \
            --icon="${PROJECT_DIR}/resources/icons/app_icon.svg" \
            --add-data="${PROJECT_DIR}/resources/icons:resources/icons" \
            --distpath="${OUTPUT_DIR}" \
            --workpath="${BUILD_DIR}" \
            "${PROJECT_DIR}/src/main.py"

# 检查PyInstaller是否成功
exit_code=$?
if [ $exit_code -ne 0 ]
then
    echo "错误: PyInstaller打包失败"
    exit $exit_code
fi

# 创建DMG安装包
echo "创建DMG安装包..."
DMG_NAME="PhotoWatermark2_1.0.0.dmg"
APP_PATH="${OUTPUT_DIR}/PhotoWatermark2.app"

# 清理旧的DMG文件
if [ -f "${OUTPUT_DIR}/${DMG_NAME}" ]
then
    rm "${OUTPUT_DIR}/${DMG_NAME}"
fi

# 使用create-dmg创建安装包
create-dmg \
  --volname "PhotoWatermark2 安装包" \
  --volicon "${PROJECT_DIR}/resources/icons/app_icon.svg" \
  --window-pos 200 120 \
  --window-size 800 400 \
  --icon-size 100 \
  --icon "PhotoWatermark2.app" 200 190 \
  --hide-extension "PhotoWatermark2.app" \
  --app-drop-link 600 190 \
  "${OUTPUT_DIR}/${DMG_NAME}" \
  "${APP_PATH}"

# 检查create-dmg是否成功
exit_code=$?
if [ $exit_code -ne 0 ]
then
    echo "错误: DMG创建失败"
    exit $exit_code
fi

echo "成功: DMG安装包已创建在 ${OUTPUT_DIR}/${DMG_NAME}"
echo "\n提示：要测试安装包，您可以双击 ${OUTPUT_DIR}/${DMG_NAME} 文件进行安装。"