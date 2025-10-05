#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
字体检查脚本
用于验证系统中是否安装了中文字体，以及FontManager是否能正确加载这些字体
"""

import os
import sys
from PIL import ImageFont

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 导入FontManager和logger
from src.utils.font_manager import FontManager
from src.utils.logger import info, warning, error


font_manager = FontManager()


def list_system_fonts():
    """
    列出系统中可用的字体
    """
    info("=== 系统字体检查 ===")
    
    # 常见中文字体列表
    chinese_fonts = [
        'SimHei', 'WenQuanYi Micro Hei', 'Heiti TC', 
        'Arial Unicode MS', 'Microsoft YaHei', 'PingFang SC',
        'Hiragino Sans GB', 'Noto Sans SC', 'Source Han Sans CN'
    ]
    
    # 测试加载每种字体
    found_fonts = []
    for font_name in chinese_fonts:
        try:
            # 尝试以32号大小加载字体
            font = ImageFont.truetype(font_name, 32)
            found_fonts.append(font_name)
            info(f"✓ 成功加载字体: {font_name}")
        except Exception as e:
            warning(f"✗ 无法加载字体: {font_name} - 错误: {str(e)}")
    
    if found_fonts:
        info(f"找到 {len(found_fonts)} 种中文字体")
    else:
        warning("没有找到中文字体，请安装中文字体包")
    
    return found_fonts


def test_font_manager():
    """
    测试FontManager的字体加载功能
    """
    info("=== FontManager测试 ===")
    
    # 测试加载默认字体
    info("测试加载默认字体...")
    default_font = font_manager.load_font(None, 32)
    if default_font:
        info("✓ 成功加载默认字体")
    else:
        error("✗ 无法加载默认字体")
    
    # 测试加载指定字体
    info("测试加载指定字体'SimHei'...")
    simhei_font = font_manager.load_font('SimHei', 32)
    if simhei_font:
        info("✓ 成功加载字体'SimHei'")
    else:
        warning("✗ 无法加载字体'SimHei'")
    
    # 测试加载Microsoft YaHei
    info("测试加载字体'Microsoft YaHei'...")
    msyh_font = font_manager.load_font('Microsoft YaHei', 32)
    if msyh_font:
        info("✓ 成功加载字体'Microsoft YaHei'")
    else:
        warning("✗ 无法加载字体'Microsoft YaHei'")
    
    # 测试加载PingFang SC (macOS特有字体)
    info("测试加载字体'PingFang SC'...")
    pingfang_font = font_manager.load_font('PingFang SC', 32)
    if pingfang_font:
        info("✓ 成功加载字体'PingFang SC'")
    else:
        warning("✗ 无法加载字体'PingFang SC'")
    
    # 显示FontManager内部状态
    info(f"FontManager缓存状态: 已缓存 {len(font_manager.font_cache)} 种字体")
    info(f"本地字体目录: {font_manager.local_font_dir}")
    if os.path.exists(font_manager.local_font_dir):
        local_fonts = os.listdir(font_manager.local_font_dir)
        info(f"本地字体文件数量: {len(local_fonts)}")
        if local_fonts:
            info(f"本地字体文件: {', '.join(local_fonts)}")
    else:
        warning(f"本地字体目录不存在: {font_manager.local_font_dir}")


def check_fonts_dir():
    """
    检查字体目录是否存在并正确设置
    """
    info("=== 字体目录检查 ===")
    
    # 检查resources/fonts目录
    fonts_dir = os.path.join(os.path.dirname(__file__), "resources", "fonts")
    if os.path.exists(fonts_dir):
        info(f"字体目录存在: {fonts_dir}")
        # 确保目录可写
        if os.access(fonts_dir, os.W_OK):
            info("字体目录可写")
        else:
            warning("警告: 字体目录不可写，可能无法添加新字体")
        
        # 检查目录中的字体文件
        font_files = [f for f in os.listdir(fonts_dir) 
                     if f.lower().endswith(('.ttf', '.otf', '.ttc'))]
        if font_files:
            info(f"找到 {len(font_files)} 个字体文件")
            for font_file in font_files:
                info(f"- {font_file}")
        else:
            info("字体目录为空，可以添加.ttf或.otf格式的中文字体文件")
            info("推荐添加的中文字体: SimHei, WenQuanYi Micro Hei, Microsoft YaHei等")
    else:
        error(f"字体目录不存在: {fonts_dir}")
        info("请创建字体目录并添加中文字体文件")


def main():
    """
    主函数，运行所有字体检查
    """
    info("=== 字体检查脚本开始运行 ===")
    
    # 检查字体目录
    check_fonts_dir()
    
    # 列出系统中可用的字体
    found_fonts = list_system_fonts()
    
    # 测试FontManager
    test_font_manager()
    
    # 如果没有找到任何中文字体，提供解决方案
    if not found_fonts:
        error("未找到任何中文字体，这可能是中文水印显示问题的原因")
        info("解决方案:")
        info("1. 在macOS上，您可以从App Store安装中文字体包")
        info("2. 或者直接将.ttf格式的中文字体文件放入resources/fonts目录")
        info("3. 常见的免费中文字体下载来源包括Google Fonts、Adobe Fonts等")
    else:
        info("=== 字体检查完成，系统至少有一个可用的中文字体 ===")
        info("中文水印应该能够正常显示")
    
    info("=== 字体检查脚本运行结束 ===")
    
    # 根据是否找到字体返回适当的退出码
    sys.exit(0 if found_fonts else 1)


if __name__ == "__main__":
    main()