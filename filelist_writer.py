import copy
import shutil
from tqdm import tqdm


def fix_all_irregular_items(reaper_files):
    file_list = reaper_files
    for outer_key, inner_dict in file_list.items():
        uppercase_keys = [key for key in inner_dict.keys() if any(c.isupper() for c in key)]
        if uppercase_keys:
            original_desc = ''
            try:
                original_desc = inner_dict['metadata']['D']
            except KeyError:
                inner_dict['metadata']['D'] = ''
            irregular_keys = [key.replace('"', "'").strip(':') for key in uppercase_keys]
            new_desc = original_desc + ' '.join(irregular_keys)
            inner_dict['metadata']['D'] = new_desc
            for key in uppercase_keys:
                del inner_dict[key]
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
            bwf_line = 'DATA ' + ' '.join([f'"{key}:{value}"' for key, value in bwf_data.items()])
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
