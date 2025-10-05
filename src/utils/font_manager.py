import os
import sys
from PIL import ImageFont
import logging

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# 导入日志模块
from .logger import info, warning, error

class FontManager:
    """
    字体管理类，负责加载和管理字体资源
    提供加载系统字体和本地字体的功能
    """
    
    def __init__(self):
        # 字体缓存，避免重复加载
        self.font_cache = {}
        
        # 导入字体配置
        try:
            from resources.fonts.font_config import chinese_fonts
            self.chinese_fonts = chinese_fonts
        except Exception as e:
            warning(f"加载字体配置失败: {str(e)}")
            # 使用默认的中文字体列表
            self.chinese_fonts = [
                'SimHei', 'WenQuanYi Micro Hei', 'Heiti TC', 'Arial Unicode MS', 'Microsoft YaHei'
            ]
        
        # 本地字体目录
        self.local_font_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            'fonts'
        )
        info(f"本地字体目录: {self.local_font_dir}")
    
    def load_font(self, font_name=None, font_size=24):
        """
        加载指定的字体
        如果未指定字体或指定的字体加载失败，则尝试加载中文字体
        
        Args:
            font_name (str): 字体名称或字体文件路径
            font_size (int): 字体大小
        
        Returns:
            ImageFont.FreeTypeFont: 加载的字体对象
        """
        # 检查缓存
        cache_key = f"{font_name}_{font_size}"
        if cache_key in self.font_cache:
            info(f"从缓存加载字体: {font_name}, 大小: {font_size}")
            return self.font_cache[cache_key]
        
        font = None
        
        # 尝试加载指定的字体
        if font_name:
            try:
                # 检查是否为绝对路径
                if os.path.isabs(font_name) and os.path.exists(font_name):
                    font = ImageFont.truetype(font_name, font_size)
                    info(f"成功加载指定路径的字体: {font_name}")
                else:
                    # 尝试作为字体名称加载
                    font = ImageFont.truetype(font_name, font_size)
                    info(f"成功加载指定名称的字体: {font_name}")
            except Exception as e:
                warning(f"加载指定字体失败 '{font_name}': {str(e)}")
        
        # 如果指定字体加载失败，尝试加载中文字体
        if font is None:
            font = self._load_chinese_font(font_size)
        
        # 如果所有尝试都失败，使用默认字体
        if font is None:
            try:
                font = ImageFont.load_default()
                warning(f"加载默认字体")
            except Exception:
                error("所有字体加载尝试都失败")
                # 这是最后的后备方案，如果失败则会在使用时抛出异常
                font = None
        
        # 缓存字体
        if font:
            self.font_cache[cache_key] = font
        
        return font
    
    def _load_chinese_font(self, font_size=24):
        """
        尝试加载中文字体
        
        Args:
            font_size (int): 字体大小
        
        Returns:
            ImageFont.FreeTypeFont: 加载的中文字体对象
        """
        # 尝试加载本地字体目录中的字体
        local_font = self._load_local_font(font_size)
        if local_font:
            return local_font
        
        # 尝试加载系统中文字体
        info(f"开始尝试加载系统中文字体，共 {len(self.chinese_fonts)} 种")
        for font_name in self.chinese_fonts:
            try:
                font = ImageFont.truetype(font_name, font_size)
                info(f"成功加载中文字体: {font_name}")
                return font
            except Exception as e:
                warning(f"加载中文字体失败 '{font_name}': {str(e)}")
        
        error("所有中文字体加载尝试都失败")
        return None
    
    def _load_local_font(self, font_size=24):
        """
        尝试加载本地字体目录中的字体
        
        Args:
            font_size (int): 字体大小
        
        Returns:
            ImageFont.FreeTypeFont: 加载的本地字体对象
        """
        if not os.path.exists(self.local_font_dir):
            warning(f"本地字体目录不存在: {self.local_font_dir}")
            return None
        
        # 查找常见的中文字体文件扩展名
        font_extensions = ['.ttf', '.ttc', '.otf', '.woff', '.woff2']
        
        try:
            # 遍历字体目录中的文件
            for file in os.listdir(self.local_font_dir):
                file_path = os.path.join(self.local_font_dir, file)
                # 检查是否为文件以及扩展名是否为字体文件扩展名
                if os.path.isfile(file_path) and any(
                    file.lower().endswith(ext) for ext in font_extensions
                ):
                    try:
                        font = ImageFont.truetype(file_path, font_size)
                        info(f"成功加载本地字体: {file}")
                        return font
                    except Exception as e:
                        warning(f"加载本地字体失败 '{file}': {str(e)}")
        except Exception as e:
            warning(f"遍历本地字体目录失败: {str(e)}")
        
        return None
    
    def clear_cache(self):
        """
        清除字体缓存
        """
        self.font_cache.clear()
        info("字体缓存已清除")

# 创建全局的字体管理器实例
font_manager = FontManager()