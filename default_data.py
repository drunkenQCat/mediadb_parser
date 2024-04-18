# -*- coding: utf-8 -*-
lib_keyword = "3D-3DSFX.Series"
album = "3D-3DSFX.Series"
tab_path = r"C:\Users\Administrator\Documents\Injector\TABS\Hollywood Edge 3DSFX Collection.tab"
reaper_filelist = r"C:\TechnicalProjects\About_Python\mediadb_parser\6000.ReaperFileList"
output_path = r"C:\Users\Administrator\AppData\Roaming\REAPER\MediaDB\3D-3DSFX.Series.ReaperFileList"
extract_pattern = r"""
pattern = r'.*\\cd(\d+)\\Track\s*(\d+).*\.(WAV|wav|Wav)'
match = re.match(pattern, file_path)
id = ''
if match:
    cd_number = match.group(1)
    track_number = match.group(2)
    id =  f'TCF{cd_number.zfill(2)}-{track_number.zfill(2)}'
"""
json_path = ''
pickle_path = 'pickle_test.pickle'

cd_prefix = 'CD'
cd_regex = r'\d{2}'
track_prefix = r'-\d\d-'
track_regex = r'\d\d'
id_prefix = '3D-'
full_regex = ''
