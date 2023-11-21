import re
import default_data

def extract_serial_number(file_path):
    # 示例用法
    # file_path = 'the parent path\\6000 Extension III\\CD 6071\\29.wav'
    # result = extract_serial_number(file_path) -------6071-29
    pattern = r'.*CD (\d+)\\(\d+)\. (.+)\.wav'
    match = re.match(pattern, file_path)
    
    if match:
        cd_number = match.group(1)
        track_number = match.group(2)
        return f'{cd_number}-{track_number}'

# %%
def update_reaper_filelist(reaper_data : dict, tab_data : dict):
    # 找到所有属于相应Soundlib的FILE
    filtered_elements = {key: value for key, value in reaper_data.items() if value.get('sound_lib') == default_data.lib_keyword}
    for path, data in filtered_elements.items():
        file_id = extract_serial_number(path)
        if file_id in tab_data:
            data['metadata']['A'] = default_data.lib_keyword
            data['metadata']['T'] = tab_data[file_id]['title']
            data['metadata']['D'] = tab_data[file_id]['desc']
        reaper_data[path] = data
        
