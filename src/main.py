import os
import sys
from PyQt6 import QtWidgets
from PyQt6 import QtGui

# 确保能正确导入项目模块
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.ui.main_window import MainWindow
from src.utils.logger import info, warning, error

def main():
    """
    应用程序主入口
    """
    # 确保中文正常显示
    os.environ["QT_FONT_DPI"] = "96"
    # 告诉Qt使用Unicode字体
    os.environ["QT_QPA_FONTDIR"] = os.path.join(
        os.path.dirname(__file__), "..", "resources", "fonts")
    # 确保matplotlib等库也能正确显示中文
    os.environ["MPLCONFIGDIR"] = os.path.join(
        os.path.dirname(__file__), "..", ".matplotlib")
    
    info("应用程序启动")
    info(f"字体目录设置: {os.environ.get('QT_QPA_FONTDIR')}")
    
    # 创建应用程序实例
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName("PhotoWatermark2")
    app.setApplicationVersion("1.0.0")
    info(f"应用程序版本: {app.applicationVersion()}")
    
    # 设置应用程序图标
    icon_path = os.path.join(os.path.dirname(__file__), "..", "resources", "icons", "app_icon.svg")
    if os.path.exists(icon_path):
        app.setWindowIcon(QtGui.QIcon(icon_path))
        info(f"已设置应用图标: {icon_path}")
    else:
        warning(f"应用图标不存在: {icon_path}")
    
    # 创建主窗口
    info("创建主窗口")
    main_window = MainWindow()
    main_window.show()
    info("主窗口已显示")
    
    # 自动加载测试图片进行测试
    test_image_path = os.path.join(os.path.dirname(__file__), "..", "lucky_pig.jpeg")
    info(f"测试图片路径: {test_image_path}")
    if os.path.exists(test_image_path):
        info("测试图片存在，正在加载...")
        main_window.open_file_from_path(test_image_path)
        info("测试图片加载成功")
    else:
        warning("测试图片不存在")
    
    # 运行应用程序
    try:
        info("应用程序开始运行")
        sys.exit(app.exec())
    except Exception as e:
        error(f"应用程序异常退出: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()