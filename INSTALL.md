# PhotoWatermark2 安装指南

## 概述

本指南将帮助您在MacOS系统上安装和使用PhotoWatermark2应用程序。PhotoWatermark2支持两种安装方式：通过DMG安装包安装，或者从源代码运行。

## 系统要求

- MacOS 10.14 (Mojave) 或更高版本
- 至少4GB RAM
- 至少100MB可用磁盘空间
- 如果从源代码运行，需要Python 3.7或更高版本

## 方法一：使用DMG安装包（推荐）

### 安装步骤

1. 下载最新版本的PhotoWatermark2 DMG安装包
2. 双击DMG文件打开安装窗口
3. 将"PhotoWatermark2"应用程序图标拖拽到"应用程序"文件夹图标中
4. 等待复制完成后，您可以在"启动台"或"应用程序"文件夹中找到并启动PhotoWatermark2

### 卸载步骤

要卸载PhotoWatermark2，只需将"应用程序"文件夹中的"PhotoWatermark2.app"文件拖拽到废纸篓中。

> **注意**：这不会删除您的配置和模板数据，这些数据保存在`~/Library/Application Support/PhotoWatermark2/`文件夹中。如果您也想删除这些数据，请手动删除该文件夹。

## 方法二：从源代码运行

如果您需要自定义或修改应用程序，可以选择从源代码运行。

### 前提条件

- 安装Python 3.7或更高版本
  - 您可以从[Python官方网站](https://www.python.org/downloads/mac-osx/)下载并安装
  - 或者使用Homebrew安装：`brew install python`
- 安装Git（可选，用于克隆代码仓库）
  - 使用Homebrew安装：`brew install git`

### 安装步骤

1. **克隆代码仓库**（如果您已经有代码，可以跳过此步骤）
   ```bash
   git clone https://github.com/photowatermark/PhotoWatermark2.git
   cd PhotoWatermark2
   ```

2. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

3. **运行应用程序**
   ```bash
   # 方法一：使用启动脚本
   ./run_app.sh
   
   # 方法二：直接运行
   python src/main.py
   ```

## 如何创建自己的DMG安装包

如果您对代码进行了修改，并希望创建自己的DMG安装包，可以按照以下步骤操作：

1. 确保已安装构建依赖
   ```bash
   pip install pyinstaller
   ```

2. 确保已安装create-dmg工具（用于创建DMG安装包）
   ```bash
   # 使用Homebrew安装
   brew install create-dmg
   ```

3. 运行构建脚本
   ```bash
   ./build_dmg.sh
   ```

4. 构建完成后，您可以在`dist`目录中找到生成的DMG安装包

## 配置和模板数据

PhotoWatermark2的配置和模板数据保存在以下位置：

```
~/Library/Application Support/PhotoWatermark2/
```

此目录包含：
- `config.json`：应用程序配置文件
- `last_session.json`：上次会话的状态信息
- `templates/`：保存的水印模板

即使您卸载并重新安装应用程序，这些数据也会被保留，确保您的设置和模板在升级后仍然可用。

## 故障排除

### 应用程序无法启动

- 检查您的MacOS版本是否满足要求（10.14或更高版本）
- 如果从源代码运行，确保已安装所有依赖：`pip install -r requirements.txt`
- 如果使用DMG安装包，尝试重新下载并安装

### 中文字体显示问题

- 确保您的系统已安装中文字体
- 应用程序会自动尝试加载系统中可用的中文字体，包括SimHei、WenQuanYi Micro Hei、Heiti TC等

### 图片加载失败

- 检查图片文件格式是否受支持（支持的格式：.jpg、.jpeg、.png、.bmp、.tiff、.tif等）
- 确保您有足够的磁盘空间和内存

## 联系与支持

如有任何问题或建议，请随时联系开发团队。