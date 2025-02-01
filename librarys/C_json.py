import json5
import re

def json_edit(file_path, key, new_value):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            data = json5.loads(content)
        if key in data:
            data[key] = new_value
            print(f"键 '{key}' 的值已修改为: {new_value}")
        else:
            print(f"键 '{key}' 不存在于文件中。")
            return
        pattern = re.compile(rf'(?P<key>{re.escape(key)}|"{re.escape(key)}")\s*:\s*(?P<value>.+?)(?P<comma>,?)\s*(?://.*)?$')
        modified_content = []
        for line in content.splitlines():
            match = pattern.search(line)
            if match and match.group('key').strip('"') == key:
                if isinstance(new_value, str):
                    new_value_str = f'"{new_value}"'
                else:
                    new_value_str = str(new_value)
                line = pattern.sub(lambda m: f'{m.group("key")}: {new_value_str}{m.group("comma")}', line)
            modified_content.append(line)
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write("\n".join(modified_content))
        print(f"文件已更新：{file_path}")
    except FileNotFoundError:
        print(f"文件未找到：{file_path}")
    except json5.JSON5DecodeError as e:
        print(f"解析文件时出错：{e}")
    except Exception as e:
        print(f"发生错误：{e}")
def json_read(file_path, key):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            data = json5.loads(content)
        if key in data:
            return data[key]
        else:
            print(f"键 '{key}' 不存在于文件中。")
            return None
    except FileNotFoundError:
        print(f"文件未找到：{file_path}")
        return None