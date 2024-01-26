import json
import os


def read_json_config(filename="config.json"):
    # 获取当前工作目录
    current_directory = os.getcwd()

    # 构造配置文件的完整路径
    config_path = os.path.join(current_directory, filename)

    # 检查文件是否存在
    if os.path.exists(config_path):
        # 读取 JSON 配置文件
        with open(config_path, 'r') as json_file:
            config_data = json.load(json_file)
        return config_data
    else:
        print(f"Config file '{filename}' not found.")
        return None


if __name__ == '__main__':
    config = read_json_config()
    print(config)
