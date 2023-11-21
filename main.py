import tkinter as tk
from filelist_parser import read_or_parse_reaper_filelist
import tkinter_ui

if __name__ == "__main__":
    reaper_file_list = r'C:/Users/Administrator/AppData/Roaming/REAPER/MediaDB/0b.ReaperFileList'
    read_or_parse_reaper_filelist(reaper_file_list)
    # root = tk.Tk()
    # app = tkinter_ui.MyApp(root)
    # root.mainloop()
