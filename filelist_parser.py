import shlex
import hashlib
import os
import json
import default_data

def calculate_hash(file_path):
    # 计算文件路径的哈希值
    hasher = hashlib.md5()
    hasher.update(file_path.encode())
    return hasher.hexdigest()

def parse_reaper_filelist(reaper_filelist_path):
    # 计算哈希值
    hash_value = calculate_hash(reaper_filelist_path)

    # 生成对应的 PyTables 文件路径
    json_path = f"{hash_value}.json"
    default_data.json_path = json_path

    if os.path.exists(json_path):
        # 如果 PyTables 文件已存在，直接读取
        return read_updated_reaper_filelist(json_path)
    else:
        # 否则，解析 ReaperFileList
        paths, reaper_data = read_reaper_filelist(reaper_filelist_path)

        # 保存到 PyTables 文件
        save_to_json(json_path, paths, reaper_data)

        return paths, reaper_data

def save_to_json(json_path, paths, reaper_data):
    # 将 paths 和 reaper_data 写入 JSON 文件
    data = {
        'paths': paths,
        'reaper_data': reaper_data
    }
    with open(json_path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=2)


def read_updated_reaper_filelist(json_path):
    # 从 JSON 文件中读取 paths 和 reaper_data
    with open(json_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)

    paths = data.get('paths', [])
    reaper_data = data.get('reaper_data', {})

    return paths, reaper_data

def read_reaper_filelist(reaper_filelist_path):
    reaper_data = {}
    paths = []
    current_file = None
    
    with open(reaper_filelist_path, 'r', encoding='utf8') as reaper_filelist:
        lines = reaper_filelist.readlines()

    for line in lines:
        if line.startswith('PATH'):
            paths.append(line)
        elif line.startswith('FILE'):
            if current_file:
                reaper_data[current_file["file_path"]] = current_file
            current_file = {}
            wav_path = line.strip().split('"')[1]
            current_file[ "file_path" ] = wav_path
            current_file[ "sound_lib" ] = parse_soundlib(wav_path)
            current_file[ "position_info" ]= " ".join(line.split('"')[2:])
            current_file[ "metadata" ]= {}

        elif line.startswith('DATA'):
            def parse_attributes(attr_str):
                splited = attr_str.split(':')
                key = splited[0]
                value = ':'.join(splited[1:])
                if current_file:
                    current_file[key] = value
            def parse_metadata(attr_str : str):
                splited = attr_str.strip('"').split(':')
                key = splited[0]
                value = ':'.join(splited[1:])
                if current_file:
                    current_file['metadata'][key] = value
            # start to process
            try:
                attrs = shlex.split(line, posix=False)[1:]
            except Exception: 
                print(line)
            for attr in attrs:
                if attr.startswith('"'):
                    parse_metadata(attr)
                    continue
                parse_attributes(attr)
    if current_file:
        reaper_data[current_file['file_path']] = current_file
    return paths, reaper_data

def parse_soundlib(wav_path: str):
    splited = wav_path.split('\\')
    return splited[-3]
