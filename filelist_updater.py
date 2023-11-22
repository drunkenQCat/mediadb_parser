import default_data
import re

def extract_serial_number(file_path):
    # 示例用法
    # file_path = 'the parent path\\6000 Extension III\\CD 6071\\29.wav'
    # result = extract_serial_number(file_path) -------6071-29
    test = r"""
pattern = r'.*\\HS-(\d+)-(\d+).*\.(WAV|wav|Wav)'
match = re.match(pattern, file_path)
id = ''
if match:
    cd_number = match.group(1)
    track_number = match.group(2)
    id =  f'HS-{cd_number.zfill(2)}-{track_number.zfill(2)}'
"""
    data = {'file_path':file_path}
    exec(default_data.extract_pattern, globals(), data)
    return data.get('id', '')

# %%
def update_reaper_filelist(reaper_data : dict, tab_data : dict):
    # 找到所有属于相应Soundlib的FILE
    filtered_elements = {key: value for key, value in reaper_data.items() if value['sound_lib'] == default_data.lib_keyword}
    # filtered_elements = {}
    # for key, value in reaper_data.items():
    #     if value['sound_lib'] == default_data.lib_keyword:
    #         filtered_elements[key] = value

    count = 0
    for path, data in filtered_elements.items():
        file_id = extract_serial_number(path)
        if file_id in tab_data:
            data['metadata']['A'] = default_data.lib_keyword
            data['metadata']['T'] = tab_data[file_id]['title']
            data['metadata']['D'] = tab_data[file_id]['desc']
            count += 1
        reaper_data[path] = data
    print(f'{count} items has been written')
        
