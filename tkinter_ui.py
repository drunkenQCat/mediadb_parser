import tkinter as tk
from tkinter import filedialog
import default_data
from tab_reader import read_tab_file
from filelist_parser import parse_reaper_filelist
from filelist_parser import save_to_json
from filelist_updater import update_reaper_filelist
from filelist_writer import write_reaper_filelist

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
        self.id_regex_str = tk.StringVar(value=default_data.extract_pattern)

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
    # 这个函数会在 StringVar 的值变化时调用
        default_data.reaper_filelist = self.filelist_path_str.get()
        print(default_data.reaper_filelist)

    def update_output_path(self, *args):
    # 这个函数会在 StringVar 的值变化时调用
        default_data.output_path = self.output_path_str.get()
        print(default_data.output_path)
    
    def update_id_regex(self, *args):
        default_data.extract_pattern = self.id_regex_str.get()
        print(default_data.extract_pattern)

    def create_widgets(self):
        # 标签和输入框
        tk.Label(self.root, text="Library Keyword:").grid(row=0, column=0, sticky="w")
        self.lib_keyword_str.trace_add("write",self.update_lib_keyword)
        tk.Entry(self.root, textvariable=self.lib_keyword_str).grid(row=0, column=1, columnspan=2, sticky="w")

        tk.Label(self.root, text="Tab File Path:").grid(row=1, column=0, sticky="w")
        self.tab_file_path_str.trace_add("write",self.update_tab_path)
        tk.Entry(self.root, textvariable=self.tab_file_path_str).grid(row=1, column=1, columnspan=2, sticky="w")
        tk.Button(self.root, text="Browse", command=self.browse_tab_file).grid(row=1, column=3)

        tk.Label(self.root, text="Reaper Filelist Path:").grid(row=2, column=0, sticky="w")
        self.filelist_path_str.trace_add("write",self.update_filelist_path)
        tk.Entry(self.root, textvariable=self.filelist_path_str).grid(row=2, column=1, columnspan=2, sticky="w")
        tk.Button(self.root, text="Browse", command=self.browse_reaper_filelist).grid(row=2, column=3)

        tk.Label(self.root, text="Output Path:").grid(row=3, column=0, sticky="w")
        self.output_path_str.trace_add("write",self.update_output_path)
        tk.Entry(self.root, textvariable=self.output_path_str).grid(row=3, column=1, columnspan=2, sticky="w")
        tk.Button(self.root, text="Browse", command=self.browse_output_path).grid(row=3, column=3)

        tk.Label(self.root, text="ID Regex:").grid(row=4, column=0, sticky="w")
        self.id_regex_str.trace_add("write",self.update_id_regex)
        regex_area = tk.Entry(self.root, textvariable=self.id_regex_str)
        regex_area.grid(row=4, column=1, columnspan=2, rowspan=2, sticky="w")
        # 按钮
        update_button = tk.Button(self.root, text="Update", command=self.update_filelist)
        update_button.grid(row=6, column=0, columnspan=1)
        write_button = tk.Button(self.root, text="Write", command=self.write_filelist)
        write_button.grid(row=6, column=1, columnspan=1)
        json_button = tk.Button(self.root, text="Write Json", command=self.write_json)
        json_button.grid(row=6, column=2, columnspan=2)


    def browse_tab_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Tab Files", "*.tab")])
        if file_path:
            self.tab_file_path_str.set(file_path)
            self.tab_data = read_tab_file(self.tab_file_path_str.get())

    def browse_reaper_filelist(self):
        file_path = filedialog.askopenfilename(filetypes=[("Reaper Filelist Files", "*.ReaperFileList")])
        if file_path:
            self.filelist_path_str.set(file_path)
            self.paths, self.list_data = parse_reaper_filelist(self.filelist_path_str.get())

    def browse_output_path(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".ReaperFileList", filetypes=[("Reaper Filelist Files", "*.ReaperFileList")])
        if file_path:
            self.output_path_str.set(file_path)

    def update_filelist(self):
        update_reaper_filelist(self.list_data, self.tab_data)

    def write_json(self):
        save_to_json(default_data.json_path, self.paths, self.list_data)

    def write_filelist(self):
        write_reaper_filelist(self.paths, self.list_data, self.output_path_str.get())

