import sys
import os
from PyQt6 import QtWidgets
from PyQt6 import QtGui
from PyQt6 import QtCore

# 从各个模块导入所需组件
from PyQt6.QtWidgets import (
    QMainWindow, QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFileDialog, QSplitter, QTabWidget,
    QScrollArea, QMessageBox, QProgressBar, QStatusBar, QMenuBar,
    QMenu, QToolBar, QGroupBox, QFormLayout, QComboBox,
    QSpinBox, QDoubleSpinBox, QColorDialog, QFontDialog, QCheckBox,
    QSlider, QToolButton, QListWidget, QListWidgetItem, QFrame, QLineEdit
)
from PyQt6.QtGui import (
    QPixmap, QImage, QFont, QIcon, QColor, QPainter, QPen, QBrush,
    QAction  # QAction在QtGui模块中
)
from PyQt6.QtCore import (
    Qt, QSize, QRect, QPoint, QThread, pyqtSignal
)

from src.core.image_processor import ImageProcessor
from src.core.watermark import Watermark
from src.core.batch_processor import BatchProcessor
from src.utils.template_manager import TemplateManager
from src.utils.config import ConfigManager
from src.utils.logger import info, warning, error


class MainWindow(QtWidgets.QMainWindow):
    """
    主窗口类，应用程序的主要界面
    """
    
    def __init__(self):
        super().__init__()
        
        # 应用程序版本
        self.app_version = "1.0.0"
        
        # 初始化管理器
        self.config_manager = ConfigManager()
        self.template_manager = TemplateManager()
        
        # 当前打开的图片路径
        self.current_image_path = None
        self.current_image = None
        
        # 当前水印对象
        self.current_watermark = Watermark()
        
        # 初始化UI
        self.init_ui()
        
        # 加载配置
        self.load_config()
    
    def init_ui(self):
        """
        初始化用户界面
        """
        # 设置窗口标题和大小
        self.setWindowTitle(f"PhotoWatermark2 - v{self.app_version}")
        
        # 从配置中获取窗口大小和位置
        window_position = self.config_manager.get('window_position', {'x': 100, 'y': 100})
        window_size = self.config_manager.get('window_size', {'width': 1200, 'height': 800})
        
        self.move(window_position['x'], window_position['y'])
        self.resize(window_size['width'], window_size['height'])
        
        # 创建中央部件
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        
        # 主布局
        main_layout = QtWidgets.QVBoxLayout(central_widget)
        
        # 创建菜单栏
        self.create_menu_bar()
        
        # 创建工具栏
        self.create_tool_bar()
        
        # 创建主分割器
        main_splitter = QtWidgets.QSplitter(QtCore.Qt.Orientation.Horizontal)
        main_layout.addWidget(main_splitter)
        
        # 左侧面板（水印设置）
        left_panel = self.create_left_panel()
        main_splitter.addWidget(left_panel)
        
        # 右侧面板（预览区域）
        right_panel = self.create_right_panel()
        main_splitter.addWidget(right_panel)
        
        # 设置分割器的初始大小
        main_splitter.setSizes([400, 800])
        
        # 创建状态栏
        self.create_status_bar()
    
    def create_menu_bar(self):
        """
        创建菜单栏
        """
        # 获取菜单栏
        menu_bar = self.menuBar()
        
        # 文件菜单
        file_menu = menu_bar.addMenu("文件")
        
        # 打开文件动作
        open_action = QAction("打开文件", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)
        
        # 打开文件夹动作
        open_folder_action = QAction("打开文件夹", self)
        open_folder_action.setShortcut("Ctrl+D")
        open_folder_action.triggered.connect(self.open_folder)
        file_menu.addAction(open_folder_action)
        
        # 最近文件子菜单
        recent_files_menu = QMenu("最近文件", self)
        file_menu.addMenu(recent_files_menu)
        self.update_recent_files_menu(recent_files_menu)
        
        # 分隔线
        file_menu.addSeparator()
        
        # 保存当前图片动作
        save_action = QAction("保存", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_image)
        file_menu.addAction(save_action)
        
        # 另存为动作
        save_as_action = QAction("另存为", self)
        save_as_action.setShortcut("Ctrl+Shift+S")
        save_as_action.triggered.connect(self.save_image_as)
        file_menu.addAction(save_as_action)
        
        # 分隔线
        file_menu.addSeparator()
        
        # 退出动作
        exit_action = QAction("退出", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # 编辑菜单
        edit_menu = menu_bar.addMenu("编辑")
        
        # 撤销动作
        undo_action = QAction("撤销", self)
        undo_action.setShortcut("Ctrl+Z")
        # TODO: 实现撤销功能
        undo_action.triggered.connect(lambda: None)
        edit_menu.addAction(undo_action)
        
        # 分隔线
        edit_menu.addSeparator()
        
        # 复制动作
        copy_action = QAction("复制", self)
        copy_action.setShortcut("Ctrl+C")
        # TODO: 实现复制功能
        copy_action.triggered.connect(lambda: None)
        edit_menu.addSeparator()
        
        # 首选项动作
        preferences_action = QAction("首选项", self)
        # TODO: 实现首选项功能
        preferences_action.triggered.connect(lambda: None)
        edit_menu.addAction(preferences_action)
        
        # 批量处理菜单
        batch_menu = menu_bar.addMenu("批量处理")
        
        # 启动批量处理动作
        start_batch_action = QAction("启动批量处理", self)
        start_batch_action.setShortcut("Ctrl+B")
        # TODO: 实现批量处理功能
        start_batch_action.triggered.connect(lambda: None)
        batch_menu.addAction(start_batch_action)
        
        # 模板菜单
        template_menu = menu_bar.addMenu("模板")
        
        # 保存模板动作
        save_template_action = QAction("保存当前模板", self)
        save_template_action.triggered.connect(self.save_current_template)
        template_menu.addAction(save_template_action)
        
        # 加载模板动作
        load_template_action = QAction("加载模板", self)
        load_template_action.triggered.connect(self.load_template)
        template_menu.addAction(load_template_action)
        
        # 帮助菜单
        help_menu = menu_bar.addMenu("帮助")
        
        # 使用帮助动作
        help_action = QAction("使用帮助", self)
        # TODO: 实现使用帮助功能
        help_action.triggered.connect(lambda: None)
        help_menu.addAction(help_action)
        
        # 关于动作
        about_action = QAction("关于", self)
        about_action.triggered.connect(self.show_about_dialog)
        help_menu.addAction(about_action)
    
    def create_tool_bar(self):
        """
        创建工具栏
        """
        tool_bar = QToolBar("主工具栏")
        self.addToolBar(tool_bar)
        
        # 打开文件按钮
        open_button = QToolButton()
        open_button.setText("打开文件")
        open_button.setToolTip("打开图片文件 (Ctrl+O)")
        open_button.clicked.connect(self.open_file)
        tool_bar.addWidget(open_button)
        
        # 保存按钮
        save_button = QToolButton()
        save_button.setText("保存")
        save_button.setToolTip("保存图片 (Ctrl+S)")
        save_button.clicked.connect(self.save_image)
        tool_bar.addWidget(save_button)
        
        # 分隔线
        tool_bar.addSeparator()
        
        # 批量处理按钮
        batch_button = QToolButton()
        batch_button.setText("批量处理")
        batch_button.setToolTip("批量添加水印 (Ctrl+B)")
        # TODO: 实现批量处理功能
        batch_button.clicked.connect(lambda: None)
        tool_bar.addWidget(batch_button)
        
        # 分隔线
        tool_bar.addSeparator()
        
        # 模板按钮
        template_button = QToolButton()
        template_button.setText("模板")
        template_button.setToolTip("管理水印模板")
        # TODO: 实现模板管理功能
        template_button.clicked.connect(lambda: None)
        tool_bar.addWidget(template_button)
    
    def create_left_panel(self):
        """
        创建左侧面板（水印设置）
        """
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        
        # 创建标签页
        tab_widget = QTabWidget()
        left_layout.addWidget(tab_widget)
        
        # 文本水印标签页
        text_watermark_tab = self.create_text_watermark_tab()
        tab_widget.addTab(text_watermark_tab, "文本水印")
        
        # 图片水印标签页
        image_watermark_tab = self.create_image_watermark_tab()
        tab_widget.addTab(image_watermark_tab, "图片水印")
        
        # 输出设置标签页
        output_settings_tab = self.create_output_settings_tab()
        tab_widget.addTab(output_settings_tab, "输出设置")
        
        return left_panel
    
    def create_text_watermark_tab(self):
        """
        创建文本水印设置标签页
        """
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # 文本设置组
        text_group = QGroupBox("文本设置")
        text_form = QFormLayout()
        
        # 水印文本输入
        self.watermark_text_edit = QLineEdit("水印文本")
        text_form.addRow("水印文本:", self.watermark_text_edit)
        
        # 字体设置
        self.font_button = QPushButton("选择字体")
        self.font_label = QLabel("Arial, 12pt")
        font_layout = QHBoxLayout()
        font_layout.addWidget(self.font_button)
        font_layout.addWidget(self.font_label)
        text_form.addRow("字体:", font_layout)
        self.font_button.clicked.connect(self.select_font)
        
        # 颜色设置
        self.color_button = QPushButton("选择颜色")
        self.color_preview = QFrame()
        self.color_preview.setMinimumSize(40, 20)
        self.color_preview.setStyleSheet("background-color: #000000;")
        color_layout = QHBoxLayout()
        color_layout.addWidget(self.color_button)
        color_layout.addWidget(self.color_preview)
        text_form.addRow("颜色:", color_layout)
        self.color_button.clicked.connect(self.select_color)
        
        # 透明度设置
        self.opacity_slider = QSlider(Qt.Orientation.Horizontal)
        self.opacity_slider.setRange(1, 100)
        self.opacity_slider.setValue(70)
        self.opacity_value = QLabel("70%")
        opacity_layout = QHBoxLayout()
        opacity_layout.addWidget(self.opacity_slider)
        opacity_layout.addWidget(self.opacity_value)
        text_form.addRow("透明度:", opacity_layout)
        self.opacity_slider.valueChanged.connect(
            lambda value: self.opacity_value.setText(f"{value}%"))
        
        text_group.setLayout(text_form)
        layout.addWidget(text_group)
        
        # 布局设置组
        layout_group = QGroupBox("布局设置")
        layout_form = QFormLayout()
        
        # 位置设置
        self.position_combo = QComboBox()
        positions = ["左上", "右上", "左下", "右下", "居中", "自定义"]
        self.position_combo.addItems(positions)
        self.position_combo.setCurrentIndex(4)  # 默认居中
        layout_form.addRow("位置:", self.position_combo)
        
        # 旋转设置
        self.rotation_slider = QSlider(Qt.Orientation.Horizontal)
        self.rotation_slider.setRange(-180, 180)
        self.rotation_slider.setValue(0)
        self.rotation_value = QLabel("0°")
        rotation_layout = QHBoxLayout()
        rotation_layout.addWidget(self.rotation_slider)
        rotation_layout.addWidget(self.rotation_value)
        layout_form.addRow("旋转:", rotation_layout)
        self.rotation_slider.valueChanged.connect(
            lambda value: self.rotation_value.setText(f"{value}°"))
        
        # 大小设置
        self.font_size_spin = QSpinBox()
        self.font_size_spin.setRange(1, 200)
        self.font_size_spin.setValue(24)
        self.font_size_spin.setSuffix(" pt")
        layout_form.addRow("字体大小:", self.font_size_spin)
        
        layout_group.setLayout(layout_form)
        layout.addWidget(layout_group)
        
        # 高级设置组
        advanced_group = QGroupBox("高级设置")
        advanced_form = QFormLayout()
        
        # 阴影设置
        self.shadow_check = QCheckBox()
        self.shadow_check.setChecked(False)
        advanced_form.addRow("添加阴影:", self.shadow_check)
        
        # 描边设置
        self.stroke_check = QCheckBox()
        self.stroke_check.setChecked(False)
        advanced_form.addRow("添加描边:", self.stroke_check)
        
        # 平铺设置
        self.tile_check = QCheckBox()
        self.tile_check.setChecked(False)
        advanced_form.addRow("平铺水印:", self.tile_check)
        
        # 平铺间距设置
        self.tile_spacing_spin = QSpinBox()
        self.tile_spacing_spin.setRange(10, 200)
        self.tile_spacing_spin.setValue(50)
        self.tile_spacing_spin.setEnabled(False)
        advanced_form.addRow("平铺间距:", self.tile_spacing_spin)
        self.tile_check.toggled.connect(self.tile_spacing_spin.setEnabled)
        
        advanced_group.setLayout(advanced_form)
        layout.addWidget(advanced_group)
        
        # 应用按钮
        apply_button = QPushButton("应用水印")
        apply_button.clicked.connect(self.apply_watermark)
        layout.addWidget(apply_button)
        
        # 添加伸缩空间
        layout.addStretch()
        
        return widget
    
    def create_image_watermark_tab(self):
        """
        创建图片水印设置标签页
        """
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # 水印图片设置组
        image_group = QGroupBox("水印图片设置")
        image_form = QFormLayout()
        
        # 选择水印图片按钮
        self.watermark_image_path_edit = QLineEdit()
        self.watermark_image_path_edit.setReadOnly(True)
        self.select_image_button = QPushButton("选择水印图片")
        image_path_layout = QHBoxLayout()
        image_path_layout.addWidget(self.watermark_image_path_edit)
        image_path_layout.addWidget(self.select_image_button)
        image_form.addRow("水印图片:", image_path_layout)
        self.select_image_button.clicked.connect(self.select_watermark_image)
        
        # 透明度设置
        self.image_opacity_slider = QSlider(Qt.Orientation.Horizontal)
        self.image_opacity_slider.setRange(1, 100)
        self.image_opacity_slider.setValue(70)
        self.image_opacity_value = QLabel("70%")
        image_opacity_layout = QHBoxLayout()
        image_opacity_layout.addWidget(self.image_opacity_slider)
        image_opacity_layout.addWidget(self.image_opacity_value)
        image_form.addRow("透明度:", image_opacity_layout)
        self.image_opacity_slider.valueChanged.connect(
            lambda value: self.image_opacity_value.setText(f"{value}%"))
        
        # 缩放设置
        self.scale_spin = QDoubleSpinBox()
        self.scale_spin.setRange(0.1, 5.0)
        self.scale_spin.setValue(1.0)
        self.scale_spin.setSingleStep(0.1)
        self.scale_spin.setSuffix("x")
        image_form.addRow("缩放比例:", self.scale_spin)
        
        image_group.setLayout(image_form)
        layout.addWidget(image_group)
        
        # 布局设置组
        layout_group = QGroupBox("布局设置")
        layout_form = QFormLayout()
        
        # 位置设置
        self.image_position_combo = QComboBox()
        positions = ["左上", "右上", "左下", "右下", "居中", "自定义"]
        self.image_position_combo.addItems(positions)
        self.image_position_combo.setCurrentIndex(4)  # 默认居中
        layout_form.addRow("位置:", self.image_position_combo)
        
        # 旋转设置
        self.image_rotation_slider = QSlider(Qt.Orientation.Horizontal)
        self.image_rotation_slider.setRange(-180, 180)
        self.image_rotation_slider.setValue(0)
        self.image_rotation_value = QLabel("0°")
        image_rotation_layout = QHBoxLayout()
        image_rotation_layout.addWidget(self.image_rotation_slider)
        image_rotation_layout.addWidget(self.image_rotation_value)
        layout_form.addRow("旋转:", image_rotation_layout)
        self.image_rotation_slider.valueChanged.connect(
            lambda value: self.image_rotation_value.setText(f"{value}°"))
        
        # 平铺设置
        self.image_tile_check = QCheckBox()
        self.image_tile_check.setChecked(False)
        layout_form.addRow("平铺水印:", self.image_tile_check)
        
        # 平铺间距设置
        self.image_tile_spacing_spin = QSpinBox()
        self.image_tile_spacing_spin.setRange(10, 200)
        self.image_tile_spacing_spin.setValue(50)
        self.image_tile_spacing_spin.setEnabled(False)
        layout_form.addRow("平铺间距:", self.image_tile_spacing_spin)
        self.image_tile_check.toggled.connect(self.image_tile_spacing_spin.setEnabled)
        
        layout_group.setLayout(layout_form)
        layout.addWidget(layout_group)
        
        # 应用按钮
        apply_button = QPushButton("应用水印")
        apply_button.clicked.connect(self.apply_watermark)
        layout.addWidget(apply_button)
        
        # 添加伸缩空间
        layout.addStretch()
        
        return widget
    
    def create_output_settings_tab(self):
        """
        创建输出设置标签页
        """
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # 输出设置组
        output_group = QGroupBox("输出设置")
        output_form = QFormLayout()
        
        # 获取当前输出设置
        output_settings = self.config_manager.get_output_settings()
        
        # 输出格式选择
        self.output_format_combo = QComboBox()
        formats = ["PNG", "JPEG", "WEBP", "TIFF", "BMP"]
        self.output_format_combo.addItems(formats)
        # 设置当前格式
        if output_settings['format'] in formats:
            self.output_format_combo.setCurrentText(output_settings['format'])
        output_form.addRow("输出格式:", self.output_format_combo)
        
        # 输出质量设置
        self.output_quality_slider = QSlider(Qt.Orientation.Horizontal)
        self.output_quality_slider.setRange(1, 100)
        self.output_quality_slider.setValue(output_settings['quality'])
        self.output_quality_value = QLabel(f"{output_settings['quality']}%")
        quality_layout = QHBoxLayout()
        quality_layout.addWidget(self.output_quality_slider)
        quality_layout.addWidget(self.output_quality_value)
        output_form.addRow("输出质量:", quality_layout)
        self.output_quality_slider.valueChanged.connect(
            lambda value: self.output_quality_value.setText(f"{value}%"))
        
        # 文件命名设置
        # 前缀
        self.rename_prefix_edit = QLineEdit(output_settings['prefix'])
        output_form.addRow("文件前缀:", self.rename_prefix_edit)
        
        # 后缀
        self.rename_suffix_edit = QLineEdit(output_settings['suffix'])
        output_form.addRow("文件后缀:", self.rename_suffix_edit)
        
        # 记住最后输出目录
        self.remember_output_dir_check = QCheckBox()
        self.remember_output_dir_check.setChecked(output_settings['remember_dir'])
        output_form.addRow("记住输出目录:", self.remember_output_dir_check)
        
        # 保存设置按钮
        self.save_output_settings_button = QPushButton("保存设置")
        self.save_output_settings_button.clicked.connect(self.save_output_settings)
        output_form.addRow(self.save_output_settings_button)
        
        output_group.setLayout(output_form)
        layout.addWidget(output_group)
        
        # 添加伸缩空间
        layout.addStretch()
        
        return widget
    
    def create_right_panel(self):
        """
        创建右侧面板（预览区域）
        """
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        
        # 预览区域
        self.preview_label = QLabel("请打开一张图片")
        self.preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview_label.setMinimumSize(400, 300)
        self.preview_label.setStyleSheet("background-color: #f0f0f0;")
        
        # 滚动区域
        scroll_area = QScrollArea()
        scroll_area.setWidget(self.preview_label)
        scroll_area.setWidgetResizable(True)
        right_layout.addWidget(scroll_area)
        
        # 图片信息
        self.image_info_label = QLabel("未加载图片")
        right_layout.addWidget(self.image_info_label)
        
        return right_panel
    
    def create_status_bar(self):
        """
        创建状态栏
        """
        status_bar = QStatusBar()
        self.setStatusBar(status_bar)
        
        # 状态标签
        self.status_label = QLabel("就绪")
        status_bar.addWidget(self.status_label)
        
        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximumWidth(200)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(False)
        status_bar.addPermanentWidget(self.progress_bar)
    
    def load_config(self):
        """
        加载配置
        """
        # 从配置中加载窗口大小和位置
        # 在init_ui中已经处理
        
        # 加载最近的会话状态
        last_session = self.config_manager.load_last_session()
        if last_session:
            # TODO: 恢复上次会话状态
            pass
    
    def save_config(self):
        """
        保存配置
        """
        # 保存窗口大小和位置
        self.config_manager.set('window_position', {
            'x': self.x(),
            'y': self.y()
        })
        self.config_manager.set('window_size', {
            'width': self.width(),
            'height': self.height()
        })
        
        # 保存当前配置
        self.config_manager.save()
        
        # 保存当前会话状态
        session_data = {
            # TODO: 添加需要保存的会话状态
        }
        self.config_manager.save_last_session(session_data)
    
    def update_recent_files_menu(self, menu):
        """
        更新最近文件菜单
        """
        # 清空现有菜单
        menu.clear()
        
        # 获取最近文件列表
        recent_files = self.config_manager.get_recent_files()
        
        if not recent_files:
            # 如果没有最近文件，添加禁用的"无最近文件"项
            no_recent_action = QAction("无最近文件", self)
            no_recent_action.setEnabled(False)
            menu.addAction(no_recent_action)
        else:
            # 添加最近文件到菜单
            for i, file_path in enumerate(recent_files):
                action = QAction(f"{i+1}. {os.path.basename(file_path)}", self)
                action.setToolTip(file_path)
                action.triggered.connect(lambda checked=False, path=file_path: self.open_file_from_path(path))
                menu.addAction(action)
            
            # 添加分隔线和"清除列表"项
            menu.addSeparator()
            clear_action = QAction("清除列表", self)
            clear_action.triggered.connect(self.clear_recent_files)
            menu.addAction(clear_action)
    
    def open_file(self):
        """
        打开文件对话框，选择图片文件
        """
        info("打开文件对话框")
        # 获取支持的图片格式
        supported_formats = ImageProcessor.SUPPORTED_FORMATS
        
        # 构建文件过滤器 - 使用PyQt6推荐的格式
        image_formats_str = " ".join([f"*{ext}" for ext in supported_formats])
        filter_str = f"图片文件 ({image_formats_str});;所有文件 (*)"
        info(f"文件过滤器: {filter_str}")
        
        # 打开文件对话框 - 指定使用原生对话框样式
        file_path, _ = QFileDialog.getOpenFileName(
            self, "打开图片", os.path.expanduser("~"), filter_str,
            options=QFileDialog.Option.DontUseNativeDialog
        )
        
        if file_path:
            info(f"选择的文件路径: {file_path}")
            self.open_file_from_path(file_path)
        else:
            info("未选择任何文件")
    
    def open_file_from_path(self, file_path):
        """
        从文件路径打开图片
        """
        try:
            info(f"尝试加载图片: {file_path}")
            # 加载图片
            self.current_image_path = file_path
            self.current_image = ImageProcessor.load_image(file_path)
            info(f"图片加载成功: {os.path.basename(file_path)}")
            
            # 更新预览
            info("更新图片预览")
            self.update_preview()
            info("预览更新完成")
            
            # 更新图片信息
            info("更新图片信息")
            self.update_image_info()
            
            # 添加到最近文件
            info("添加到最近文件列表")
            self.config_manager.add_recent_file(file_path)
            
            # 更新状态
            self.status_label.setText(f"已加载: {os.path.basename(file_path)}")
            info(f"状态更新: 已加载 - {os.path.basename(file_path)}")
            
        except Exception as e:
            error(f"加载图片失败: {str(e)}")
            QMessageBox.critical(self, "错误", f"加载图片失败: {str(e)}")
    
    def open_folder(self):
        """
        打开文件夹对话框，选择图片文件夹
        """
        # TODO: 实现打开文件夹功能
        QMessageBox.information(self, "提示", "打开文件夹功能尚未实现")
    
    def save_image(self):
        """
        保存当前图片
        """
        if not self.current_image:
            QMessageBox.warning(self, "警告", "没有可保存的图片")
            return
        
        try:
            # 如果是已有文件，直接保存
            if self.current_image_path:
                # 获取输出设置
                output_settings = self.config_manager.get_output_settings()
                
                # 保存图片
                ImageProcessor.save_image(
                    self.current_image,
                    self.current_image_path,
                    format=output_settings['format'],
                    quality=output_settings['quality']
                )
                
                # 更新状态
                self.status_label.setText(f"已保存: {os.path.basename(self.current_image_path)}")
            else:
                # 如果是新文件，调用另存为
                self.save_image_as()
        except Exception as e:
            QMessageBox.critical(self, "错误", f"保存图片失败: {str(e)}")
    
    def save_image_as(self):
        """
        另存为对话框，保存当前图片
        """
        if not self.current_image:
            QMessageBox.warning(self, "警告", "没有可保存的图片")
            return
        
        try:
            # 获取输出设置
            output_settings = self.config_manager.get_output_settings()
            
            # 构建文件过滤器
            filter_str = f"{output_settings['format']} 文件 (*.{output_settings['format'].lower()})"
            filter_str += ";;所有文件 (*.*)"
            
            # 获取默认保存目录
            default_dir = output_settings['last_dir'] if output_settings['remember_dir'] else ""
            
            # 打开另存为对话框
            file_path, _ = QFileDialog.getSaveFileName(
                self, "另存为", default_dir,
                filter_str
            )
            
            if file_path:
                # 确保文件扩展名正确
                ext = output_settings['format'].lower()
                if not file_path.lower().endswith(f".{ext}"):
                    file_path += f".{ext}"
                
                # 应用重命名前缀和后缀
                dir_path, filename = os.path.split(file_path)
                name, ext = os.path.splitext(filename)
                new_filename = f"{output_settings['prefix']}{name}{output_settings['suffix']}{ext}"
                file_path = os.path.join(dir_path, new_filename)
                
                # 保存图片
                ImageProcessor.save_image(
                    self.current_image,
                    file_path,
                    format=output_settings['format'],
                    quality=output_settings['quality']
                )
                
                # 更新当前图片路径
                self.current_image_path = file_path
                
                # 保存最后输出目录
                if output_settings['remember_dir']:
                    self.config_manager.save_output_settings({
                        'last_dir': os.path.dirname(file_path)
                    })
                
                # 更新状态
                self.status_label.setText(f"已保存: {os.path.basename(file_path)}")
                
        except Exception as e:
            QMessageBox.critical(self, "错误", f"保存图片失败: {str(e)}")
    
    def apply_watermark(self):
        """
        应用水印到当前图片
        """
        if not self.current_image:
            QMessageBox.warning(self, "警告", "请先打开一张图片")
            return
        
        try:
            # 获取当前选中的标签页（文本水印或图片水印）
            tab_widget = self.findChild(QTabWidget)
            current_tab_index = tab_widget.currentIndex()
            
            if current_tab_index == 0:  # 文本水印
                # 获取文本水印设置
                text = self.watermark_text_edit.text()
                font_str = self.font_label.text()
                color_str = self.color_preview.styleSheet()[len("background-color: "):]
                opacity = self.opacity_slider.value() / 100.0
                rotation = self.rotation_slider.value()
                font_size = self.font_size_spin.value()
                position = self.position_combo.currentText()
                
                # 获取高级设置
                has_shadow = self.shadow_check.isChecked()
                has_stroke = self.stroke_check.isChecked()
                use_tile = self.tile_check.isChecked()
                tile_spacing = self.tile_spacing_spin.value()
                
                # 尝试从字体信息中解析字体名称
                font_name = "Arial"
                try:
                    parts = font_str.split(",")
                    if len(parts) > 0:
                        font_name = parts[0].strip()
                except Exception:
                    pass
                
                # 构建字体信息
                font = (font_name, font_size)
                
                # 更新当前水印设置
                self.current_watermark.watermark_type = 'text'
                self.current_watermark.text = text
                self.current_watermark.font_name = font_name
                self.current_watermark.font_size = font_size
                # 转换颜色为RGBA
                q_color = QColor(color_str)
                self.current_watermark.font_color = (q_color.red(), q_color.green(), q_color.blue(), int(255 * opacity))
                self.current_watermark.opacity = opacity * 100  # 存储为0-100的整数
                self.current_watermark.rotation = rotation
                self.current_watermark.position = position
                self.current_watermark.has_shadow = has_shadow
                self.current_watermark.has_stroke = has_stroke
                
                # 应用文本水印
                if use_tile:
                    # 使用平铺水印
                    watermarked_image = ImageProcessor.add_tiled_watermark(
                        self.current_image,
                        text,
                        font_name=font_name,
                        font_size=font_size,
                        font_color=(q_color.red(), q_color.green(), q_color.blue(), int(255 * opacity)),
                        rotation=rotation,
                        spacing=tile_spacing
                    )
                else:
                    # 应用阴影和描边效果
                    watermark = Watermark()
                    watermark.set_text_watermark(text, font_name, font_size, (q_color.red(), q_color.green(), q_color.blue()), opacity * 100)
                    watermark.set_position(position)
                    watermark.set_rotation(rotation)
                    watermark.set_style(has_shadow, has_stroke)
                    watermarked_image = watermark.apply_watermark(self.current_image)
            elif current_tab_index == 1:  # 图片水印
                # 获取图片水印设置
                image_path = self.watermark_image_path_edit.text()
                
                if not image_path or not os.path.exists(image_path):
                    QMessageBox.warning(self, "警告", "请先选择一个有效的水印图片")
                    return
                
                opacity = self.image_opacity_slider.value() / 100.0
                scale = self.scale_spin.value()
                rotation = self.image_rotation_slider.value()
                position = self.image_position_combo.currentText()
                
                # 获取高级设置
                use_tile = self.image_tile_check.isChecked()
                tile_spacing = self.image_tile_spacing_spin.value()
                
                # 更新当前水印设置
                self.current_watermark.watermark_type = 'image'
                self.current_watermark.watermark_path = image_path
                self.current_watermark.opacity = opacity * 100  # 存储为0-100的整数
                self.current_watermark.scale = scale
                self.current_watermark.rotation = rotation
                self.current_watermark.position = position
                
                # 应用图片水印
                if use_tile:
                    # 使用平铺水印
                    watermarked_image = ImageProcessor.add_tiled_image_watermark(
                        self.current_image,
                        image_path,
                        opacity=opacity * 100,
                        scale=scale,
                        rotation=rotation,
                        spacing=tile_spacing
                    )
                else:
                    # 应用普通图片水印
                    watermarked_image = ImageProcessor.add_image_watermark(
                        self.current_image,
                        image_path,
                        position=position,
                        opacity=opacity * 100,
                        scale=scale,
                        rotation=rotation
                    )
            else:
                QMessageBox.warning(self, "警告", "请选择水印类型")
                return
            
            # 更新当前图片
            self.current_image = watermarked_image
            
            # 更新预览
            self.update_preview()
            
            # 更新状态
            self.status_label.setText("已应用水印")
            
        except Exception as e:
            QMessageBox.critical(self, "错误", f"应用水印失败: {str(e)}")
    
    def update_preview(self):
        """
        更新预览图像
        """
        if not self.current_image:
            self.preview_label.setText("请打开一张图片")
            return
        
        try:
            # 将PIL图像转换为QPixmap
            image_rgb = self.current_image.convert('RGB')
            width, height = image_rgb.size
            image_data = image_rgb.tobytes()
            
            q_image = QImage(image_data, width, height, 3 * width, QImage.Format.Format_RGB888)
            pixmap = QPixmap.fromImage(q_image)
            
            # 调整预览大小以适应标签
            scaled_pixmap = pixmap.scaled(
                self.preview_label.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            
            self.preview_label.setPixmap(scaled_pixmap)
            
        except Exception as e:
            self.preview_label.setText(f"预览失败: {str(e)}")
    
    def update_image_info(self):
        """
        更新图片信息
        """
        if not self.current_image or not self.current_image_path:
            self.image_info_label.setText("未加载图片")
            return
        
        try:
            # 获取图片信息
            width, height = self.current_image.size
            format = self.current_image.format
            file_size = os.path.getsize(self.current_image_path) / 1024  # KB
            
            # 更新信息标签
            info_text = f"文件: {os.path.basename(self.current_image_path)} | 尺寸: {width}x{height} | 格式: {format} | 大小: {file_size:.2f} KB"
            self.image_info_label.setText(info_text)
            
        except Exception as e:
            self.image_info_label.setText(f"获取图片信息失败: {str(e)}")
    
    def save_current_template(self):
        """
        保存当前水印模板
        """
        try:
            # 提示用户输入模板名称
            template_name, ok = QInputDialog.getText(self, "保存模板", "请输入模板名称:")
            
            if ok and template_name:
                # 保存模板
                self.template_manager.save_template(template_name, self.current_watermark)
                
                # 显示成功消息
                QMessageBox.information(self, "成功", f"模板 '{template_name}' 已保存")
                
        except Exception as e:
            QMessageBox.critical(self, "错误", f"保存模板失败: {str(e)}")
    
    def load_template(self):
        """
        加载水印模板
        """
        try:
            # 获取可用模板列表
            templates = self.template_manager.list_templates()
            
            if not templates:
                QMessageBox.information(self, "提示", "没有可用的模板")
                return
            
            # 显示模板选择对话框
            template_name, ok = QInputDialog.getItem(self, "加载模板", "请选择模板:", templates, 0, False)
            
            if ok and template_name:
                # 加载模板
                watermark = self.template_manager.load_template(template_name)
                
                if watermark:
                    # 更新当前水印设置
                    self.current_watermark = watermark
                    
                    # 更新UI
                    self.update_watermark_ui()
                    
                    # 显示成功消息
                    QMessageBox.information(self, "成功", f"已加载模板 '{template_name}'")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"加载模板失败: {str(e)}")
    
    def update_watermark_ui(self):
        """
        更新水印设置UI
        """
        # TODO: 实现水印设置UI更新
        pass
    
    def clear_recent_files(self):
        """
        清除最近文件列表
        """
        self.config_manager.clear_recent_files()
        
        # 更新最近文件菜单
        # 找到"文件"菜单中的"最近文件"子菜单
        file_menu = self.menuBar().findChild(QMenu, "文件")
        if file_menu:
            recent_files_menu = file_menu.findChild(QMenu, "最近文件")
            if recent_files_menu:
                self.update_recent_files_menu(recent_files_menu)
    
    def show_about_dialog(self):
        """
        显示关于对话框
        """
        about_text = f"PhotoWatermark2 v{self.app_version}\n\n"
        about_text += "MacOS图片水印工具\n"
        about_text += "大语言模型辅助软件工程第二次作业\n\n"
        about_text += "支持文本水印和图片水印，提供丰富的水印设置选项。"
        
        QMessageBox.about(self, "关于", about_text)
    
    def resizeEvent(self, event):
        """
        窗口大小改变事件
        """
        super().resizeEvent(event)
        
        # 更新预览
        if self.current_image:
            self.update_preview()
    
    def closeEvent(self, event):
        """
        窗口关闭事件
        """
        # 保存配置
        self.save_config()
        
        # 接受关闭事件
        event.accept()
    
    def save_output_settings(self, settings=None):
        """
        保存输出设置
        """
        if settings is None:
            # 从UI控件获取设置
            settings = {
                'format': self.output_format_combo.currentText(),
                'quality': self.output_quality_slider.value(),
                'prefix': self.rename_prefix_edit.text(),
                'suffix': self.rename_suffix_edit.text(),
                'remember_dir': self.remember_output_dir_check.isChecked()
            }
        
        # 保存设置
        self.config_manager.save_output_settings(settings)
        
        # 显示成功消息
        QMessageBox.information(self, "成功", "输出设置已保存")
        
        return True
        
    def select_font(self):
        """
        选择字体
        """
        # 获取当前字体信息
        current_font_str = self.font_label.text()
        
        # 尝试从当前字体信息中解析字体名称和大小
        font_name = "Arial"
        font_size = 12
        
        try:
            parts = current_font_str.split(",")
            if len(parts) > 0:
                font_name = parts[0].strip()
            if len(parts) > 1:
                size_part = parts[1].strip()
                font_size = int(size_part.replace("pt", "").strip())
        except Exception:
            pass
        
        # 创建当前字体
        current_font = QFont(font_name, font_size)
        
        # 显示字体选择对话框
        font, ok = QFontDialog.getFont(
            current_font,
            self,
            "选择字体",
            QFontDialog.FontDialogOption.MonospacedFonts |
            QFontDialog.FontDialogOption.ScalableFonts
        )
        
        if ok:
            # 更新字体标签
            self.font_label.setText(f"{font.family()}, {font.pointSize()}pt")
    
    def select_color(self):
        """
        选择颜色
        """
        # 获取当前颜色
        current_color = QColor()
        style_sheet = self.color_preview.styleSheet()
        if style_sheet.startswith("background-color: "):
            color_str = style_sheet[len("background-color: "):]
            current_color.setNamedColor(color_str)
        
        # 显示颜色选择对话框
        color = QColorDialog.getColor(
            current_color,
            self,
            "选择颜色"
        )
        
        if color.isValid():
            # 更新颜色预览
            self.color_preview.setStyleSheet(f"background-color: {color.name()};")
    
    def select_watermark_image(self):
        """
        选择水印图片
        """
        # 获取支持的图片格式
        supported_formats = ImageProcessor.SUPPORTED_FORMATS
        
        # 构建文件过滤器 - 移除扩展名前的点号，因为SUPPORTED_FORMATS中已经包含了
        image_formats_str = " ".join([f"*{ext}" for ext in supported_formats])
        filter_str = f"图片文件 ({image_formats_str});;所有文件 (*)"
        
        # 记录日志
        info("打开水印图片选择对话框")
        
        # 打开文件对话框，设置初始目录为用户主目录，并使用Qt非原生对话框
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择水印图片", os.path.expanduser("~"), filter_str,
            options=QFileDialog.Option.DontUseNativeDialog
        )
        
        if file_path:
            # 更新水印图片路径
            self.watermark_image_path_edit.setText(file_path)
            info(f"选择水印图片: {file_path}")
        else:
            info("未选择任何水印图片")

# 添加QInputDialog导入，因为在save_current_template和load_template方法中使用了
from PyQt6.QtWidgets import QInputDialog, QLineEdit