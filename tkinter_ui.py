import json
import tkinter as tk
from tkinter import filedialog
import default_data
from tab_reader import read_tab_file
from filelist_parser import parse_reaper_filelist
from filelist_parser import save_to_json
from filelist_parser import save_to_pickle
from filelist_updater import update_reaper_filelist
from filelist_writer import write_reaper_filelist


def get_path_pattern():
    cd_pattern = r'.*\\' + f'{default_data.cd_prefix}({default_data.cd_regex})'
    track_pattern = r'.*\\' + f'{default_data.track_prefix}({default_data.track_regex})'
    ending_pattern = r'.*\.(WAV|wav|Wav|mp3)'
    pattern = cd_pattern + track_pattern + ending_pattern
    return pattern


class MyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Reaper Filelist Updater")

        # 初始化参数
        self.lib_keyword_str = tk.StringVar(value=default_data.lib_keyword)
        self.tab_file_path_str = tk.StringVar(value=default_data.tab_path)
        self.tab_data = read_tab_file(self.tab_file_path_str.get())
        self.filelist_path_str = tk.StringVar(value=default_data.reaper_filelist)
        self.paths, self.list_data = parse_reaper_filelist(self.filelist_path_str.get())
        self.output_path_str = tk.StringVar(value=default_data.output_path)
        # self.id_regex_str = tk.StringVar(value=default_data.extract_pattern)
        # 新增参数
        self.cd_prefix_str = tk.StringVar(value=default_data.cd_prefix)
        self.cd_regex_str = tk.StringVar(value=default_data.cd_regex)
        self.track_prefix_str = tk.StringVar(value=default_data.track_prefix)
        self.track_regex_str = tk.StringVar(value=default_data.track_regex)
        self.id_prefix_str = tk.StringVar(value=default_data.id_prefix)
        # 创建界面元素
        self.create_widgets()

    def update_lib_keyword(self, *args):
        # 这个函数会在 StringVar 的值变化时调用
        default_data.lib_keyword = self.lib_keyword_str.get()
        print(default_data.lib_keyword)

    def update_tab_path(self, *args):
        # 这个函数会在 StringVar 的值变化时调用
        default_data.tab_path = self.tab_file_path_str.get()
        print(default_data.tab_path)

    def update_filelist_path(self, *args):
        default_data.reaper_filelist = self.filelist_path_str.get()
        print(default_data.reaper_filelist)

    def update_output_path(self, *args):
        default_data.output_path = self.output_path_str.get()
        print(default_data.output_path)

    # def update_id_regex(self, *args):
    #     default_data.extract_pattern = self.id_regex_str.get()
    #     print(default_data.extract_pattern)

    def update_cd_prefix(self, *args):
        default_data.cd_prefix = self.cd_prefix_str.get()
        print(get_path_pattern())

    def update_cd_regex(self, *args):
        default_data.cd_regex = self.cd_regex_str.get()
        print(get_path_pattern())

    def update_track_prefix(self, *args):
        default_data.track_prefix = self.track_prefix_str.get()
        print(get_path_pattern())

    def update_track_regex(self, *args):
        default_data.track_regex = self.track_regex_str.get()
        print(get_path_pattern())

    def update_id_prefix(self, *args):
        default_data.id_prefix = self.id_prefix_str.get()
        print(f'{default_data.id_prefix}0001-01')

    def create_widgets(self):
        # 标签和输入框
        keyword_label = tk.Label(self.root, text="Library Keyword:")
        keyword_label.grid(row=0, column=0, sticky="w")
        self.lib_keyword_str.trace_add("write", self.update_lib_keyword)
        keyword_field = tk.Entry(self.root, textvariable=self.lib_keyword_str)
        keyword_field.grid(row=0, column=1, columnspan=2, sticky="w")

        tk.Label(self.root, text="Tab File Path:").grid(row=1, column=0, sticky="w")
        self.tab_file_path_str.trace_add("write", self.update_tab_path)
        tk.Entry(self.root, textvariable=self.tab_file_path_str).grid(row=1, column=1, columnspan=2, sticky="w")
        tk.Button(self.root, text="Browse", command=self.browse_tab_file).grid(row=1, column=3)

        tk.Label(self.root, text="Reaper Filelist Path:").grid(row=2, column=0, sticky="w")
        self.filelist_path_str.trace_add("write", self.update_filelist_path)
        tk.Entry(self.root, textvariable=self.filelist_path_str).grid(row=2, column=1, columnspan=2, sticky="w")
        tk.Button(self.root, text="Browse", command=self.browse_reaper_filelist).grid(row=2, column=3)

        tk.Label(self.root, text="Output Path:").grid(row=3, column=0, sticky="w")
        self.output_path_str.trace_add("write", self.update_output_path)
        tk.Entry(self.root, textvariable=self.output_path_str).grid(row=3, column=1, columnspan=2, sticky="w")
        tk.Button(self.root, text="Browse", command=self.browse_output_path).grid(row=3, column=3)

        # 按钮
        update_button = tk.Button(self.root, text="Update", command=self.update_filelist)
        update_button.grid(row=6, column=0, columnspan=1)
        write_button = tk.Button(self.root, text="Write", command=self.write_filelist)
        write_button.grid(row=6, column=1, columnspan=1)
        json_button = tk.Button(self.root, text="Write Json", command=self.write_json)
        json_button.grid(row=6, column=2, columnspan=1)
        pickle_button = tk.Button(self.root, text="Write Pickle", command=self.write_pickle)
        pickle_button.grid(row=6, column=3)

        # 新增文本框和标签
        tk.Label(self.root, text="CD Prefix:").grid(row=7, column=0, sticky="w")
        self.cd_prefix_str.trace_add("write", self.update_cd_prefix)
        tk.Entry(self.root, textvariable=self.cd_prefix_str).grid(row=7, column=1, columnspan=2, sticky="w")

        tk.Label(self.root, text="CD Regex:").grid(row=8, column=0, sticky="w")
        self.cd_regex_str.trace_add("write", self.update_cd_regex)
        tk.Entry(self.root, textvariable=self.cd_regex_str).grid(row=8, column=1, columnspan=2, sticky="w")

        tk.Label(self.root, text="Track Prefix:").grid(row=9, column=0, sticky="w")
        self.track_prefix_str.trace_add("write", self.update_track_prefix)
        tk.Entry(self.root, textvariable=self.track_prefix_str).grid(row=9, column=1, columnspan=2, sticky="w")

        tk.Label(self.root, text="Track Regex:").grid(row=10, column=0, sticky="w")
        self.track_regex_str.trace_add("write", self.update_track_regex)
        tk.Entry(self.root, textvariable=self.track_regex_str).grid(row=10, column=1, columnspan=2, sticky="w")

        tk.Label(self.root, text="FileID Prefix:").grid(row=11, column=0, sticky="w")
        self.id_prefix_str.trace_add("write", self.update_id_prefix)
        tk.Entry(self.root, textvariable=self.id_prefix_str).grid(row=11, column=1, columnspan=2, sticky="w")

    def browse_tab_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Tab Files", "*.tab")])
        if file_path:
            self.tab_file_path_str.set(file_path)
            self.tab_data = read_tab_file(self.tab_file_path_str.get())

    def browse_reaper_filelist(self):
        file_path = filedialog.askopenfilename(filetypes=[('Reaper Filelist Files', "*.ReaperFileList")])
        if file_path:
            self.filelist_path_str.set(file_path)
            self.paths, self.list_data = parse_reaper_filelist(self.filelist_path_str.get())

    def browse_output_path(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".ReaperFileList",
                                                 filetypes=[("Reaper Filelist Files", "*.ReaperFileList")])
        if file_path:
            self.output_path_str.set(file_path)

    def update_filelist(self):
        update_reaper_filelist(self.list_data, self.tab_data)

    def write_json(self):
        save_to_json(default_data.json_path, self.paths, self.list_data)

    def write_pickle(self):
        save_to_pickle(default_data.pickle_path, self.paths, self.list_data)

    def write_filelist(self):
        write_reaper_filelist(self.paths, self.list_data, self.output_path_str.get())

