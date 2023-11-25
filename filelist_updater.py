import default_data
import re


def extract_serial_number(file_path):
    # 示例用法
    # file_path = 'the parent path\\6000 Extension III\\CD 6071\\29.wav'
    # result = extract_serial_number(file_path) -------6071-29
    cd_pattern = r'.*\\' + f'{default_data.cd_prefix}({default_data.cd_regex})'
    track_pattern = r'.*\\' + f'{default_data.track_prefix}({default_data.track_regex})'
    ending_pattern = r'.*\.(WAV|wav|Wav|mp3)'
    pattern = cd_pattern + track_pattern + ending_pattern
    match = re.match(pattern, file_path)
    file_id = ''
    if match:
        cd_number = match.group(1)
        track_number = match.group(2)
        file_id = f'{default_data.id_prefix}{cd_number.zfill(2)}-{track_number.zfill(2)}'
    return file_id
    # data = {'file_path': file_path}
    # exec(default_data.extract_pattern, globals(), data)
    # return data.get('id', '')


# %%
def update_reaper_filelist(reaper_data: dict, tab_data: dict):
    # 找到所有属于相应Soundlib的FILE
    filtered_elements = {key: value for key, value in reaper_data.items() if
                         value['sound_lib'] == default_data.lib_keyword}
    # filtered_elements = {}
    # for key, value in reaper_data.items():
    #     if value['sound_lib'] == default_data.lib_keyword:
    #         filtered_elements[key] = value

    count = 0
    first_path = next(iter(filtered_elements))
    first_id = extract_serial_number(first_path)
    first_id_in_tab = next(iter(tab_data))
    for path, data in filtered_elements.items():
        file_id = extract_serial_number(path)
        if file_id in tab_data:
            data['metadata']['A'] = default_data.lib_keyword
            data['metadata']['T'] = tab_data[file_id]['title']
            data['metadata']['D'] = tab_data[file_id]['desc']
            count += 1
        reaper_data[path] = data
    print(f'the first fileid is {first_id}')
    print(f'the first id in tab is {first_id_in_tab}')
    print(f'the first file path is {first_path}')
    print(f'{count} items has been written.')

