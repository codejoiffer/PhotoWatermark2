#!/bin/bash

# 更完善的应用程序运行脚本，包含详细的调试和状态检查

# 设置颜色输出
green='\033[0;32m'
red='\033[0;31m'
yellow='\033[0;33m'
blue='\033[0;34m'
nocolor='\033[0m'

# 检查应用程序是否已在运行
check_existing_process() {
    echo -e "${blue}检查是否有PhotoWatermark2进程正在运行...${nocolor}"
    existing_pid=$(pgrep -x "PhotoWatermark2")
    if [ -n "$existing_pid" ]; then
        echo -e "${yellow}发现应用程序已经在运行，进程ID: $existing_pid${nocolor}"
        echo -e "${yellow}如果看不到窗口，请尝试以下操作：${nocolor}"
        echo -e "${yellow}1. 按 Command+Tab 切换应用程序${nocolor}"
        echo -e "${yellow}2. 在Dock中查找应用图标${nocolor}"
        echo -e "${yellow}3. 或者关闭现有进程，重新启动${nocolor}"
        read -p "是否要关闭现有进程并重新启动？(y/n): " choice
        if [ "$choice" = "y" ] || [ "$choice" = "Y" ]; then
            echo -e "${blue}关闭现有进程 $existing_pid...${nocolor}"
            kill -9 "$existing_pid"
            sleep 2
        else
            echo -e "${yellow}已取消操作，应用程序继续运行。${nocolor}"
            exit 0
        fi
    fi
}

# 检查并设置应用程序权限
set_permissions() {
    echo -e "${blue}正在设置应用程序权限...${nocolor}"
    chmod -R +x ./dist/PhotoWatermark2.app
    if [ $? -ne 0 ]; then
        echo -e "${red}设置权限失败，请使用sudo权限重试。${nocolor}"
        exit 1
    fi
    echo -e "${green}权限设置成功。${nocolor}"
}

# 移除隔离属性
remove_quarantine() {
    echo -e "${blue}正在移除应用程序隔离属性...${nocolor}"
    xattr -dr com.apple.quarantine ./dist/PhotoWatermark2.app
    if [ $? -ne 0 ]; then
        echo -e "${red}移除隔离属性失败，请使用sudo权限重试。${nocolor}"
        exit 1
    fi
    echo -e "${green}隔离属性移除成功。${nocolor}"
}

# 检查应用程序完整性
check_app_integrity() {
    echo -e "${blue}检查应用程序完整性...${nocolor}"
    app_path="./dist/PhotoWatermark2.app/Contents/MacOS/PhotoWatermark2"
    if [ ! -f "$app_path" ]; then
        echo -e "${red}错误：应用程序可执行文件不存在。${nocolor}"
        echo -e "${red}请确认应用程序构建正确。${nocolor}"
        exit 1
    fi
    echo -e "${green}应用程序可执行文件存在。${nocolor}"
}

# 启动应用程序并捕获输出
start_application() {
    echo -e "${blue}正在启动PhotoWatermark2应用程序（带详细日志）...${nocolor}"
    echo -e "${yellow}如果应用程序正常启动但看不到窗口，请按Command+Tab查看是否在后台运行。${nocolor}"
    echo -e "${yellow}日志输出将显示在终端中，请等待图形界面出现...${nocolor}"
    echo -e "${yellow}要退出，请在终端中按Ctrl+C，或关闭应用程序窗口。${nocolor}"
    echo -e "-----------------------------------------------"
    
    # 启动应用程序并显示实时日志
    "./dist/PhotoWatermark2.app/Contents/MacOS/PhotoWatermark2"
    
    # 检查启动结果
    exit_code=$?
    if [ $exit_code -eq 0 ]; then
        echo -e "-----------------------------------------------"
        echo -e "${green}应用程序已正常退出。${nocolor}"
    else
        echo -e "-----------------------------------------------"
        echo -e "${red}应用程序异常退出，退出码: $exit_code${nocolor}"
        echo -e "${yellow}请尝试以下解决方案：${nocolor}"
        echo -e "${yellow}1. 右键点击dist/PhotoWatermark2.app，选择'打开'${nocolor}"
        echo -e "${yellow}2. 在弹出的安全对话框中点击'打开'${nocolor}"
        echo -e "${yellow}3. 如果问题持续存在，请联系开发者。${nocolor}"
    fi
}

# 主函数
main() {
    echo -e "${blue}===== PhotoWatermark2 启动助手 =====${nocolor}"
    check_existing_process
    set_permissions
    remove_quarantine
    check_app_integrity
    start_application
}

# 执行主函数
main