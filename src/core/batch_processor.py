import os
import threading
import queue
import os
from core.image_processor import ImageProcessor
from core.watermark import Watermark

class BatchProcessor:
    """
    批量处理类，用于批量添加水印到多张图片
    """
    
    def __init__(self):
        self.is_processing = False
        self.cancel_flag = False
        self.progress_callback = None
        self.complete_callback = None
        self.error_callback = None
        self.thread = None
    
    def start_processing(self, image_paths, output_dir, watermark, 
                        output_format='PNG', quality=95, 
                        rename_prefix='', rename_suffix='', 
                        resize_width=None, resize_height=None, resize_percentage=None):
        """
        开始批量处理图片
        """
        if self.is_processing:
            raise RuntimeError("正在处理中，请等待当前任务完成")
        
        # 检查输出目录
        if not os.path.exists(output_dir):
            try:
                os.makedirs(output_dir)
            except Exception as e:
                raise Exception(f"创建输出目录失败: {str(e)}")
        
        # 检查是否有图片需要处理
        if not image_paths:
            raise ValueError("没有找到需要处理的图片")
        
        # 重置状态
        self.is_processing = True
        self.cancel_flag = False
        
        # 创建任务队列
        task_queue = queue.Queue()
        for image_path in image_paths:
            task_queue.put((image_path, output_dir, watermark, output_format, 
                          quality, rename_prefix, rename_suffix, 
                          resize_width, resize_height, resize_percentage))
        
        # 创建并启动线程
        self.thread = threading.Thread(
            target=self._process_queue,
            args=(task_queue, len(image_paths))
        )
        self.thread.daemon = True
        self.thread.start()
    
    def _process_queue(self, task_queue, total_tasks):
        """
        处理任务队列
        """
        processed_count = 0
        
        try:
            while not task_queue.empty() and not self.cancel_flag:
                # 获取任务
                (image_path, output_dir, watermark, output_format, 
                 quality, rename_prefix, rename_suffix, 
                 resize_width, resize_height, resize_percentage) = task_queue.get()
                
                try:
                    # 处理单张图片
                    self._process_single_image(
                        image_path,
                        output_dir,
                        watermark,
                        output_format,
                        quality,
                        rename_prefix,
                        rename_suffix,
                        resize_width,
                        resize_height,
                        resize_percentage
                    )
                    processed_count += 1
                    
                    # 调用进度回调
                    if self.progress_callback:
                        progress = int(processed_count / total_tasks * 100)
                        self.progress_callback(progress, image_path)
                        
                except Exception as e:
                    # 调用错误回调
                    if self.error_callback:
                        self.error_callback(str(e), image_path)
                        
                finally:
                    # 标记任务完成
                    task_queue.task_done()
            
        finally:
            # 处理完成或取消
            self.is_processing = False
            
            # 调用完成回调
            if self.complete_callback:
                result = {
                    'success': not self.cancel_flag,
                    'processed_count': processed_count,
                    'total_count': total_tasks,
                    'cancelled': self.cancel_flag
                }
                self.complete_callback(result)
    
    def _process_single_image(self, image_path, output_dir, watermark, 
                             output_format, quality, 
                             rename_prefix, rename_suffix, 
                             resize_width, resize_height, resize_percentage):
        """
        处理单张图片
        """
        # 加载图片
        image = ImageProcessor.load_image(image_path)
        
        # 应用水印
        watermarked_image = watermark.apply_watermark(image)
        
        # 调整图片大小（如果需要）
        if resize_width or resize_height or resize_percentage:
            watermarked_image = ImageProcessor.resize_image(
                watermarked_image,
                width=resize_width,
                height=resize_height,
                percentage=resize_percentage
            )
        
        # 生成输出文件名
        original_name = os.path.basename(image_path)
        name_without_ext, ext = os.path.splitext(original_name)
        
        # 根据输出格式设置扩展名
        if output_format.upper() == 'JPEG':
            output_ext = '.jpg'
        else:
            output_ext = '.png'
        
        # 应用重命名规则
        output_filename = f"{rename_prefix}{name_without_ext}{rename_suffix}{output_ext}"
        output_path = os.path.join(output_dir, output_filename)
        
        # 确保不会覆盖原文件
        original_dir = os.path.dirname(image_path)
        if os.path.normpath(output_dir) == os.path.normpath(original_dir):
            # 如果输出目录与原目录相同，添加额外的后缀
            base_name, ext = os.path.splitext(output_filename)
            output_filename = f"{base_name}_watermarked{ext}"
            output_path = os.path.join(output_dir, output_filename)
        
        # 保存图片
        ImageProcessor.save_image(watermarked_image, output_path, format=output_format, quality=quality)
    
    def cancel(self):
        """
        取消当前的批量处理任务
        """
        if self.is_processing and self.thread and self.thread.is_alive():
            self.cancel_flag = True
            # 等待线程结束
            self.thread.join(timeout=3.0)
            self.is_processing = False
    
    def set_callbacks(self, progress_callback=None, complete_callback=None, error_callback=None):
        """
        设置回调函数
        """
        self.progress_callback = progress_callback
        self.complete_callback = complete_callback
        self.error_callback = error_callback