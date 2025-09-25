import os
import sys
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
    
    # 自动加载测试图片进行测试
    test_image_path = os.path.join(os.path.dirname(__file__), "..", "lucky_pig.jpeg")
    print(f"测试图片路径: {test_image_path}")
    if os.path.exists(test_image_path):
        print("测试图片存在，正在加载...")
        main_window.open_file_from_path(test_image_path)
        print("测试图片加载成功")
    else:
        print("警告: 测试图片不存在")
    
    # 运行应用程序
    sys.exit(app.exec())


if __name__ == "__main__":
    main()