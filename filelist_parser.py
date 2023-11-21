import shlex
import hashlib
import tables as tb
import os
import json
from tqdm import tqdm

def calculate_hash(file_path):
    # 计算文件路径的哈希值
    hasher = hashlib.md5()
    hasher.update(file_path.encode())
    return hasher.hexdigest()

def read_or_parse_reaper_filelist(reaper_filelist_path):
    # 计算哈希值
    hash_value = calculate_hash(reaper_filelist_path)

    # 生成对应的 PyTables 文件路径
    pytable_path = f"{hash_value}.h5"

    if os.path.exists(pytable_path):
        # 如果 PyTables 文件已存在，直接读取
        return read_updated_reaper_filelist(pytable_path)
    else:
        # 否则，解析 ReaperFileList
        paths, reaper_data = read_reaper_filelist(reaper_filelist_path)

        # 保存到 PyTables 文件
        save_to_pytables(pytable_path, paths, reaper_data)

        return paths, reaper_data

def save_to_pytables(pytable_path, paths, reaper_data):
    # 定义 PyTables 表格结构
    class ReaperFile(tb.IsDescription):
        file_path = tb.UnicodeCol(255, pos=0)
        position_info = tb.StringCol(255, pos=1)
        sound_lib = tb.StringCol(255, pos=2)
        metadata = tb.StringCol(1024, pos=3)

    # 创建 PyTables 文件
    with tb.open_file(pytable_path, mode='w') as h5file:
        # 创建表格
        h5file.create_array('/', 'paths_array', paths)
        table = h5file.create_table('/', 'reaper_files', description=ReaperFile)
        # 填充表格
        for file_path, file_data in tqdm(reaper_data.items()):
            row = table.row
            try:
                row['file_path'] = file_path
            except Exception as e:
                print(file_path)
                print(file_data)
                print(e)
            row['position_info'] = file_data['position_info']
            row['sound_lib'] = file_data['sound_lib']
            row['metadata'] = json.dumps(file_data.get('metadata', {}))
            row.append()
        h5file.create_array('/', 'test', paths)

def read_updated_reaper_filelist(pytable_path):
    # 读取 PyTables 文件
    with tb.open_file(pytable_path, mode='r') as h5file:
        # 读取表格
        table = h5file.root.reaper_files

        paths = h5file.root.paths_array.read()
        reaper_data = {}

        # 遍历表格
        for row in table.iterrows():
            file_path = row['file_path'].decode('utf-8')
            position_info = row['position_info'].decode('utf-8')
            sound_lib = row['sound_lib'].decode('utf-8')
            metadata_str = row['metadata'].decode('utf-8')

            # 将字符串形式的元数据转换为字典
            metadata = json.loads(metadata_str)

            reaper_data[file_path] = {
                'position_info': position_info,
                'sound_lib': sound_lib,
                'metadata': metadata
            }

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
            attrs = shlex.split(line, posix=False)[1:]
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
