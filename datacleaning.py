# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 20:31:57 2020

@author: qyk
"""

# data cleaning 
# refresh the string number to float except 2019
import json
import os


def is_num_by_except(string):
    try:
        num_float = float(string)
        return num_float
    except ValueError:
        return string
    

def refresh_json(file_name):
    data = []
    with open(file_name,'r') as f:
        for line in f.readlines():
            data.append(json.loads(line))
    for dic in data:
        for key, value in dic.items():
            if value == 2019:
                continue
            if value == None:
                continue
            else:
                dic[key] = is_num_by_except(value)
    with open(file_name,'w') as outf:
        for di in data:
            outf.write(json.dumps(di)+'\n')
            
            
def _test_refresh_json():
    test_file = [{'年份':2019,'最低分':'342'},
                 {'年份':2019,'最低分':'342','科类':"理工"}]

    for dic in test_file:
        for key, value in dic.items():
            if value == 2019:
                continue
            else:
                dic[key] = is_num_by_except(value)
    return test_file

#%%
# get all the json file list
prepath = [r'C:\Myfile\File\学业资料\测评产品\Data\二批抓取']

def _search_file(prepath):
    file_list = []
    dir_list = os.listdir(prepath)
    for d in dir_list:
        dir_path = os.path.join(prepath,d)
        file_name = os.listdir(dir_path)
        
        file_path = [os.path.join(dir_path,f) for f in file_name if f.endswith(".json")]
        file_list.extend(file_path)
    return file_list

file_list = []
for p in prepath:
    file_list.extend(_search_file(p))

#%%
for i,file in enumerate(file_list):
    refresh_json(file)
    if i % 100 == 0:
        print(i)
        
    