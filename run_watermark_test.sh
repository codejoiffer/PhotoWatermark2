#!/bin/bash
# 激活虚拟环境
source venv/bin/activate
# 设置PYTHONPATH以包含项目根目录
export PYTHONPATH=$PYTHONPATH:$(pwd)
# 运行测试脚本
python3 test_chinese_watermark.py