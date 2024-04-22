# -*- coding: utf-8 -*-
import os
import re
import glob
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import default_data
from tab_reader import read_tab_file
from filelist_parser import convert_to_lib_path_structure, parse_reaper_filelist, read_reaper_filelist
from filelist_parser import save_to_json
from filelist_updater import update_reaper_filelist
from filelist_writer import write_reaper_filelist, overwrite_file_list


def get_path_pattern():
    # 示例用法
    # file_path = 'the parent path\\6000 Extension III\\CD 6071\\29.wav'
    # result = extract_serial_number(file_path) -------6071-29
    cd_pattern = r'.*\\' + f'{default_data.cd_prefix}({default_data.cd_regex})'
    track_pattern = r'.*\\' + f'{default_data.track_prefix}({default_data.track_regex})'
    ending_pattern = r'.*\.(WAV|wav|Wav|mp3)'
    pattern = cd_pattern + track_pattern + ending_pattern
    return pattern


def display_head_and_tail(file_path):
    file_head_tail = "Head 10 lines\n"
    with open(file_path, "r", encoding='utf-8') as file:
        for _ in range(10):
            line = file.readline()
            if not line:
                break  # 如果文件已经读取完毕，则跳出循环
            file_head_tail += line.strip() + '\n'  # 使用strip()方法去除行尾的换行符
        file_head_tail += "Tail 10 lines\n"
        lines_rest = file.readlines()
        last_10_lines = lines_rest[-10:]
        for line in last_10_lines:
            file_head_tail += line.strip() + '\n'  # 使用strip()方法去除行尾的换行符
    messagebox.showinfo(f"Write Done", f"File head and tail:\n{file_head_tail}")


class MyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Reaper Filelist Updater")

        # 初始化参数
        self.lib_keyword_str = tk.StringVar(value=default_data.lib_keyword)
        self.album_str = tk.StringVar(value=default_data.album)
        self.tab_file_path_str = tk.StringVar(value=default_data.tab_path)
        self.tab_data = read_tab_file(self.tab_file_path_str.get())
        self.filelist_path_str = tk.StringVar(value=default_data.reaper_filelist)

        self.paths, self.list_data = parse_reaper_filelist(self.filelist_path_str.get())
        self.list_data_library_to_file = convert_to_lib_path_structure(self.list_data)

        self.output_path_str = tk.StringVar(value=default_data.output_path)
        # self.id_regex_str = tk.StringVar(value=default_data.extract_pattern)
        # 新增参数
        self.cd_prefix_str = tk.StringVar(value=default_data.cd_prefix)
        self.cd_regex_str = tk.StringVar(value=default_data.cd_regex)
        self.track_prefix_str = tk.StringVar(value=default_data.track_prefix)
        self.track_regex_str = tk.StringVar(value=default_data.track_regex)
        self.id_prefix_str = tk.StringVar(value=default_data.id_prefix)
        self.full_regex_str = tk.StringVar(value='')
        self.full_regex_str.set(get_path_pattern())
        default_data.full_regex = self.full_regex_str.get()
        # 创建界面元素
        self.create_widgets()


    def update_all_paths_with_lib_key(self):
        tab_file_folder = r"C:\Users\Administrator\Documents\Injector\TABS"
        mediadb_folder = r"C:\REAPER\MediaDB"
        key = default_data.lib_keyword
        mediadb_path = os.path.join(mediadb_folder, key + ".ReaperFileList")

        # 优化关键词处理，以支持更灵活的关键词匹配
        abbr = key.split("-")[0]
        words_in_key = key.split("-")[1].replace('.', ' ').split()
        reg_to_find_tab = ".*" + ".*".join(words_in_key) + ".*\\.tab$"

        # 使用 glob 搜索匹配的 TAB 文件
        tab_files = glob.glob(os.path.join(tab_file_folder, '**', '*.tab'), recursive=True)
        matched_tab_path = next((f for f in tab_files if re.match(reg_to_find_tab, os.path.basename(f), re.IGNORECASE)),
                                None)

        if matched_tab_path:
            self.tab_file_path_str.set(matched_tab_path)
            self.tab_data = read_tab_file(matched_tab_path)
        else:
            print("No matching TAB file found.")

        # 设置和验证 MediaDB 路径
        self.filelist_path_str.set(mediadb_path)
        if not os.path.exists(mediadb_path):
            print(f"MediaDB path {mediadb_path} does not exist.")
        else:
            self.paths, self.list_data = read_reaper_filelist(self.filelist_path_str.get())
            display_head_and_tail(matched_tab_path)
            display_head_and_tail(mediadb_path)
            self.id_prefix_str.set(abbr)

    def update_lib_keyword(self, *args):
        # 这个函数会在 StringVar 的值变化时调用
        default_data.lib_keyword = self.lib_keyword_str.get()
        self.album_str.set(default_data.lib_keyword)
        default_data.album = default_data.lib_keyword
        print(default_data.lib_keyword)

    def update_album(self, *args):
        # 这个函数会在 StringVar 的值变化时调用
        default_data.album = self.album_str.get()
        print(default_data.album)

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
        self.full_regex_str.set(get_path_pattern())
        self.update_regex()

    def update_cd_regex(self, *args):
        default_data.cd_regex = self.cd_regex_str.get()
        self.full_regex_str.set(get_path_pattern())
        self.update_regex()

    def update_track_prefix(self, *args):
        default_data.track_prefix = self.track_prefix_str.get()
        self.full_regex_str.set(get_path_pattern())
        self.update_regex()

    def update_track_regex(self, *args):
        default_data.track_regex = self.track_regex_str.get()
        self.full_regex_str.set(get_path_pattern())
        self.update_regex()

    def update_id_prefix(self, *args):
        default_data.id_prefix = self.id_prefix_str.get()
        print(f'{default_data.id_prefix}01-01')

    def update_regex(self, *args):
        default_data.full_regex = self.full_regex_str.get()
        print(default_data.full_regex)

    def create_widgets(self):
        # 标签和输入框
        keyword_label = tk.Label(self.root, text="Library Keyword:")
        keyword_label.grid(row=0, column=0, sticky="w")
        self.lib_keyword_str.trace_add("write", self.update_lib_keyword)
        keyword_field = tk.Entry(self.root, textvariable=self.lib_keyword_str)
        keyword_field.grid(row=0, column=1, columnspan=2, sticky="w")
        # 新增按钮，用于触发路径更新
        update_paths_button = tk.Button(self.root, text="Update Paths", command=self.update_all_paths_with_lib_key)
        update_paths_button.grid(row=0, column=3)

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
        json_button = tk.Button(self.root, text="Save Json", command=self.write_json)
        json_button.grid(row=6, column=2, columnspan=1)
        refresh_button = tk.Button(self.root, text="Refresh Data", command=self.refresh_data)
        refresh_button.grid(row=6, column=3)

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

        tk.Label(self.root, text="Album").grid(row=12, column=0, sticky="w")
        self.album_str.trace_add("write", self.update_album)
        tk.Entry(self.root, textvariable=self.album_str).grid(row=12, column=1, columnspan=2, sticky="w")

        tk.Label(self.root, text="Full Regex").grid(row=13, column=0, sticky="w")
        self.full_regex_str.trace_add("write", self.update_regex)
        tk.Entry(self.root, textvariable=self.full_regex_str).grid(row=13, column=1, columnspan=2, sticky="w")

        # 创建一个居中的按钮
        overwrite_button = tk.Button(self.root, text="OverWrite Original", command=self.overwrite_filelist)
        overwrite_button.grid(row=14, sticky="nsew", columnspan=4)

    def browse_tab_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Tab Files", "*.tab")])
        if file_path:
            self.tab_file_path_str.set(file_path)
            self.tab_data = read_tab_file(self.tab_file_path_str.get())
            display_head_and_tail(file_path)

    def browse_reaper_filelist(self):
        file_path = filedialog.askopenfilename(filetypes=[('Reaper Filelist Files', "*.ReaperFileList")])
        if file_path:
            self.filelist_path_str.set(file_path)
            self.paths, self.list_data = parse_reaper_filelist(self.filelist_path_str.get())
            display_head_and_tail(file_path)
            save_to_json(default_data.json_path, self.paths, self.list_data)

    def browse_output_path(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".ReaperFileList",
                                                 filetypes=[("Reaper Filelist Files", "*.ReaperFileList")])
        if file_path:
            self.output_path_str.set(file_path)

    def update_filelist(self):
        message = update_reaper_filelist(self.list_data, self.tab_data)
        self.write_json()
        messagebox.showinfo("FileList Updated", message)

    def write_json(self):
        save_to_json(default_data.json_path, self.paths, self.list_data)

    def refresh_data(self):
        file_path = self.filelist_path_str.get()
        self.paths, self.list_data = read_reaper_filelist(file_path)
        self.write_json()
        display_head_and_tail(file_path)

    def write_filelist(self):
        write_reaper_filelist(self.paths, self.list_data, self.output_path_str.get())
        # 预览前100行结果
        file_path = self.output_path_str.get()
        hundred_lines = ""

        with open(file_path, "r", encoding='utf-8') as file:
            for _ in range(100):
                line = file.readline()
                if not line:
                    break  # 如果文件已经读取完毕，则跳出循环
                hundred_lines += line.strip() + '\n'  # 使用strip()方法去除行尾的换行符
        messagebox.showinfo(f"Write Done", f"First Hundred Lines:\n{hundred_lines}")

    def overwrite_filelist(self):
        overwrite_file_list(self.output_path_str.get(), self.filelist_path_str.get())

