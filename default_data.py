lib_keyword = "6000 Extension III"
tab_path = r"C:\Users\Administrator\Documents\Injector\TABS\Sound Ideas Series 6000 Extension III Sound Effects Library.tab"
reaper_filelist = r"C:/Users/Administrator/AppData/Roaming/REAPER/MediaDB/0b.ReaperFileList"
output_path = r"C:/TechnicalProjects/About_Python/mediadb_parser/output.ReaperFileList"
extract_pattern = r"""
pattern = r'.*CD (\d+)\\(\d+)\. (.+)\.wav'
match = re.match(pattern, file_path)
id = ''
if match:
    cd_number = match.group(1)
    track_number = match.group(2)
    id =  f'{cd_number}-{track_number}'
"""
json_path = ''