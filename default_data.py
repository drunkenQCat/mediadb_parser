# -*- coding: utf-8 -*-
lib_keyword = "DST-Destructibles"
album = "DST-Destructibles"
tab_path = r"C:\_SataVolumeA\Downloads\Export_TrackList_Destructibles Sound Effects.csv"
reaper_filelist = r"C:\REAPER\MediaDB\DST-Destructibles.ReaperFileList"
output_path = r"C:/TechnicalProjects/About_Python/mediadb_parser/output.ReaperFileList"
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
cd_regex = r'\d+'
track_prefix = r'Track'
track_regex = r'\d+'
id_prefix = 'PE-'
full_regex = ''
