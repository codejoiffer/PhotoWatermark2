#!/bin/bash
# 设置PYTHONPATH，确保能正确导入模块
export PYTHONPATH=$(pwd)
# 激活虚拟环境
source venv/bin/activate
# 从项目根目录直接运行主程序
python3 src/main.py