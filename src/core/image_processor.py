import os
import os
from PIL import Image, ImageDraw, ImageFont
import io
from src.utils.font_manager import font_manager
from src.utils.logger import info, warning, error

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
            info(f"开始加载图片: {file_path}")
            
            if not ImageProcessor.is_supported_format(file_path):
                warning(f"不支持的图片格式: {file_path}")
                raise ValueError(f"不支持的图片格式: {file_path}")
            
            image = Image.open(file_path)
            info(f"图片成功打开: {file_path}")
            
            # 确保图片模式包含alpha通道（如果是PNG）
            if image.mode == 'RGBA' or image.mode == 'LA':
                info(f"图片模式已包含alpha通道: {image.mode}")
                return image
            else:
                # 转换为RGBA以支持透明水印
                info(f"将图片从 {image.mode} 转换为 RGBA")
                return image.convert('RGBA')
        except Exception as e:
            error(f"加载图片失败: {str(e)}")
            raise Exception(f"加载图片失败: {str(e)}")
    
    @staticmethod
    def save_image(image, output_path, format=None, quality=95):
        """
        保存图片到指定路径
        """
        try:
            info(f"开始保存图片: {output_path}")
            
            if format is None:
                format = os.path.splitext(output_path)[1][1:].upper()
                if format == 'JPG':
                    format = 'JPEG'
                info(f"自动检测输出格式: {format}")
            else:
                info(f"指定输出格式: {format}")
            
            # 如果输出格式为JPEG，转换为RGB模式
            if format.upper() == 'JPEG':
                info("输出格式为JPEG，将图片转换为RGB模式")
                image = image.convert('RGB')
                image.save(output_path, format=format, quality=quality)
            else:
                image.save(output_path, format=format, quality=quality)
            
            info(f"图片保存成功: {output_path}, 质量: {quality}")
        except Exception as e:
            error(f"保存图片失败: {str(e)}")
            raise Exception(f"保存图片失败: {str(e)}")
    
    @staticmethod
    def _get_text_size(draw, text, font):
        """
        获取文本尺寸的兼容性方法
        兼容PIL/Pillow的新旧版本
        """
        try:
            # 尝试使用较新版本的方法
            if hasattr(draw, 'textbbox'):
                # 获取文本边界框 (left, top, right, bottom)
                bbox = draw.textbbox((0, 0), text, font=font)
                return bbox[2] - bbox[0], bbox[3] - bbox[1]
            elif hasattr(font, 'getbbox'):
                # 尝试使用字体的getbbox方法
                bbox = font.getbbox(text)
                return bbox[2] - bbox[0], bbox[3] - bbox[1]
            else:
                # 回退到旧版本的textsize方法
                return draw.textsize(text, font=font)
        except Exception:
            # 出现任何错误时，使用合理的默认值
            # 从字体中获取大小或使用默认值
            try:
                default_size = font.size if hasattr(font, 'size') else 20
                return default_size * len(text) // 2, default_size
            except:
                return 20 * len(text) // 2, 20
    
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
        font = font_manager.load_font(font_name, font_size)
        
        if font is None:
            warning("无法加载任何字体，使用默认字体")
            font = ImageFont.load_default()
        
        # 获取文本尺寸
        text_width, text_height = ImageProcessor._get_text_size(draw, text, font)
        
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
            info(f"开始添加图片水印: {watermark_path}")
            
            # 加载水印图片
            watermark = Image.open(watermark_path).convert('RGBA')
            info(f"水印图片加载成功: {watermark_path}")
            
            # 缩放水印
            if scale != 1.0:
                new_width = int(watermark.width * scale)
                new_height = int(watermark.height * scale)
                info(f"缩放水印: {watermark.width}x{watermark.height} -> {new_width}x{new_height}")
                watermark = watermark.resize((new_width, new_height), Image.LANCZOS)
            
            # 旋转水印
            if rotation != 0:
                info(f"旋转水印: {rotation}度")
                watermark = watermark.rotate(rotation, expand=True, resample=Image.BICUBIC)
            
            # 调整透明度
            if opacity != 100:
                info(f"调整水印透明度: {opacity}%")
                alpha = watermark.split()[3]
                alpha = alpha.point(lambda p: p * opacity / 100)
                watermark.putalpha(alpha)
            
            # 创建副本并粘贴水印
            watermark_image = image.copy()
            img_width, img_height = watermark_image.size
            wm_width, wm_height = watermark.size
            info(f"图片尺寸: {img_width}x{img_height}, 水印尺寸: {wm_width}x{wm_height}")
            
            # 计算位置
            # [位置计算代码保持不变]
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
            
            info(f"水印位置: {position} ({pos_x}, {pos_y})")
            
            # 粘贴水印
            watermark_image.paste(watermark, (pos_x, pos_y), watermark)
            info("图片水印添加完成")
            
            return watermark_image
        except Exception as e:
            error(f"添加图片水印失败: {str(e)}")
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
            font = font_manager.load_font(font_name, font_size)
            
            if font is None:
                warning("无法加载任何字体，使用默认字体")
                font = ImageFont.load_default()
            
            # 获取文本尺寸
            text_width, text_height = ImageProcessor._get_text_size(draw, text, font)
            
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
            info(f"调整图片大小: 当前尺寸 {img_width}x{img_height}")
            
            if percentage:
                # 按百分比缩放
                new_width = int(img_width * percentage / 100)
                new_height = int(img_height * percentage / 100)
                info(f"按百分比缩放: {percentage}% -> {new_width}x{new_height}")
            elif width and height:
                # 同时指定宽高
                new_width, new_height = width, height
                info(f"指定宽高: {new_width}x{new_height}")
            elif width:
                # 只指定宽度，保持比例
                ratio = width / img_width
                new_width = width
                new_height = int(img_height * ratio)
                info(f"按宽度缩放: {new_width}x{new_height}")
            elif height:
                # 只指定高度，保持比例
                ratio = height / img_height
                new_width = int(img_width * ratio)
                new_height = height
                info(f"按高度缩放: {new_width}x{new_height}")
            else:
                # 不调整大小
                info("不调整图片大小")
                return image.copy()
            
            # 调整大小
            resized_image = image.resize((new_width, new_height), Image.LANCZOS)
            info(f"图片大小调整完成: {new_width}x{new_height}")
            return resized_image
        except Exception as e:
            error(f"调整图片大小失败: {str(e)}")
            raise Exception(f"调整图片大小失败: {str(e)}")