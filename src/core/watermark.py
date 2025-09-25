import os
from PIL import Image, ImageDraw, ImageFont
import io
from core.image_processor import ImageProcessor
import json
class Watermark:
    """
    水印处理类，提供文本水印和图片水印的添加功能
    """
    
    def __init__(self):
        # 默认水印配置
        self.watermark_type = 'text'  # 'text' 或 'image'
        self.text = "Watermark"
        self.font_name = None
        self.font_size = 24
        self.font_color = (255, 255, 255, 128)  # RGBA，默认半透明白色
        self.watermark_path = None
        self.opacity = 50  # 水印透明度，0-100
        self.position = 'bottom-right'  # 预设位置或坐标元组
        self.rotation = 0  # 旋转角度
        self.scale = 1.0  # 图片水印缩放比例
        self.has_shadow = False  # 是否添加阴影
        self.has_stroke = False  # 是否添加描边
        
    def set_text_watermark(self, text, font_name=None, font_size=24, 
                          font_color=(255, 255, 255, 128), opacity=50):
        """
        设置文本水印参数
        """
        self.watermark_type = 'text'
        self.text = text
        self.font_name = font_name
        self.font_size = font_size
        # 调整颜色的透明度
        if len(font_color) == 3:
            # 如果没有透明度通道，添加透明度
            self.font_color = font_color + (int(255 * opacity / 100),)
        else:
            # 如果有透明度通道，使用指定的透明度
            self.font_color = font_color[:3] + (int(255 * opacity / 100),)
        self.opacity = opacity
    
    def set_image_watermark(self, watermark_path, opacity=50, scale=1.0):
        """
        设置图片水印参数
        """
        if not os.path.exists(watermark_path):
            raise FileNotFoundError(f"水印图片文件不存在: {watermark_path}")
        
        self.watermark_type = 'image'
        self.watermark_path = watermark_path
        self.opacity = opacity
        self.scale = scale
    
    def set_position(self, position):
        """
        设置水印位置
        """
        self.position = position
    
    def set_rotation(self, rotation):
        """
        设置水印旋转角度
        """
        self.rotation = rotation
    
    def set_style(self, has_shadow=False, has_stroke=False):
        """
        设置水印样式
        """
        self.has_shadow = has_shadow
        self.has_stroke = has_stroke
    
    def apply_watermark(self, image):
        """
        应用水印到图片
        """
        if self.watermark_type == 'text':
            return self._apply_text_watermark(image)
        elif self.watermark_type == 'image':
            return self._apply_image_watermark(image)
        else:
            raise ValueError(f"不支持的水印类型: {self.watermark_type}")
    
    def _apply_text_watermark(self, image):
        """
        应用文本水印
        """
        # 创建一个可绘制的副本
        watermark_image = image.copy()
        draw = ImageDraw.Draw(watermark_image, 'RGBA')
        
        # 加载字体
        try:
            if self.font_name:
                font = ImageFont.truetype(self.font_name, self.font_size)
            else:
                # 使用默认字体
                font = ImageFont.load_default()
        except Exception:
            # 如果指定字体加载失败，使用默认字体
            font = ImageFont.load_default()
        
        # 获取文本尺寸
        text_width, text_height = self._get_text_size(draw, self.text, font)
        
        # 创建文本图像
        text_img = Image.new('RGBA', (text_width + 20, text_height + 20), (255, 255, 255, 0))
        text_draw = ImageDraw.Draw(text_img)
        
        # 计算文本在图像中的位置
        text_x, text_y = 10, 10
        
        # 如果需要添加阴影或描边
        if self.has_stroke:
            # 添加描边
            stroke_width = 2
            stroke_color = (0, 0, 0, self.font_color[3] // 2)  # 半透明黑色
            text_draw.text((text_x - stroke_width, text_y), self.text, font=font, fill=stroke_color)
            text_draw.text((text_x + stroke_width, text_y), self.text, font=font, fill=stroke_color)
            text_draw.text((text_x, text_y - stroke_width), self.text, font=font, fill=stroke_color)
            text_draw.text((text_x, text_y + stroke_width), self.text, font=font, fill=stroke_color)
            text_draw.text((text_x - stroke_width, text_y - stroke_width), self.text, font=font, fill=stroke_color)
            text_draw.text((text_x + stroke_width, text_y - stroke_width), self.text, font=font, fill=stroke_color)
            text_draw.text((text_x - stroke_width, text_y + stroke_width), self.text, font=font, fill=stroke_color)
            text_draw.text((text_x + stroke_width, text_y + stroke_width), self.text, font=font, fill=stroke_color)
        
        if self.has_shadow:
            # 添加阴影
            shadow_offset = 2
            shadow_color = (0, 0, 0, self.font_color[3] // 2)  # 半透明黑色
            text_draw.text((text_x + shadow_offset, text_y + shadow_offset), self.text, font=font, fill=shadow_color)
        
        # 添加主文本
        text_draw.text((text_x, text_y), self.text, font=font, fill=self.font_color)
        
        # 旋转文本
        if self.rotation != 0:
            text_img = text_img.rotate(self.rotation, expand=True, resample=Image.BICUBIC)
        
        # 计算最终位置
        img_width, img_height = watermark_image.size
        wm_width, wm_height = text_img.size
        
        pos_x, pos_y = self._calculate_position(img_width, img_height, wm_width, wm_height)
        
        # 粘贴水印
        watermark_image.paste(text_img, (pos_x, pos_y), text_img)
        
        return watermark_image
    
    def _apply_image_watermark(self, image):
        """
        应用图片水印
        """
        # 使用ImageProcessor的方法添加图片水印
        return ImageProcessor.add_image_watermark(
            image,
            self.watermark_path,
            self.position,
            self.opacity,
            self.scale,
            self.rotation
        )
    
    def _calculate_position(self, img_width, img_height, wm_width, wm_height):
        """
        计算水印位置
        """
        if isinstance(self.position, tuple):
            # 使用指定的绝对位置
            return self.position
        else:
            # 使用预设位置
            margin = 10
            if self.position == 'top-left':
                return margin, margin
            elif self.position == 'top-center':
                return (img_width - wm_width) // 2, margin
            elif self.position == 'top-right':
                return img_width - wm_width - margin, margin
            elif self.position == 'center-left':
                return margin, (img_height - wm_height) // 2
            elif self.position == 'center':
                return (img_width - wm_width) // 2, (img_height - wm_height) // 2
            elif self.position == 'center-right':
                return img_width - wm_width - margin, (img_height - wm_height) // 2
            elif self.position == 'bottom-left':
                return margin, img_height - wm_height - margin
            elif self.position == 'bottom-center':
                return (img_width - wm_width) // 2, img_height - wm_height - margin
            elif self.position == 'bottom-right':
                return img_width - wm_width - margin, img_height - wm_height - margin
            else:
                # 默认右下角
                return img_width - wm_width - margin, img_height - wm_height - margin
    
    def _get_text_size(self, draw, text, font):
        """
        获取文本尺寸
        兼容PIL的不同版本
        """
        try:
            # 对于较新版本的PIL
            bbox = draw.textbbox((0, 0), text, font=font)
            return bbox[2] - bbox[0], bbox[3] - bbox[1]
        except AttributeError:
            # 对于较旧版本的PIL
            return draw.textsize(text, font=font)
    
    def to_dict(self):
        """
        将水印配置转换为字典
        用于保存为模板
        """
        return {
            'watermark_type': self.watermark_type,
            'text': self.text,
            'font_name': self.font_name,
            'font_size': self.font_size,
            'font_color': self.font_color,
            'watermark_path': self.watermark_path,
            'opacity': self.opacity,
            'position': self.position,
            'rotation': self.rotation,
            'scale': self.scale,
            'has_shadow': self.has_shadow,
            'has_stroke': self.has_stroke
        }
    
    def from_dict(self, config_dict):
        """
        从字典加载水印配置
        用于加载模板
        """
        for key, value in config_dict.items():
            if hasattr(self, key):
                setattr(self, key, value)