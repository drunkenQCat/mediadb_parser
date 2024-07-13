# -*- coding: utf-8 -*-
import copy
import shutil
from tqdm import tqdm


def fix_all_irregular_items(reaper_files):
    """
    修复所有不规则的描述

    Args:
    - reaper_files (dict): 包含 Reaper 文件信息的字典

    Returns:
    - None

    Description:
    该函数用于修复包含不规则项目的 Reaper 文件信息字典。不规则项目是指键名包含大写字母的键值对。
    函数会将不规则项目的键名替换为没有双引号和冒号的格式，并将这些键名的值添加到 'metadata' 字典中的 'D' 键的值后面。
    最后，删除原始不规则项目的键值对，并更新 'metadata' 字典的 'D' 键的值为修复后的描述。

    Example:
    reaper_files = {
        'file1': {
            'metadata': {
                'D': 'Original description'
            },
            'Irregular_Key': 'value'
        }
    }
    fix_all_irregular_items(reaper_files)
    # 'metadata' 字典的 'D' 键的值将会更新为 'Original description Irregular_Key'
    # 'Irregular_Key' 键值对将会被删除
    """

    file_list = reaper_files
    for outer_key, inner_dict in file_list.items():
        # 查找包含大写字母的键名
        uppercase_keys = [key for key in inner_dict.keys() if any(c.isupper() for c in key) and len(key) > 1]
        if uppercase_keys:
            # 获取原始描述，如果 'metadata' 字典中不存在 'D' 键，则设置为空字符串
            original_desc = ''
            try:
                original_desc = inner_dict['metadata']['D']
            except KeyError:
                try:
                    inner_dict['metadata']['D'] = inner_dict['d']
                except KeyError:
                    inner_dict['metadata']['D'] = ''
            # 替换不规则键名的格式，并将它们添加到原始描述后面
            irregular_keys = [key.replace('"', " ").replace(':', " ") for key in uppercase_keys]
            new_desc = original_desc + ' '+' '.join(irregular_keys)
            inner_dict['metadata']['D'] = new_desc
            # 删除原始不规则项目的键值对
            for key in uppercase_keys:
                del inner_dict[key]
            # 更新字典中的值
            file_list[outer_key] = inner_dict


def write_reaper_filelist(paths, original_reaper_data, output_path):
    reaper_filelist_content = "\n".join(paths)
    reaper_data = copy.deepcopy(original_reaper_data)
    fix_all_irregular_items(reaper_data)

    for file_path, file_data in tqdm(reaper_data.items()):
        reaper_filelist_content += f'FILE "{file_path}" {file_data["position_info"]}'
        del file_data["file_path"]
        del file_data["position_info"]
        del file_data["sound_lib"]

        bwf_data = file_data.get("metadata", {})
        if bwf_data:
            bwf_line = 'DATA '

            # 使用for循环构建字符串
            for key, value in bwf_data.items():
                if bwf_line != 'DATA ':  # 如果不是第一个元素，添加空格
                    bwf_line += ' '
                bwf_line += f'"{key}:{value}"'  # 添加当前的键值对

            reaper_filelist_content += bwf_line + '\n'
        del file_data["metadata"]

        # 获取字典键
        keys = list(file_data.keys())

        # 计算拆分的位置
        if len(keys) == 0:
            continue
        basic_info_len = len(keys)
        split_index = basic_info_len // 2 if basic_info_len > 4 else basic_info_len

        # 拆分字典
        basic_info_list_1 = [f'{key}:{file_data[key]}' for key in keys[:split_index]]
        basic_info_1 = 'DATA ' + ' '.join(basic_info_list_1)
        reaper_filelist_content += basic_info_1 + '\n'
        if split_index != basic_info_len:
            basic_info_list_2 = [f'{key}:{file_data[key]}' for key in keys[split_index:]]
            basic_info_2 = 'DATA ' + ' '.join(basic_info_list_2)
            reaper_filelist_content += basic_info_2 + '\n'

    with open(output_path, 'w', encoding='utf8') as output_file:
        output_file.write(reaper_filelist_content)


def overwrite_file_list(output_path, original_path):
    # 备份一份
    shutil.copyfile(original_path, original_path + ".bak")
    shutil.copyfile(output_path, original_path)
