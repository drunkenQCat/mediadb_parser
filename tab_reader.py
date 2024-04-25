# -*- coding: utf-8 -*-
import csv


def read_tab_file(tab_file_path):
    tab_data = {}
    with open(tab_file_path, 'r', encoding='utf8') as tab_file:
        csv_reader = csv.reader(tab_file)
        for line in csv_reader:
            wav_metadata = {}
            file_id = line[2]
            wav_metadata["title"] = line[0]
            wav_metadata["desc"] = line[1]
            tab_data[file_id] = wav_metadata
    return tab_data
