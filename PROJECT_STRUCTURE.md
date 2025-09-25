# 项目结构说明

## 当前文件结构

```
/PhotoWatermark2/
├── PRD.md                 # 产品需求文档，详细描述产品功能和需求
├── README.md              # 项目说明文档，包含项目概述、功能特性、技术栈等信息
├── requirements.txt       # Python依赖库列表
└── PROJECT_STRUCTURE.md   # 项目结构说明文件
```

## 未来实现的文件结构（规划）

```
/PhotoWatermark2/
├── PRD.md                 # 产品需求文档
├── README.md              # 项目说明文档
├── requirements.txt       # Python依赖库列表
├── PROJECT_STRUCTURE.md   # 项目结构说明文件
├── src/                   # 源代码目录
│   ├── main.py            # 主程序入口
│   ├── ui/                # 界面相关代码
│   │   ├── main_window.py # 主窗口类
│   │   ├── image_list.py  # 图片列表控件
│   │   └── watermark_panel.py # 水印设置面板
│   ├── core/              # 核心功能实现
│   │   ├── image_processor.py # 图片处理核心类
│   │   ├── watermark.py   # 水印添加功能
│   │   └── batch_processor.py # 批量处理功能
│   └── utils/             # 工具类和辅助函数
│       ├── template_manager.py # 模板管理功能
│       └── config.py      # 配置管理
└── resources/             # 资源文件
    └── icons/             # 应用图标
```

## 目录说明

- **src/**：包含所有源代码，按功能模块组织
- **ui/**：界面相关代码，实现用户交互界面
- **core/**：核心功能实现，包含图片处理和水印添加的核心算法
- **utils/**：工具类和辅助函数，提供配置管理、模板管理等功能
- **resources/**：存放应用所需的资源文件，如图标等