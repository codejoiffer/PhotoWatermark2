import os
import json
import datetime
import os
from core.watermark import Watermark


class TemplateManager:
    """
    模板管理类，用于保存、加载和管理水印模板
    """
    
    def __init__(self, templates_dir=None):
        # 获取用户目录
        user_home = os.path.expanduser('~')
        # 默认模板保存目录
        self.default_templates_dir = os.path.join(
            user_home, 'Library', 'Application Support', 'PhotoWatermark2', 'templates'
        )
        
        # 使用指定目录或默认目录
        self.templates_dir = templates_dir or self.default_templates_dir
        
        # 确保模板目录存在
        self._ensure_templates_dir_exists()
        
        # 模板文件扩展名
        self.template_extension = '.json'
    
    def _ensure_templates_dir_exists(self):
        """
        确保模板目录存在
        """
        if not os.path.exists(self.templates_dir):
            try:
                os.makedirs(self.templates_dir, exist_ok=True)
            except Exception as e:
                raise Exception(f"创建模板目录失败: {str(e)}")
    
    def save_template(self, name, watermark, description=""):
        """
        保存水印配置为模板
        """
        if not name or not isinstance(name, str):
            raise ValueError("模板名称不能为空且必须是字符串")
        
        if not isinstance(watermark, Watermark):
            raise TypeError("watermark参数必须是Watermark类型")
        
        try:
            # 生成模板文件路径
            template_name = f"{name}{self.template_extension}"
            template_path = os.path.join(self.templates_dir, template_name)
            
            # 检查文件名是否已存在
            counter = 1
            while os.path.exists(template_path):
                template_name = f"{name}_{counter}{self.template_extension}"
                template_path = os.path.join(self.templates_dir, template_name)
                counter += 1
            
            # 创建模板数据
            template_data = {
                'name': name,
                'description': description,
                'created_at': datetime.datetime.now().isoformat(),
                'watermark_config': watermark.to_dict()
            }
            
            # 保存模板到文件
            with open(template_path, 'w', encoding='utf-8') as f:
                json.dump(template_data, f, indent=2, ensure_ascii=False)
            
            # 返回实际保存的模板名称（可能包含计数器后缀）
            return os.path.splitext(template_name)[0]
        except Exception as e:
            raise Exception(f"保存模板失败: {str(e)}")
    
    def load_template(self, name):
        """
        加载模板
        """
        if not name:
            raise ValueError("模板名称不能为空")
        
        try:
            # 构建可能的文件路径
            possible_paths = [
                os.path.join(self.templates_dir, f"{name}{self.template_extension}"),
                os.path.join(self.templates_dir, name)
            ]
            
            # 查找存在的文件路径
            template_path = None
            for path in possible_paths:
                if os.path.exists(path):
                    template_path = path
                    break
            
            if not template_path:
                raise FileNotFoundError(f"找不到模板: {name}")
            
            # 读取模板文件
            with open(template_path, 'r', encoding='utf-8') as f:
                template_data = json.load(f)
            
            # 创建Watermark对象并加载配置
            watermark = Watermark()
            if 'watermark_config' in template_data:
                watermark.from_dict(template_data['watermark_config'])
            
            # 返回Watermark对象和模板元数据
            metadata = {
                'name': template_data.get('name', name),
                'description': template_data.get('description', ''),
                'created_at': template_data.get('created_at', '')
            }
            
            return watermark, metadata
        except Exception as e:
            raise Exception(f"加载模板失败: {str(e)}")
    
    def delete_template(self, name):
        """
        删除模板
        """
        if not name:
            raise ValueError("模板名称不能为空")
        
        try:
            # 构建可能的文件路径
            possible_paths = [
                os.path.join(self.templates_dir, f"{name}{self.template_extension}"),
                os.path.join(self.templates_dir, name)
            ]
            
            # 查找存在的文件路径
            template_path = None
            for path in possible_paths:
                if os.path.exists(path):
                    template_path = path
                    break
            
            if not template_path:
                raise FileNotFoundError(f"找不到模板: {name}")
            
            # 删除模板文件
            os.remove(template_path)
            return True
        except Exception as e:
            raise Exception(f"删除模板失败: {str(e)}")
    
    def list_templates(self):
        """
        列出所有可用的模板
        """
        try:
            templates = []
            
            # 检查模板目录是否存在
            if not os.path.exists(self.templates_dir):
                return templates
            
            # 遍历模板目录中的文件
            for filename in os.listdir(self.templates_dir):
                if filename.endswith(self.template_extension):
                    file_path = os.path.join(self.templates_dir, filename)
                    
                    try:
                        # 读取模板信息
                        with open(file_path, 'r', encoding='utf-8') as f:
                            template_data = json.load(f)
                        
                        # 收集模板信息
                        template_info = {
                            'name': os.path.splitext(filename)[0],
                            'display_name': template_data.get('name', os.path.splitext(filename)[0]),
                            'description': template_data.get('description', ''),
                            'created_at': template_data.get('created_at', ''),
                            'path': file_path
                        }
                        
                        templates.append(template_info)
                    except Exception:
                        # 如果读取模板信息失败，跳过该文件
                        continue
            
            # 按创建时间排序
            templates.sort(key=lambda x: x['created_at'], reverse=True)
            
            return templates
        except Exception as e:
            raise Exception(f"列出模板失败: {str(e)}")
    
    def rename_template(self, old_name, new_name):
        """
        重命名模板
        """
        if not old_name or not new_name:
            raise ValueError("模板名称不能为空")
        
        if old_name == new_name:
            return True
        
        try:
            # 构建可能的旧文件路径
            possible_old_paths = [
                os.path.join(self.templates_dir, f"{old_name}{self.template_extension}"),
                os.path.join(self.templates_dir, old_name)
            ]
            
            # 查找存在的旧文件路径
            old_path = None
            for path in possible_old_paths:
                if os.path.exists(path):
                    old_path = path
                    break
            
            if not old_path:
                raise FileNotFoundError(f"找不到模板: {old_name}")
            
            # 构建新文件路径
            new_path = os.path.join(self.templates_dir, f"{new_name}{self.template_extension}")
            
            # 检查新文件名是否已存在
            counter = 1
            base_new_path = new_path
            while os.path.exists(new_path):
                new_path = os.path.join(self.templates_dir, f"{new_name}_{counter}{self.template_extension}")
                counter += 1
            
            # 重命名文件
            os.rename(old_path, new_path)
            
            # 更新模板内部的名称
            try:
                with open(new_path, 'r', encoding='utf-8') as f:
                    template_data = json.load(f)
                
                template_data['name'] = os.path.splitext(os.path.basename(new_path))[0]
                
                with open(new_path, 'w', encoding='utf-8') as f:
                    json.dump(template_data, f, indent=2, ensure_ascii=False)
            except Exception:
                # 如果更新模板内部名称失败，不影响重命名操作
                pass
            
            return True
        except Exception as e:
            raise Exception(f"重命名模板失败: {str(e)}")