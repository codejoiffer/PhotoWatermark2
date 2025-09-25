import os
from PIL import Image, ImageDraw, ImageFont
import io
import os

class ImageProcessor:
    """
    图片处理核心类，提供图片读取、写入和水印添加等功能
    """
    
    SUPPORTED_FORMATS = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif']
    
    @staticmethod
    def is_supported_format(file_path):
        """
        检查文件是否为支持的图片格式
        """
        ext = os.path.splitext(file_path)[1].lower()
        return ext in ImageProcessor.SUPPORTED_FORMATS
    
    @staticmethod
    def load_image(file_path):
        """
        加载图片文件
        """
        try:
            if not ImageProcessor.is_supported_format(file_path):
                raise ValueError(f"不支持的图片格式: {file_path}")
            
            image = Image.open(file_path)
            # 确保图片模式包含alpha通道（如果是PNG）
            if image.mode == 'RGBA' or image.mode == 'LA':
                return image
            else:
                # 转换为RGBA以支持透明水印
                return image.convert('RGBA')
        except Exception as e:
            raise Exception(f"加载图片失败: {str(e)}")
    
    @staticmethod
    def save_image(image, output_path, format=None, quality=95):
        """
        保存图片到指定路径
        """
        try:
            if format is None:
                format = os.path.splitext(output_path)[1][1:].upper()
                if format == 'JPG':
                    format = 'JPEG'
            
            # 如果输出格式为JPEG，转换为RGB模式
            if format.upper() == 'JPEG':
                image = image.convert('RGB')
                image.save(output_path, format=format, quality=quality)
            else:
                image.save(output_path, format=format, quality=quality)
        except Exception as e:
            raise Exception(f"保存图片失败: {str(e)}")
    
    @staticmethod
    def add_text_watermark(image, text, position, font_name=None, font_size=20, 
                          font_color=(255, 255, 255, 128), rotation=0):
        """
        添加文本水印
        """
        # 创建一个可绘制的副本
        watermark_image = image.copy()
        draw = ImageDraw.Draw(watermark_image, 'RGBA')
        
        # 加载字体
        try:
            if font_name:
                font = ImageFont.truetype(font_name, font_size)
            else:
                # 使用默认字体
                font = ImageFont.load_default()
        except Exception:
            # 如果指定字体加载失败，使用默认字体
            font = ImageFont.load_default()
        
        # 获取文本尺寸
        text_width, text_height = draw.textsize(text, font=font)
        
        # 计算水印位置
        img_width, img_height = watermark_image.size
        
        # 创建文本图像
        text_img = Image.new('RGBA', (text_width, text_height), (255, 255, 255, 0))
        text_draw = ImageDraw.Draw(text_img)
        text_draw.text((0, 0), text, font=font, fill=font_color)
        
        # 旋转文本
        if rotation != 0:
            text_img = text_img.rotate(rotation, expand=True)
        
        # 计算最终位置
        text_width, text_height = text_img.size
        
        if isinstance(position, tuple):
            # 使用指定的绝对位置
            pos_x, pos_y = position
        else:
            # 使用预设位置
            if position == 'top-left':
                pos_x, pos_y = 10, 10
            elif position == 'top-center':
                pos_x, pos_y = (img_width - text_width) // 2, 10
            elif position == 'top-right':
                pos_x, pos_y = img_width - text_width - 10, 10
            elif position == 'center-left':
                pos_x, pos_y = 10, (img_height - text_height) // 2
            elif position == 'center':
                pos_x, pos_y = (img_width - text_width) // 2, (img_height - text_height) // 2
            elif position == 'center-right':
                pos_x, pos_y = img_width - text_width - 10, (img_height - text_height) // 2
            elif position == 'bottom-left':
                pos_x, pos_y = 10, img_height - text_height - 10
            elif position == 'bottom-center':
                pos_x, pos_y = (img_width - text_width) // 2, img_height - text_height - 10
            elif position == 'bottom-right':
                pos_x, pos_y = img_width - text_width - 10, img_height - text_height - 10
            else:
                # 默认右下角
                pos_x, pos_y = img_width - text_width - 10, img_height - text_height - 10
        
        # 粘贴水印
        watermark_image.paste(text_img, (pos_x, pos_y), text_img)
        
        return watermark_image
    
    @staticmethod
    def add_image_watermark(image, watermark_path, position, opacity=50, scale=1.0, rotation=0):
        """
        添加图片水印
        """
        try:
            # 加载水印图片
            watermark = Image.open(watermark_path).convert('RGBA')
            
            # 缩放水印
            if scale != 1.0:
                new_width = int(watermark.width * scale)
                new_height = int(watermark.height * scale)
                watermark = watermark.resize((new_width, new_height), Image.LANCZOS)
            
            # 旋转水印
            if rotation != 0:
                watermark = watermark.rotate(rotation, expand=True, resample=Image.BICUBIC)
            
            # 调整透明度
            if opacity != 100:
                alpha = watermark.split()[3]
                alpha = alpha.point(lambda p: p * opacity / 100)
                watermark.putalpha(alpha)
            
            # 创建副本并粘贴水印
            watermark_image = image.copy()
            img_width, img_height = watermark_image.size
            wm_width, wm_height = watermark.size
            
            # 计算位置
            if isinstance(position, tuple):
                pos_x, pos_y = position
            else:
                if position == 'top-left':
                    pos_x, pos_y = 10, 10
                elif position == 'top-center':
                    pos_x, pos_y = (img_width - wm_width) // 2, 10
                elif position == 'top-right':
                    pos_x, pos_y = img_width - wm_width - 10, 10
                elif position == 'center-left':
                    pos_x, pos_y = 10, (img_height - wm_height) // 2
                elif position == 'center':
                    pos_x, pos_y = (img_width - wm_width) // 2, (img_height - wm_height) // 2
                elif position == 'center-right':
                    pos_x, pos_y = img_width - wm_width - 10, (img_height - wm_height) // 2
                elif position == 'bottom-left':
                    pos_x, pos_y = 10, img_height - wm_height - 10
                elif position == 'bottom-center':
                    pos_x, pos_y = (img_width - wm_width) // 2, img_height - wm_height - 10
                elif position == 'bottom-right':
                    pos_x, pos_y = img_width - wm_width - 10, img_height - wm_height - 10
                else:
                    # 默认右下角
                    pos_x, pos_y = img_width - wm_width - 10, img_height - wm_height - 10
            
            # 粘贴水印
            watermark_image.paste(watermark, (pos_x, pos_y), watermark)
            
            return watermark_image
        except Exception as e:
            raise Exception(f"添加图片水印失败: {str(e)}")
    
    @staticmethod
    def add_tiled_watermark(image, text, font_name=None, font_size=20,
                           font_color=(255, 255, 255, 128), rotation=0,
                           spacing=50):
        """
        添加平铺文本水印
        """
        try:
            # 创建一个可绘制的副本
            watermark_image = image.copy()
            draw = ImageDraw.Draw(watermark_image, 'RGBA')
            
            # 加载字体
            try:
                if font_name:
                    font = ImageFont.truetype(font_name, font_size)
                else:
                    # 使用默认字体
                    font = ImageFont.load_default()
            except Exception:
                # 如果指定字体加载失败，使用默认字体
                font = ImageFont.load_default()
            
            # 获取文本尺寸
            text_width, text_height = draw.textsize(text, font=font)
            
            # 创建文本图像
            text_img = Image.new('RGBA', (text_width, text_height), (255, 255, 255, 0))
            text_draw = ImageDraw.Draw(text_img)
            text_draw.text((0, 0), text, font=font, fill=font_color)
            
            # 旋转文本
            if rotation != 0:
                text_img = text_img.rotate(rotation, expand=True)
            
            # 平铺水印
            img_width, img_height = watermark_image.size
            wm_width, wm_height = text_img.size
            
            # 计算每行每列可以放置的水印数量
            # 考虑间距
            step_x = wm_width + spacing
            step_y = wm_height + spacing
            
            # 平铺水印
            for x in range(0, img_width, step_x):
                for y in range(0, img_height, step_y):
                    # 计算实际位置
                    pos_x = x
                    pos_y = y
                    
                    # 粘贴水印
                    watermark_image.paste(text_img, (pos_x, pos_y), text_img)
            
            return watermark_image
        except Exception as e:
            raise Exception(f"添加平铺水印失败: {str(e)}")
    
    @staticmethod
    def add_tiled_image_watermark(image, watermark_path, opacity=50, scale=1.0,
                                 rotation=0, spacing=50):
        """
        添加平铺图片水印
        """
        try:
            # 加载水印图片
            watermark = Image.open(watermark_path).convert('RGBA')
            
            # 缩放水印
            if scale != 1.0:
                new_width = int(watermark.width * scale)
                new_height = int(watermark.height * scale)
                watermark = watermark.resize((new_width, new_height), Image.LANCZOS)
            
            # 旋转水印
            if rotation != 0:
                watermark = watermark.rotate(rotation, expand=True, resample=Image.BICUBIC)
            
            # 调整透明度
            if opacity != 100:
                alpha = watermark.split()[3]
                alpha = alpha.point(lambda p: p * opacity / 100)
                watermark.putalpha(alpha)
            
            # 创建副本并平铺水印
            watermark_image = image.copy()
            img_width, img_height = watermark_image.size
            wm_width, wm_height = watermark.size
            
            # 计算每行每列可以放置的水印数量
            # 考虑间距
            step_x = wm_width + spacing
            step_y = wm_height + spacing
            
            # 平铺水印
            for x in range(0, img_width, step_x):
                for y in range(0, img_height, step_y):
                    # 粘贴水印
                    watermark_image.paste(watermark, (x, y), watermark)
            
            return watermark_image
        except Exception as e:
            raise Exception(f"添加平铺图片水印失败: {str(e)}")
    
    @staticmethod
    def resize_image(image, width=None, height=None, percentage=None):
        """
        调整图片大小
        """
        try:
            img_width, img_height = image.size
            
            if percentage:
                # 按百分比缩放
                new_width = int(img_width * percentage / 100)
                new_height = int(img_height * percentage / 100)
            elif width and height:
                # 同时指定宽高
                new_width, new_height = width, height
            elif width:
                # 只指定宽度，保持比例
                ratio = width / img_width
                new_width = width
                new_height = int(img_height * ratio)
            elif height:
                # 只指定高度，保持比例
                ratio = height / img_height
                new_width = int(img_width * ratio)
                new_height = height
            else:
                # 不调整大小
                return image.copy()
            
            # 调整大小
            resized_image = image.resize((new_width, new_height), Image.LANCZOS)
            return resized_image
        except Exception as e:
            raise Exception(f"调整图片大小失败: {str(e)}")