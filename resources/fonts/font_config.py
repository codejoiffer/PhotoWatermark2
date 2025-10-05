# 中文字体配置文件
# 此文件定义了程序将尝试加载的中文字体列表
# 字体将按顺序尝试加载，直到找到可用的字体

# 常见的中文字体列表
chinese_fonts = [
    # Windows 系统字体
    'SimHei',         # 黑体
    'Microsoft YaHei', # 微软雅黑
    'FangSong',       # 仿宋
    'KaiTi',          # 楷体
    'NSimSun',        # 新宋体
    
    # macOS 系统字体
    'Heiti TC',       # 黑体-繁
    'STHeiti',        # 华文黑体
    'STKaiti',        # 华文楷体
    'STSong',         # 华文宋体
    'PingFang SC',    # 苹方-简
    'Hiragino Sans GB', # 冬青黑体 GB
    
    # Linux 系统字体
    'WenQuanYi Micro Hei', # 文泉驿微米黑
    'WenQuanYi Zen Hei',   # 文泉驿正黑
    'Noto Sans SC',        # Noto Sans 简体中文
    'Noto Serif SC',       # Noto Serif 简体中文
    
    # 通用字体
    'Arial Unicode MS',    # 包含多种语言的 Arial
    'SimSun',              # 宋体
]

# 默认字体大小
default_font_size = 24

# 字体加载超时时间（秒）
font_load_timeout = 1.0