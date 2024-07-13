## 工程结构

```
├── docs                    各类文档
├── requirements.txt        依赖项列表
├── default.ReaperFileList  占位用ReaperFileList文件
├── default.tab             占位用tab文件
├── main.py                 程序入口
├── default_data.py         用于保存界面中的默认数据
├── filelist_parser.py      ReaperFileList解析器
├── filelist_updater.py     用于按照tab或csv文件更新条目
├── filelist_writer.py      用于输出文件
├── tab_path_comparor.py    一个使用nlp方法比较文件路径与tab条目的尝试，并没有用到程序中
├── tab_reader.py           用于读取tab以及csv
└── tkinter_ui.py           程序图形化界面
```

### 程序工作流程概述

这个程序的主要任务是解析ReaperFileList和TAB文件，并利用TAB文件中的描述信息更新ReaperFileList中的相应条目。最终，将更新后的ReaperFileList写入一个新的文件，并显示前100行内容供用户预览。

### ReaperFileList的结构

ReaperFileList文件包含以下几种行：
1. **PATH行**: 指示要扫描的文件夹路径。
2. **FILE行**: 列出具体文件的路径及其元数据。
3. **DATA行**: 包含音频文件的各类元数据。

例如：
```
PATH "W:\06.Sound.Bank.Sound.Effects\Sony.Complete.Sound.FX.Library-SoSISO"
FILE "W:\06.Sound.Bank.Sound.Effects\Sony.Complete.Sound.FX.Library-SoSISO\CD10\Track01.wav" 30688016 0 1714504588 0
DATA t:SPACESHIP "C:SPACESHIP : HATCH CLOSING" "D:SPACESHIP : HATCH CLOSING" s:44100
DATA n:2 l:2:53.946 i:16
```

### TAB文件的结构

TAB文件的表头如下：
```
| CD编号（一般为库名-序号，例如DIGI-D-15） | 文件序号（例如01） | 音效片段序号（一个文件中有多个音效时使用，一般为01） | 描述 | 时长 |
```
每一行代表一个音效片段的信息，包括CD编号、文件序号、音效片段序号、描述和时长。

### 解析TAB文件

1. **读取TAB文件**:
   - 打开TAB文件，逐行读取内容。
   - 将每一行根据制表符拆分为多个字段，并将其存储到一个词典中。
   - 词典的键是“CD编号-文件序号-音效片段序号”，值是包含描述和时长的字典。

### 匹配和更新ReaperFileList条目

1. **解析ReaperFileList文件**:
   - 打开ReaperFileList文件，逐行读取内容。
   - 根据不同的行类型（PATH、FILE、DATA）进行解析，存储到相应的数据结构中。

2. **匹配和更新描述信息**:
   - 遍历解析后的ReaperFileList数据，找到每个FILE行对应的DATA行。
   - 使用TAB文件中解析出的词典，根据文件路径中的CD编号和文件序号匹配对应的描述信息。
   - 更新DATA行中的描述字段。

### 输出文件

1. **写入新的ReaperFileList文件**:
   - 将更新后的ReaperFileList数据写入一个新的文件中。
   - 在写入过程中保持原有的格式，包括PATH、FILE和DATA行的顺序和结构。

2. **预览前100行内容**:
   - 将更新后的ReaperFileList文件的前100行内容显示在GUI的文本框中，供用户预览和检查。

### 代码中的关键位置

1. **读取TAB文件**:
   - 在`tab_reader.py`中的`read_tab_file`函数实现。

2. **解析ReaperFileList文件**:
   - 在`filelist_parser.py`中的相关函数实现，如`parse_reaper_filelist`。

3. **匹配和更新描述信息**:
   - 在`filelist_updater.py`中的`update_reaper_filelist`函数实现。

4. **写入新的ReaperFileList文件**:
   - 在`filelist_writer.py`中的`write_reaper_filelist`函数实现。

5. **GUI操作和预览**:
   - 在`main.py`中的`write_output_file`函数和相关GUI事件处理函数中实现。

通过上述步骤和流程，程序能够有效地解析TAB文件和ReaperFileList文件，更新描述信息，并输出更新后的ReaperFileList文件供用户使用。