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
            pattern_to_separate_title_and_desc = r'(.*?)\s{2,}(.*)'
            file_id = f"{splited_line[0]}-{splited_line[1].zfill(2)}"
            title_and_desc = re.match(pattern_to_separate_title_and_desc, splited_line[3])
            if title_and_desc is not None:
                wav_metadata["title"] = title_and_desc.group(1)
                wav_metadata["desc"] = title_and_desc.group(2)
                if is_different_part(file_id):
                    tab_data[get_last_id()]["desc"] = update_desc(title_and_desc.group(2))
                    continue
            else:
                wav_metadata["desc"] = splited_line[3]
                wav_metadata["title"] = ""
                if is_different_part(file_id):
                    tab_data[get_last_id()]["desc"] = update_desc(splited_line[3])
                    continue

            tab_data[file_id] = wav_metadata
    return tab_data


def merge_strings(str1, str2):
    common_prefix = ""
    common_suffix = ""

    # 找到共同的前缀
    min_len = min(len(str1), len(str2))
    for i in range(min_len):
        if str1[i] == str2[i]:
            common_prefix += str1[i]
        else:
            break

    # 找到共同的后缀
    for i in range(1, min_len + 1):
        if str1[-i] == str2[-i]:
            common_suffix = str1[-i] + common_suffix
        else:
            break

    # 去除共同的前缀和后缀
    str1 = str1[len(common_prefix):-len(common_suffix)] if common_suffix else str1[len(common_prefix):]
    str2 = str2[len(common_prefix):-len(common_suffix)] if common_suffix else str2[len(common_prefix):]

    # 合并字符串，使用逗号分隔
    merged_string = f"{common_prefix}{str1},{str2}{common_suffix}"

    return merged_string
