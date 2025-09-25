#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试脚本 - 验证PhotoWatermark2的核心功能
"""

import os
import sys
import tempfile
import shutil

# 添加项目根目录到Python路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from core.image_processor import ImageProcessor
from core.watermark import Watermark
from utils.template_manager import TemplateManager
from utils.config import ConfigManager

class PhotoWatermarkTester:
    """测试类，用于验证PhotoWatermark2的核心功能"""
    
    def __init__(self):
        # 创建临时目录用于测试
        self.test_dir = tempfile.mkdtemp()
        self.temp_image_path = os.path.join(self.test_dir, "test_image.png")
        self.temp_watermark_path = os.path.join(self.test_dir, "test_watermark.png")
        self.output_dir = os.path.join(self.test_dir, "output")
        os.makedirs(self.output_dir, exist_ok=True)
        
        # 初始化管理器
        self.template_manager = TemplateManager()
        self.config_manager = ConfigManager()
        
        # 测试状态
        self.success_count = 0
        self.failure_count = 0
        
    def cleanup(self):
        """清理测试资源"""
        try:
            shutil.rmtree(self.test_dir)
        except Exception as e:
            print(f"清理测试资源失败: {str(e)}")
    
    def create_test_image(self):
        """创建测试图片"""
        try:
            from PIL import Image, ImageDraw
            
            # 创建一个简单的测试图片
            image = Image.new('RGBA', (500, 300), color='white')
            draw = ImageDraw.Draw(image)
            
            # 绘制一些简单内容
            draw.rectangle([(50, 50), (450, 250)], fill='lightblue', outline='blue', width=2)
            draw.text((100, 100), "测试图片", fill='black', font=None)
            
            # 保存测试图片
            image.save(self.temp_image_path)
            print(f"✓ 创建测试图片成功: {self.temp_image_path}")
            return True
        except Exception as e:
            print(f"✗ 创建测试图片失败: {str(e)}")
            return False
    
    def create_test_watermark_image(self):
        """创建测试水印图片"""
        try:
            from PIL import Image, ImageDraw
            
            # 创建一个简单的水印图片
            image = Image.new('RGBA', (100, 50), color=(255, 255, 255, 0))
            draw = ImageDraw.Draw(image)
            
            # 绘制水印内容
            draw.rectangle([(10, 10), (90, 40)], fill=(255, 0, 0, 128), outline='red', width=1)
            draw.text((15, 15), "水印", fill='black', font=None)
            
            # 保存水印图片
            image.save(self.temp_watermark_path)
            print(f"✓ 创建测试水印图片成功: {self.temp_watermark_path}")
            return True
        except Exception as e:
            print(f"✗ 创建测试水印图片失败: {str(e)}")
            return False
    
    def test_file_processing(self):
        """测试文件处理功能"""
        print("\n===== 测试文件处理功能 ====")
        
        try:
            # 测试加载图片
            image = ImageProcessor.load_image(self.temp_image_path)
            print(f"✓ 加载图片成功，尺寸: {image.size}")
            
            # 测试保存图片
            output_path = os.path.join(self.output_dir, "saved_image.png")
            ImageProcessor.save_image(image, output_path)
            print(f"✓ 保存图片成功: {output_path}")
            
            # 测试支持的格式
            supported_formats = ImageProcessor.SUPPORTED_FORMATS
            print(f"✓ 支持的图片格式: {supported_formats}")
            
            # 测试JPEG格式保存
            jpeg_output = os.path.join(self.output_dir, "saved_image.jpg")
            ImageProcessor.save_image(image, jpeg_output, format="JPEG", quality=80)
            print(f"✓ 保存为JPEG格式成功: {jpeg_output}")
            
            self.success_count += 4
            return True
        except Exception as e:
            print(f"✗ 文件处理功能测试失败: {str(e)}")
            self.failure_count += 1
            return False
    
    def test_text_watermark(self):
        """测试文本水印功能"""
        print("\n===== 测试文本水印功能 ====")
        
        try:
            # 加载测试图片
            image = ImageProcessor.load_image(self.temp_image_path)
            
            # 测试添加基本文本水印
            text_watermarked = ImageProcessor.add_text_watermark(
                image, 
                "测试水印", 
                position="center", 
                font_size=30,
                font_color=(255, 0, 0, 128)
            )
            text_output = os.path.join(self.output_dir, "text_watermark.png")
            ImageProcessor.save_image(text_watermarked, text_output)
            print(f"✓ 添加基本文本水印成功: {text_output}")
            
            # 测试旋转文本水印
            rotated_text_watermarked = ImageProcessor.add_text_watermark(
                image, 
                "旋转水印", 
                position="center", 
                font_size=30,
                font_color=(0, 0, 255, 128),
                rotation=45
            )
            rotated_text_output = os.path.join(self.output_dir, "rotated_text_watermark.png")
            ImageProcessor.save_image(rotated_text_watermarked, rotated_text_output)
            print(f"✓ 添加旋转文本水印成功: {rotated_text_output}")
            
            # 测试平铺文本水印
            tiled_text_watermarked = ImageProcessor.add_tiled_watermark(
                image, 
                "平铺水印", 
                font_size=20,
                font_color=(0, 128, 0, 64),
                rotation=-15,
                spacing=60
            )
            tiled_text_output = os.path.join(self.output_dir, "tiled_text_watermark.png")
            ImageProcessor.save_image(tiled_text_watermarked, tiled_text_output)
            print(f"✓ 添加平铺文本水印成功: {tiled_text_output}")
            
            self.success_count += 3
            return True
        except Exception as e:
            print(f"✗ 文本水印功能测试失败: {str(e)}")
            self.failure_count += 1
            return False
    
    def test_image_watermark(self):
        """测试图片水印功能"""
        print("\n===== 测试图片水印功能 ====")
        
        try:
            # 加载测试图片
            image = ImageProcessor.load_image(self.temp_image_path)
            
            # 测试添加基本图片水印
            image_watermarked = ImageProcessor.add_image_watermark(
                image, 
                self.temp_watermark_path, 
                position="center", 
                opacity=50,
                scale=2.0
            )
            image_output = os.path.join(self.output_dir, "image_watermark.png")
            ImageProcessor.save_image(image_watermarked, image_output)
            print(f"✓ 添加基本图片水印成功: {image_output}")
            
            # 测试旋转图片水印
            rotated_image_watermarked = ImageProcessor.add_image_watermark(
                image, 
                self.temp_watermark_path, 
                position="center", 
                opacity=50,
                scale=2.0,
                rotation=30
            )
            rotated_image_output = os.path.join(self.output_dir, "rotated_image_watermark.png")
            ImageProcessor.save_image(rotated_image_watermarked, rotated_image_output)
            print(f"✓ 添加旋转图片水印成功: {rotated_image_output}")
            
            # 测试平铺图片水印
            tiled_image_watermarked = ImageProcessor.add_tiled_image_watermark(
                image, 
                self.temp_watermark_path, 
                opacity=30,
                scale=0.8,
                rotation=0,
                spacing=120
            )
            tiled_image_output = os.path.join(self.output_dir, "tiled_image_watermark.png")
            ImageProcessor.save_image(tiled_image_watermarked, tiled_image_output)
            print(f"✓ 添加平铺图片水印成功: {tiled_image_output}")
            
            self.success_count += 3
            return True
        except Exception as e:
            print(f"✗ 图片水印功能测试失败: {str(e)}")
            self.failure_count += 1
            return False
    
    def test_watermark_class(self):
        """测试Watermark类功能"""
        print("\n===== 测试Watermark类功能 ====")
        
        try:
            # 加载测试图片
            image = ImageProcessor.load_image(self.temp_image_path)
            
            # 测试文本水印
            watermark = Watermark()
            watermark.set_text_watermark("Watermark类测试", font_size=28, opacity=70)
            watermark.set_position("bottom-right")
            watermark.set_rotation(15)
            watermark.set_style(has_shadow=True, has_stroke=True)
            
            # 应用水印
            watermarked = watermark.apply_watermark(image)
            watermark_output = os.path.join(self.output_dir, "watermark_class_test.png")
            ImageProcessor.save_image(watermarked, watermark_output)
            print(f"✓ Watermark类文本水印测试成功: {watermark_output}")
            
            # 测试字典转换功能
            watermark_dict = watermark.to_dict()
            print(f"✓ Watermark转换为字典成功: {watermark_dict}")
            
            # 从字典加载
            new_watermark = Watermark()
            new_watermark.from_dict(watermark_dict)
            print(f"✓ 从字典加载Watermark成功")
            
            self.success_count += 3
            return True
        except Exception as e:
            print(f"✗ Watermark类功能测试失败: {str(e)}")
            self.failure_count += 1
            return False
    
    def test_template_manager(self):
        """测试模板管理功能"""
        print("\n===== 测试模板管理功能 ====")
        
        try:
            # 创建一个水印对象
            watermark = Watermark()
            watermark.set_text_watermark("模板水印", font_size=36, opacity=60)
            watermark.set_position("center")
            
            # 保存模板
            template_name = "test_template"
            self.template_manager.save_template(template_name, watermark)
            print(f"✓ 保存模板成功: {template_name}")
            
            # 列出模板
            templates = self.template_manager.list_templates()
            print(f"✓ 列出模板成功: {templates}")
            
            # 加载模板 (返回元组: watermark, metadata)
            loaded_watermark, _ = self.template_manager.load_template(template_name)
            print(f"✓ 加载模板成功")
            
            # 验证加载的模板
            assert loaded_watermark.text == "模板水印"
            assert loaded_watermark.font_size == 36
            assert loaded_watermark.position == "center"
            print(f"✓ 模板内容验证成功")
            
            self.success_count += 4
            return True
        except Exception as e:
            print(f"✗ 模板管理功能测试失败: {str(e)}")
            self.failure_count += 1
            return False
    
    def test_config_manager(self):
        """测试配置管理功能"""
        print("\n===== 测试配置管理功能 ====")
        
        try:
            # 测试设置和获取配置
            test_config = {"test_key": "test_value", "test_number": 123}
            for key, value in test_config.items():
                self.config_manager.set(key, value)
                retrieved = self.config_manager.get(key)
                assert retrieved == value
                print(f"✓ 设置和获取配置项 '{key}' 成功")
            
            # 测试获取默认值
            default_value = self.config_manager.get("non_existent_key", "default")
            assert default_value == "default"
            print(f"✓ 获取默认值成功")
            
            # 测试保存和加载配置
            self.config_manager.save()
            print(f"✓ 保存配置成功")
            
            self.success_count += len(test_config) + 1
            return True
        except Exception as e:
            print(f"✗ 配置管理功能测试失败: {str(e)}")
            self.failure_count += 1
            return False
    
    def test_image_resize(self):
        """测试图片调整大小功能"""
        print("\n===== 测试图片调整大小功能 ====")
        
        try:
            # 加载测试图片
            image = ImageProcessor.load_image(self.temp_image_path)
            original_size = image.size
            print(f"原始图片尺寸: {original_size}")
            
            # 测试按百分比缩放
            resized_percent = ImageProcessor.resize_image(image, percentage=50)
            resized_size = resized_percent.size
            print(f"✓ 按百分比缩放成功: {resized_size}")
            
            # 测试按宽度缩放
            resized_width = ImageProcessor.resize_image(image, width=300)
            resized_size = resized_width.size
            print(f"✓ 按宽度缩放成功: {resized_size}")
            
            # 测试按高度缩放
            resized_height = ImageProcessor.resize_image(image, height=200)
            resized_size = resized_height.size
            print(f"✓ 按高度缩放成功: {resized_size}")
            
            # 保存测试结果
            percent_output = os.path.join(self.output_dir, "resized_percent.png")
            width_output = os.path.join(self.output_dir, "resized_width.png")
            height_output = os.path.join(self.output_dir, "resized_height.png")
            
            ImageProcessor.save_image(resized_percent, percent_output)
            ImageProcessor.save_image(resized_width, width_output)
            ImageProcessor.save_image(resized_height, height_output)
            
            self.success_count += 3
            return True
        except Exception as e:
            print(f"✗ 图片调整大小功能测试失败: {str(e)}")
            self.failure_count += 1
            return False
    
    def run_all_tests(self):
        """运行所有测试"""
        print("开始测试PhotoWatermark2核心功能...")
        print(f"测试目录: {self.test_dir}")
        
        # 创建测试图片
        if not self.create_test_image():
            print("无法创建测试图片，测试中止")
            self.cleanup()
            return False
        
        # 创建测试水印图片
        if not self.create_test_watermark_image():
            print("无法创建测试水印图片，部分测试可能失败")
        
        # 运行各项测试
        self.test_file_processing()
        self.test_text_watermark()
        self.test_image_watermark()
        self.test_watermark_class()
        self.test_template_manager()
        self.test_config_manager()
        self.test_image_resize()
        
        # 输出测试结果
        print("\n===== 测试结果摘要 =====")
        print(f"成功测试: {self.success_count}")
        print(f"失败测试: {self.failure_count}")
        
        # 计算通过率
        total_tests = self.success_count + self.failure_count
        if total_tests > 0:
            pass_rate = (self.success_count / total_tests) * 100
            print(f"通过率: {pass_rate:.1f}%")
        
        # 清理测试资源
        self.cleanup()
        
        return self.failure_count == 0

if __name__ == "__main__":
    tester = PhotoWatermarkTester()
    success = tester.run_all_tests()
    
    if success:
        print("\n✅ 所有核心功能测试通过！")
    else:
        print("\n❌ 部分功能测试失败，请查看详细信息。")
    
    # 根据测试结果设置退出码
    sys.exit(0 if success else 1)