import sys
import os
from PyQt6 import QtWidgets
from PyQt6 import QtGui

from ui.main_window import MainWindow


def main():
    """
    应用程序主入口
    """
    # 确保中文正常显示
    os.environ["QT_FONT_DPI"] = "96"
    
    # 创建应用程序实例
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName("PhotoWatermark2")
    app.setApplicationVersion("1.0.0")
    
    # 设置应用程序图标
    icon_path = os.path.join(os.path.dirname(__file__), "..", "resources", "icons", "app_icon.svg")
    if os.path.exists(icon_path):
        app.setWindowIcon(QtGui.QIcon(icon_path))
    
    # 创建主窗口
    main_window = MainWindow()
    main_window.show()
    
    # 运行应用程序
    sys.exit(app.exec())


if __name__ == "__main__":
    main()