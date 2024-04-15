lib_keyword = "6000"
lib_folder_keyword = "6000"
tab_path = (r"C:\Users\Administrator\Documents\Injector\TABS\Sound Ideas Series 6000 "
            r"'The General' Sound Effects Library.tab")
reaper_filelist = r"C:\TechnicalProjects\About_Python\mediadb_parser\6000.ReaperFileList"
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

cd_prefix = 'cd'
cd_regex = r'\d{2}'
track_prefix = r'Track\s?'
track_regex = r'\d+'
id_prefix = '60'
