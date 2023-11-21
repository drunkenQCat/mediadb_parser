import tkinter as tk
from tkinter import filedialog
from default_data import lib_keyword
from tab_reader import read_tab_file
from filelist_parser import read_or_parse_reaper_filelist
from filelist_updater import update_reaper_filelist
from filelist_writer import write_updated_reaper_filelist

class MyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Reaper Filelist Updater")

        # 初始化参数
        self.lib_keyword_str = tk.StringVar(value=lib_keyword)
        self.tab_file_path = tk.StringVar()
        self.reaper_filelist_path = tk.StringVar()
        self.output_path = tk.StringVar()

        # 创建界面元素
        self.create_widgets()

    def update_external_parameter(self, *args):
    # 这个函数会在 StringVar 的值变化时调用
        lib_keyword = self.lib_keyword_str.get()
        print(lib_keyword)

    def create_widgets(self):
        # 标签和输入框
        tk.Label(self.root, text="Library Keyword:").grid(row=0, column=0, sticky="w")
        self.lib_keyword_str.trace_add("write",self.update_external_parameter)
        tk.Entry(self.root, textvariable=self.lib_keyword_str).grid(row=0, column=1, columnspan=2, sticky="w")

        tk.Label(self.root, text="Tab File Path:").grid(row=1, column=0, sticky="w")
        tk.Entry(self.root, textvariable=self.tab_file_path).grid(row=1, column=1, columnspan=2, sticky="w")
        tk.Button(self.root, text="Browse", command=self.browse_tab_file).grid(row=1, column=3)

        tk.Label(self.root, text="Reaper Filelist Path:").grid(row=2, column=0, sticky="w")
        tk.Entry(self.root, textvariable=self.reaper_filelist_path).grid(row=2, column=1, columnspan=2, sticky="w")
        tk.Button(self.root, text="Browse", command=self.browse_reaper_filelist).grid(row=2, column=3)

        tk.Label(self.root, text="Output Path:").grid(row=3, column=0, sticky="w")
        tk.Entry(self.root, textvariable=self.output_path).grid(row=3, column=1, columnspan=2, sticky="w")
        tk.Button(self.root, text="Browse", command=self.browse_output_path).grid(row=3, column=3)

        # 按钮
        tk.Button(self.root, text="Update Filelist", command=self.update_filelist).grid(row=4, column=0, columnspan=4, pady=10)

    def browse_tab_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Tab Files", "*.tab")])
        if file_path:
            self.tab_file_path.set(file_path)
            self.tab_data = read_tab_file(self.tab_file_path.get())

    def browse_reaper_filelist(self):
        file_path = filedialog.askopenfilename(filetypes=[("Reaper Filelist Files", "*.ReaperFileList")])
        if file_path:
            self.reaper_filelist_path.set(file_path)
            self.paths, self.list_data = read_or_parse_reaper_filelist(self.reaper_filelist_path.get())

    def browse_output_path(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".ReaperFileList", filetypes=[("Reaper Filelist Files", "*.ReaperFileList")])
        if file_path:
            self.output_path.set(file_path)

    def update_filelist(self):
        # 在这里调用你的更新函数，使用 self.lib_keyword.get(), self.tab_file_path.get(), self.reaper_filelist_path.get(), self.output_path.get()
        update_reaper_filelist(self.tab_data, self.list_data)
        write_updated_reaper_filelist(self.paths, self.list_data, self.output_path.get())

