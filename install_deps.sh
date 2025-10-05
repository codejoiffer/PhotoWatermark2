#!/bin/bash
# 激活虚拟环境
source venv/bin/activate
# 安装项目依赖
pip install -r requirements.txt
# 安装PyQt6（如果没有在requirements.txt中列出）
pip install PyQt6
# 检查安装结果
pip list