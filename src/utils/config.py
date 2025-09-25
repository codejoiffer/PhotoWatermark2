import os
import json
import datetime

class ConfigManager:
    """
    配置管理类，用于保存和加载应用程序配置
    """
    
    def __init__(self, config_dir=None):
        # 获取用户目录
        user_home = os.path.expanduser('~')
        # 默认配置保存目录
        self.default_config_dir = os.path.join(
            user_home, 'Library', 'Application Support', 'PhotoWatermark2'
        )
        
        # 使用指定目录或默认目录
        self.config_dir = config_dir or self.default_config_dir
        
        # 配置文件名
        self.config_filename = 'config.json'
        self.last_session_filename = 'last_session.json'
        
        # 配置文件路径
        self.config_path = os.path.join(self.config_dir, self.config_filename)
        self.last_session_path = os.path.join(self.config_dir, self.last_session_filename)
        
        # 确保配置目录存在
        self._ensure_config_dir_exists()
        
        # 默认配置
        self.default_config = {
            'app_version': '1.0.0',
            'last_update_check': '',
            'output_format': 'PNG',
            'output_quality': 95,
            'rename_prefix': '',
            'rename_suffix': '_watermarked',
            'remember_last_output_dir': True,
            'last_output_dir': '',
            'auto_save_template': True,
            'auto_save_interval': 300,  # 秒
            'language': 'zh_CN',
            'theme': 'light',
            'window_position': {'x': 100, 'y': 100},
            'window_size': {'width': 1200, 'height': 800},
            'max_recent_files': 10,
            'recent_files': []
        }
        
        # 加载配置
        self.config = self._load_config()
    
    def _ensure_config_dir_exists(self):
        """
        确保配置目录存在
        """
        if not os.path.exists(self.config_dir):
            try:
                os.makedirs(self.config_dir, exist_ok=True)
            except Exception as e:
                raise Exception(f"创建配置目录失败: {str(e)}")
    
    def _load_config(self):
        """
        从文件加载配置
        """
        try:
            if not os.path.exists(self.config_path):
                # 如果配置文件不存在，创建默认配置
                self._save_config(self.default_config)
                return self.default_config.copy()
            
            # 读取配置文件
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # 合并默认配置（处理新增的配置项）
            merged_config = self.default_config.copy()
            merged_config.update(config)
            
            return merged_config
        except Exception as e:
            # 如果加载失败，使用默认配置
            print(f"加载配置失败: {str(e)}")
            return self.default_config.copy()
    
    def _save_config(self, config):
        """
        保存配置到文件
        """
        try:
            # 确保配置目录存在
            self._ensure_config_dir_exists()
            
            # 保存配置文件
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            raise Exception(f"保存配置失败: {str(e)}")
    
    def get(self, key, default=None):
        """
        获取配置项
        """
        return self.config.get(key, default)
    
    def set(self, key, value):
        """
        设置配置项
        """
        self.config[key] = value
        return True
    
    def save(self):
        """
        保存当前配置
        """
        return self._save_config(self.config)
    
    def reset(self):
        """
        重置配置为默认值
        """
        self.config = self.default_config.copy()
        return self.save()
    
    def load_last_session(self):
        """
        加载上次会话的状态
        """
        try:
            if not os.path.exists(self.last_session_path):
                return None
            
            # 读取上次会话状态
            with open(self.last_session_path, 'r', encoding='utf-8') as f:
                last_session = json.load(f)
            
            return last_session
        except Exception as e:
            print(f"加载上次会话状态失败: {str(e)}")
            return None
    
    def save_last_session(self, session_data):
        """
        保存当前会话状态
        """
        try:
            # 确保配置目录存在
            self._ensure_config_dir_exists()
            
            # 添加保存时间
            session_data['saved_at'] = datetime.datetime.now().isoformat()
            
            # 保存会话状态
            with open(self.last_session_path, 'w', encoding='utf-8') as f:
                json.dump(session_data, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            raise Exception(f"保存会话状态失败: {str(e)}")
    
    def add_recent_file(self, file_path):
        """
        添加最近使用的文件
        """
        if not file_path or not os.path.exists(file_path):
            return False
        
        try:
            recent_files = self.config.get('recent_files', [])
            max_recent_files = self.config.get('max_recent_files', 10)
            
            # 如果文件已在列表中，移除它
            if file_path in recent_files:
                recent_files.remove(file_path)
            
            # 添加到列表开头
            recent_files.insert(0, file_path)
            
            # 限制列表长度
            if len(recent_files) > max_recent_files:
                recent_files = recent_files[:max_recent_files]
            
            # 更新配置
            self.config['recent_files'] = recent_files
            
            return True
        except Exception:
            return False
    
    def get_recent_files(self):
        """
        获取最近使用的文件列表
        """
        recent_files = self.config.get('recent_files', [])
        
        # 过滤掉不存在的文件
        valid_recent_files = []
        for file_path in recent_files:
            if os.path.exists(file_path):
                valid_recent_files.append(file_path)
        
        # 更新配置中的有效文件列表
        if len(valid_recent_files) != len(recent_files):
            self.config['recent_files'] = valid_recent_files
            self.save()
        
        return valid_recent_files
    
    def clear_recent_files(self):
        """
        清除最近使用的文件列表
        """
        self.config['recent_files'] = []
        return self.save()
    
    def get_output_settings(self):
        """
        获取输出设置
        """
        return {
            'format': self.config.get('output_format', 'PNG'),
            'quality': self.config.get('output_quality', 95),
            'prefix': self.config.get('rename_prefix', ''),
            'suffix': self.config.get('rename_suffix', '_watermarked'),
            'last_dir': self.config.get('last_output_dir', ''),
            'remember_dir': self.config.get('remember_last_output_dir', True)
        }
    
    def save_output_settings(self, settings):
        """
        保存输出设置
        """
        if 'format' in settings:
            self.config['output_format'] = settings['format']
        if 'quality' in settings:
            self.config['output_quality'] = settings['quality']
        if 'prefix' in settings:
            self.config['rename_prefix'] = settings['prefix']
        if 'suffix' in settings:
            self.config['rename_suffix'] = settings['suffix']
        if 'last_dir' in settings:
            self.config['last_output_dir'] = settings['last_dir']
        if 'remember_dir' in settings:
            self.config['remember_last_output_dir'] = settings['remember_dir']
        
        return self.save()