#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试中文水印显示功能
此脚本用于验证程序是否能正确显示中文水印
"""

import os
import sys
from PIL import Image

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 导入所需模块
from src.core.image_processor import ImageProcessor
from src.core.watermark import Watermark
from src.utils.logger import info, warning, error


def test_chinese_text_watermark():
    """
    测试中文文本水印功能
    """
    try:
        info("开始测试中文文本水印")
        
        # 准备测试图片
        test_image_path = os.path.join(os.path.dirname(__file__), "lucky_pig.jpeg")
        if not os.path.exists(test_image_path):
            raise FileNotFoundError(f"测试图片不存在: {test_image_path}")
        
        # 加载图片
        image = Image.open(test_image_path).convert('RGBA')
        info(f"成功加载测试图片，尺寸: {image.size}")
        
        # 测试文本水印 - 使用ImageProcessor直接添加
        chinese_text = "中文水印测试"
        info(f"添加中文文本水印: {chinese_text}")
        
        # 测试不同位置的中文水印
        positions = ['top-left', 'top-center', 'top-right', 
                     'center-left', 'center', 'center-right',
                     'bottom-left', 'bottom-center', 'bottom-right']
        
        # 测试普通文本水印
        for position in positions:
            info(f"测试位置: {position}")
            watermarked_image = ImageProcessor.add_text_watermark(
                image, 
                chinese_text,
                position=position,
                font_size=36,
                font_color=(255, 0, 0, 128),  # 半透明红色
                rotation=0
            )
            
        # 测试使用Watermark类添加
        watermark = Watermark()
        watermark.set_text_watermark(
            text=chinese_text,
            font_size=48,
            font_color=(0, 0, 255, 128),  # 半透明蓝色
            opacity=50
        )
        watermark.set_position('center')
        watermark.set_rotation(30)
        watermark.set_style(has_shadow=True, has_stroke=True)
        
        final_watermarked_image = watermark.apply_watermark(image)
        
        # 测试平铺水印
        info("测试平铺中文水印")
        tiled_watermark_image = ImageProcessor.add_tiled_watermark(
            image,
            chinese_text,
            font_size=24,
            font_color=(0, 255, 0, 96),  # 半透明绿色
            rotation=45,
            spacing=50
        )
        
        # 保存结果
        output_dir = os.path.join(os.path.dirname(__file__), "test_results")
        os.makedirs(output_dir, exist_ok=True)
        
        # 保存最终结果
        final_output_path = os.path.join(output_dir, "chinese_watermark_result.png")
        final_watermarked_image.save(final_output_path)
        info(f"中文水印测试结果已保存到: {final_output_path}")
        
        # 保存平铺水印结果
        tiled_output_path = os.path.join(output_dir, "chinese_tiled_watermark_result.png")
        tiled_watermark_image.save(tiled_output_path)
        info(f"中文平铺水印测试结果已保存到: {tiled_output_path}")
        
        info("中文文本水印测试完成")
        return True
        
    except Exception as e:
        error(f"中文文本水印测试失败: {str(e)}")
        return False


def main():
    """
    主函数，运行所有测试
    """
    info("=== 中文水印显示测试开始 ===")
    
    # 运行中文文本水印测试
    text_watermark_result = test_chinese_text_watermark()
    
    if text_watermark_result:
        info("中文水印显示测试成功！")
        info("请查看test_results目录下的图片，确认中文水印是否正确显示。")
    else:
        error("中文水印显示测试失败！")
        
    info("=== 中文水印显示测试结束 ===")
    
    # 根据测试结果返回适当的退出码
    sys.exit(0 if text_watermark_result else 1)


if __name__ == "__main__":
    main()