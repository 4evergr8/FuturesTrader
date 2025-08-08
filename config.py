import os
import yaml

def load_config(filename="config.yaml"):
    if not os.path.exists(filename):
        print(f"❌ 配置文件 {filename} 不存在。")
        return None

    try:
        with open(filename, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        return config
    except Exception as e:
        print(f"❌ 读取配置文件失败：{e}")
        return None
