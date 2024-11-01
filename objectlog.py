import json
import os
import shutil

class SafeJSONHandler:
    def __init__(self, file_path):
        self.file_path = file_path
        self.backup_path = file_path + ".bak"
    
    # 读取 JSON 文件
    def read_json(self, path=None):
        if path is None:
            path = self.file_path
        try:
            with open(path, 'r') as file:
                data = json.load(file)
            return data
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"读取文件时出错: {e}")
            return None
    
    # 备份文件，防止写入错误
    def backup_file(self):
        try:
            shutil.copy(self.file_path, self.backup_path)
            print(f"备份创建成功: {self.backup_path}")
        except Exception as e:
            print(f"备份文件时出错: {e}")
    
    # 写入 JSON 文件，同时保留备份
    def write_json(self, data):
        try:
            # 备份当前文件
            self.backup_file()
            
            # 尝试写入数据
            with open(self.file_path, 'w') as file:
                json.dump(data, file, indent=4)
            
            # 写入成功后进行文件比较
            if self.compare_files(self.backup_path, self.file_path):
                print("文件更新成功，数据一致。")
            else:
                print("写入后文件与备份不一致，恢复备份。")
                self.restore_backup()

        except Exception as e:
            print(f"写入文件时出错，恢复备份: {e}")
            # 恢复备份文件
            self.restore_backup()
    
    # 恢复备份文件
    def restore_backup(self):
        try:
            if os.path.exists(self.backup_path):
                shutil.copy(self.backup_path, self.file_path)
                print("备份恢复成功。")
            else:
                print("未找到备份文件，无法恢复。")
        except Exception as e:
            print(f"恢复备份时出错: {e}")
    
    # 比较备份文件和新文件，确保写入后的数据与备份一致
    def compare_files(self, backup_path, new_path):
        try:
            backup_data = self.read_json(backup_path)
            new_data = self.read_json(new_path)
            
            if backup_data is None or new_data is None:
                return False

            # 遍历每个对象，比较相同的 key 值
            for backup_obj, new_obj in zip(backup_data, new_data):
                for key in backup_obj:
                    if key in new_obj and backup_obj[key] != new_obj[key]:
                        print(f"不一致的键: {key}, 备份值: {backup_obj[key]}, 新值: {new_obj[key]}")
                        return False
            return True
        except Exception as e:
            print(f"比较文件时出错: {e}")
            return False
    
    # 列出所有对象中的唯一键
    def list_all_keys(self):
        """
        列出 JSON 文件中所有对象的唯一键
        """
        data = self.read_json(self.file_path)
        if data is None:
            return
        
        all_keys = set()
        try:
            # 遍历每个对象，收集键
            for obj in data:
                all_keys.update(obj.keys())
            
            print("文件中包含的所有键:", all_keys)
            return all_keys
        except Exception as e:
            print(f"列出键时出错: {e}")

    def delete_key(self, key_to_delete):
        """
        删除 JSON 数据中指定的键
        """
        data = self.read_json(self.file_path)
        if data is None:
            print("无法读取文件数据，操作失败。")
            return
        
        # 遍历所有对象，删除指定的键
        for obj in data:
            if key_to_delete in obj:
                del obj[key_to_delete]
        
        # 写入更新后的数据
        self.write_json(data)
        print(f"已删除键: {key_to_delete}")



if __name__ == "__main__":
    # 示例用法
    handler = SafeJSONHandler('/home/leech/code/3DGT-LLM/results/objectlog.json')
    # 列出所有的键
    keys = handler.list_all_keys()
    # 输出数据
    data = handler.read_json()
    # 更新json
    handler.write_json(data)
