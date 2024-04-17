# -*- coding: utf-8 -*-
import re


def read_tab_file(tab_file_path):
    tab_data = {}

    def is_different_part(file_id: str) -> bool:
        return get_last_id() == file_id

    def update_desc(new_desc: str) -> str:
        last_id = get_last_id()
        old_desc = tab_data[last_id]["desc"]
        return merge_strings(old_desc, new_desc)

    def get_last_id():
        last_id = list(tab_data.keys())[-1] if tab_data else None
        return last_id

    with open(tab_file_path, 'r', encoding='utf8') as tab_file:
        for line in tab_file:
            wav_metadata = {}
            splited_line = line.strip().split('\t')
            wav_metadata["cd"] = splited_line[0]
            wav_metadata["track"] = splited_line[1].zfill(2)
            pattern_to_separate_title_and_desc = r'(.*?)\s{4,}(.*)'
            file_id = f"{splited_line[0]}-{splited_line[1].zfill(2)}"
            title_desc_combined = splited_line[3].strip().replace('"', '')
            title_and_desc = re.match(pattern_to_separate_title_and_desc, title_desc_combined)
            if title_and_desc is not None:
                wav_metadata["title"] = title_and_desc.group(1)
                wav_metadata["desc"] = title_and_desc.group(2)
                if is_different_part(file_id):
                    tab_data[get_last_id()]["desc"] = update_desc(title_and_desc.group(2))
                    continue
            else:
                wav_metadata["desc"] = title_desc_combined
                wav_metadata["title"] = ""
                if is_different_part(file_id):
                    tab_data[get_last_id()]["desc"] = update_desc(title_desc_combined)
                    continue

            tab_data[file_id] = wav_metadata
    return tab_data


def merge_strings(str1, str2):
    # 查找共同前缀
    prefix_length = 0
    while (prefix_length < len(str1) and prefix_length < len(str2) and
           str1[prefix_length] == str2[prefix_length]):
        prefix_length += 1
    prefix = str1[:prefix_length]

    # 查找共同后缀
    suffix_length = 0
    while (suffix_length < len(str1) - prefix_length and suffix_length < len(str2) - prefix_length and
           str1[-1 - suffix_length] == str2[-1 - suffix_length]):
        suffix_length += 1
    suffix = str1[-suffix_length:] if suffix_length > 0 else ""

    # 提取没有公共前缀和后缀的部分
    unique_part1 = str1[prefix_length:-suffix_length].strip() if suffix_length > 0 else str1[prefix_length:].strip()
    unique_part2 = str2[prefix_length:-suffix_length].strip() if suffix_length > 0 else str2[prefix_length:].strip()

    # 构建结果字符串
    if unique_part1 and unique_part2:
        return f"{prefix}{unique_part1}, {unique_part2}{suffix}"
    elif unique_part1:
        return f"{prefix}{unique_part1}{suffix}"
    else:
        return f"{prefix}{unique_part2}{suffix}"


def merge_string_list(string_list):
    if not string_list:
        return ""
    
    result = string_list[0]
    for next_string in string_list[1:]:
        result = merge_strings(result, next_string)
    
    # 移除最后的逗号（如果存在）并且处理空格
    result = result.rstrip(',').strip()
    return result

# 测试用例
string_list1 = ["hello world comp", "hello universe comp", "hello world G comp"]
string_list2 = ["hello world", "hello universe", "hello world"]
print("Merged result 1:", merge_string_list(string_list1))
print("Merged result 2:", merge_string_list(string_list2))
