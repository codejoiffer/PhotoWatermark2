import os
import sys
import logging
import datetime
from logging.handlers import RotatingFileHandler


class Logger:
    """
    日志管理类，用于记录应用程序运行日志
    """
    
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not Logger._initialized:
            # 获取基础路径，支持PyInstaller打包
            base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            
            # 对于macOS应用程序，使用用户的Application Support目录存储日志
            if sys.platform == 'darwin':  # macOS
                app_support_dir = os.path.expanduser('~/Library/Application Support/PhotoWatermark2')
                self.log_dir = os.path.join(app_support_dir, 'logs')
            else:
                # 其他平台使用应用程序目录下的logs文件夹
                self.log_dir = os.path.join(base_path, 'logs')
            
            # 确保日志目录存在
            self._ensure_log_dir_exists()
            
            # 日志文件名（按日期）
            today = datetime.date.today().strftime('%Y-%m-%d')
            self.log_file = os.path.join(self.log_dir, f'photowatermark2_{today}.log')
            
            # 配置日志记录器
            self.logger = logging.getLogger('PhotoWatermark2')
            self.logger.setLevel(logging.DEBUG)
            
            # 避免重复添加处理器
            if not self.logger.handlers:
                # 创建文件处理器（支持日志轮转）
                file_handler = RotatingFileHandler(
                    self.log_file,
                    maxBytes=5 * 1024 * 1024,  # 5MB
                    backupCount=5,             # 保留5个备份
                    encoding='utf-8'
                )
                
                # 创建控制台处理器
                console_handler = logging.StreamHandler()
                
                # 设置日志格式
                formatter = logging.Formatter(
                    '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S'
                )
                
                file_handler.setFormatter(formatter)
                console_handler.setFormatter(formatter)
                
                # 添加处理器到日志记录器
                self.logger.addHandler(file_handler)
                self.logger.addHandler(console_handler)
            
            Logger._initialized = True
    
    def _ensure_log_dir_exists(self):
        """
        确保日志目录存在
        """
        if not os.path.exists(self.log_dir):
            try:
                os.makedirs(self.log_dir, exist_ok=True)
            except Exception as e:
                print(f"创建日志目录失败: {str(e)}")
    
    def debug(self, message):
        """
        记录调试信息
        """
        self.logger.debug(message)
    
    def info(self, message):
        """
        记录一般信息
        """
        self.logger.info(message)
    
    def warning(self, message):
        """
        记录警告信息
        """
        self.logger.warning(message)
    
    def error(self, message):
        """
        记录错误信息
        """
        self.logger.error(message)
    
    def critical(self, message):
        """
        记录严重错误信息
        """
        self.logger.critical(message)


# 创建全局日志实例
global_logger = Logger()


# 方便使用的函数
def debug(message):
    global_logger.debug(message)


def info(message):
    global_logger.info(message)


def warning(message):
    global_logger.warning(message)


def error(message):
    global_logger.error(message)


def critical(message):
    global_logger.critical(message)