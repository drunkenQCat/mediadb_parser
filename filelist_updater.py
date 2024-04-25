# -*- coding: utf-8 -*-
import re
from enum import Enum

import default_data


class MatchCondition(Enum):
    NO_MATCH = 0
    TRACK_NUMBER_ONLY = 1
    CD_AND_TRACK_NUMBER = 2


def extract_serial_number(file_path):
    path_parts = file_path.split("\\")
    file_id = path_parts[-1].replace(".wav", "").strip()
    return file_id


def update_reaper_filelist(reaper_data: dict, tab_data: dict):
    # 找到所有属于相应Soundlib的FILE
    filtered_elements = {key: value for key, value in reaper_data.items() if
                         value['sound_lib'] == default_data.lib_keyword}
    # 检验lib中是否有音频文件。如果没有，找所有含lib_key的.wav文件
    if not any(key.endswith('.wav') for key in filtered_elements):
        # 遍历字典 B，找到符合条件的键，并添加到字典 A
        for key, value in reaper_data.items():
            if key.endswith('.wav') and default_data.lib_keyword in key:
                filtered_elements[key] = value
            elif key.endswith('.WAV') and default_data.lib_keyword in key:
                filtered_elements[key] = value
            elif key.endswith('.mp3') and default_data.lib_keyword in key:
                filtered_elements[key] = value
            elif key.endswith('.MP3') and default_data.lib_keyword in key:
                filtered_elements[key] = value

    count = 0
    modified_file_id_list = []
    first_path = next(iter(filtered_elements))
    first_id = extract_serial_number(first_path)
    first_id_in_tab = next(iter(tab_data))

    # 存储更新条目的详情
    updated_entries = []

    for path, data in filtered_elements.items():
        file_id = extract_serial_number(path)
        if file_id in tab_data:
            data['metadata']['C'] = default_data.album
            data['metadata']['T'] = tab_data[file_id]['title']
            data['metadata']['D'] = tab_data[file_id]['desc']
            count += 1
            # 添加更新条目信息
            entry_info = f"Updated File ID: {file_id}, Title: {tab_data[file_id]['title']}, Desc: {tab_data[file_id]['desc']}"
            updated_entries.append(entry_info)
            modified_file_id_list.append(file_id)
        reaper_data[path] = data

    output_message = f"the first file ID is {first_id}\n"
    output_message += f"the first ID in tab is {first_id_in_tab}\n"
    output_message += f"the first file path is {first_path}\n"
    output_message += f"{count} items has been written.\n"

    # 添加前十条和后十条更新的条目信息
    first_ten_updates = "\n".join(updated_entries[:10])
    last_ten_updates = "\n".join(updated_entries[-10:])
    if updated_entries:
        output_message += "First 10 updated entries:\n===============\n" + first_ten_updates + "\n"
        output_message += "Last 10 updated entries:\n===============\n" + last_ten_updates + "\n"

    # 检查tab_data中有但file_id_list中没有的元素，并写入日志文件
    with open('missing_file_log.txt', 'w', encoding='utf-8') as f:
        missing_count = 0
        first_modified_id = modified_file_id_list[0]
        f.write("\n=========================\n")
        f.write(default_data.lib_keyword + "\n")
        for file_id, _ in tab_data.items():
            if file_id not in modified_file_id_list and file_id >= first_modified_id:
                if missing_count < 4:
                    output_message += f"Missing File ID: {file_id}\n"
                missing_count += 1
                f.write(f"File ID: {file_id}\n")
        output_message += f"...\nTotally {missing_count} missing items\n"

    return output_message
