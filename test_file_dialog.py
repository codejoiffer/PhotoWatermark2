#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
from PyQt6.QtWidgets import QApplication, QFileDialog, QMessageBox

"""
文件对话框测试脚本
用于测试PyQt6的QFileDialog是否能正常工作
"""

if __name__ == "__main__":
    # 创建应用程序实例
    app = QApplication(sys.argv)
    
    # 打印测试信息
    print("开始测试文件对话框...")
    print(f"当前工作目录: {os.getcwd()}")
    print(f"用户主目录: {os.path.expanduser('~')}")
    
    # 测试1: 使用默认设置
    print("\n测试1: 使用默认设置的文件对话框")
    file_path, _ = QFileDialog.getOpenFileName(
        caption="测试1 - 打开图片",
        directory="",
        filter="图片文件 (*.jpg *.jpeg *.png *.bmp *.tiff *.tif);;所有文件 (*)"
    )
    print(f"测试1 - 选择的文件: {file_path if file_path else '未选择任何文件'}")
    
    # 测试2: 指定起始目录为用户主目录
    print("\n测试2: 指定起始目录为用户主目录的文件对话框")
    file_path, _ = QFileDialog.getOpenFileName(
        caption="测试2 - 打开图片",
        directory=os.path.expanduser("~"),
        filter="图片文件 (*.jpg *.jpeg *.png *.bmp *.tiff *.tif);;所有文件 (*)"
    )
    print(f"测试2 - 选择的文件: {file_path if file_path else '未选择任何文件'}")
    
    # 测试3: 使用Qt的非原生对话框
    print("\n测试3: 使用Qt非原生对话框")
    file_path, _ = QFileDialog.getOpenFileName(
        caption="测试3 - 打开图片",
        directory=os.path.expanduser("~"),
        filter="图片文件 (*.jpg *.jpeg *.png *.bmp *.tiff *.tif);;所有文件 (*)",
        options=QFileDialog.Option.DontUseNativeDialog
    )
    print(f"测试3 - 选择的文件: {file_path if file_path else '未选择任何文件'}")
    
    # 显示完成消息
    QMessageBox.information(None, "测试完成", "文件对话框测试已完成，请查看终端输出")
    
    # 退出应用程序
    sys.exit(0)