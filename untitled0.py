# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 17:16:59 2020

@author: qyk
"""

import json

data = []
with open("""C:\\Myfile\\File\\学业资料\\测评产品\\Data\\raw\\哈尔滨工程大学/raw_admission_info@哈尔滨工程大学2019年辽宁本科一批录取分数线.json""",'r') as f:
    for line in f.readlines():
        dic = json.loads(line)
        data.append(dic)
f.close()
#%%
import json
with open(r"""C:\Myfile\File\学业资料\测评产品/raw_scoreline_url_data@20200405.json""",'r') as f:
     title_url = json.load(f)

url = title_url.pop('陕西师范大学2019年西藏/南疆国家专项录取分数线')
title_url['陕西师范大学2019年西藏南疆国家专项录取分数线'] = url

with open("""C:\Myfile\File\学业资料\测评产品/scoreline_title_url.json""",'w') as outf:
    outf.write(json.dumps(title_url))
outf.close()

#%%
school = [s.split('2019')[0] for s in school]  # 提取出每个title 属于的学校或者学院字符串
school  = list(set(school))

#%%

school_url ={}
for s in school:
    for ttt in title_url.keys():
        if s in ttt:
            school_url[s] = title_url[ttt]
            break
        
#%%
for x in third_crawl_resiude:
    if '天津师范大学' in x:
        print(third_crawl_resiude.index(x))
        
del school_url['福州大学']

#%%
output_file = os.path.join('C:\Myfile\File\学业资料\测评产品\Data','剩余学校.json')
outf = open(output_file, 'w')
outf.write(json.dumps(residue_school))
outf.close()
#%%
school_crawl = []
for i in school:
    if i not in school_residue:
        school_crawl.append(i)
        
#%%
with open(r'C:\Myfile\File\学业资料\测评产品\Data\raw\哈尔滨工程大学/raw_admission_info@哈尔滨工程大学2019年吉林本科一批录取分数线.json','r') as load_g:
    guizhou = json.load(load_g)

#%%
# 2.5 seconde residue 
tmp_residue = second_crawl_residue[1395:]
second_plus_residue = list(second_crawl_residue[1395:])
for spr in tmp_residue:
    if '厦门工学院' in spr:
        second_plus_residue.remove(spr)
for tl in second_plus_residue:
    tr = get_admission_img(tl,title_url[tl])
    if tr:
        third_crawl_resiude.append(tl)
#%%
# 2.75 second residue
tmp_residue = second_crawl_residue[1944:]
second_ultra_residue = list(second_crawl_residue[1944:])
for spr in tmp_residue:
    if '延安大学' in spr:
        second_ultra_residue.remove(spr)
for tl in second_ultra_residue:
    tr = get_admission_img(tl,title_url[tl])
    if tr:
        third_crawl_resiude.append(tl)
#%%
import json
import numpy as np
all_url = 'C:\Myfile\File\学业资料\测评产品\scoreline_title_url.json'
with open(all_url,'r') as f:
    title_url = json.load(f)

residue_title = np.load(r'C:\Myfile\File\学业资料\测评产品\Data\crawl_log/third_crawl_residue.npy')

outf = open('C:\Myfile\File\学业资料\测评产品\Data\crawl_log/third_crawl_residue_url','wb')
for i in residue_title:
    i = i.decode()
    tmp = dict(zip(i, title_url[i]))

    outf.write(json.dumps(tmp)+'\n')
outf.close()
    
#%%     
def add(x,y):
    return x+y

def f_add(k,x,y,method):
    return k*method(x,y)
print(f_add(3,1,2,add))


#%%
line1 = {'年份':2019,'省份':'黑龙江','批次':'本科一批',"学校":"吉林大学","科类":"理工","最低分":590}
line2 = {'年份':2019,'省份':'黑龙江','批次':'本科一批',"学校":"吉林大学","科类":"文史","最低分":557}
with open("""C:\\Myfile\\File\\学业资料\\测评产品\\Data\\raw\\哈尔滨工程大学/raw_admission_info@哈尔滨工程大学2019年黑龙江本科一批录取分数线.json""",'w') as f:
    f.write(json.dumps(line1)+'\n')
    #f.write(json.dumps(line2)+'\n')
#%%
import json
outf = open(r'C:\Myfile\File\学业资料\测评产品\Data\raw\山东青年政治学院/raw_admission_info@山东青年政治学院2019年艺术类专业录取分数线.json','w')
data = [{'年份': 2019, '学校': '山东青年政治学院', '省份':'山东', '科类': '艺文', '批次': '本科', '专业':'播音与主持艺术', '文化课最高分':521.0, '文化课最低分': 426.0, '专业最高分': 185.73,'专业最低分':169.07},
        {'年份': 2019, '学校': '山东青年政治学院', '省份':'山东', '科类': '艺理', '批次': '本科', '专业':'播音与主持艺术',  '文化课最高分':467.0, '文化课最低分': 396.0, '专业最高分': 184.40,'专业最低分':169.60},
        {'年份': 2019, '学校': '山东青年政治学院', '省份':'四川', '科类': '艺术', '批次': '本科',  '专业':'播音与主持艺术', '文化课最高分':481.0, '文化课最低分': 376.0, '专业最高分': 241.60,'专业最低分':229.60},
        {'年份': 2019, '学校': '山东青年政治学院', '省份':'河南', '科类': '文科', '批次': '本科',  '专业':'播音与主持艺术', '文化课最高分':428.0, '文化课最低分': 388.0, '专业最高分': 332.60,'专业最低分':306.0},
        {'年份': 2019, '学校': '山东青年政治学院', '省份':'安徽', '科类': '艺术', '批次': '本科',  '专业':'播音与主持艺术', '文化课最高分':517.0, '文化课最低分': 440.0, '专业最高分': 249.46,'专业最低分':180.14},
        {'年份': 2019, '学校': '山东青年政治学院', '省份':'山东', '科类': '艺文', '批次': '本科',   '专业':'音乐与舞蹈','文化课最高分':457.0, '文化课最低分': 326.0, '专业最高分': 163.39,'专业最低分':148.03},
        {'年份': 2019, '学校': '山东青年政治学院', '省份':'山东', '科类': '艺理', '批次': '本科',  '专业':'音乐与舞蹈','文化课最高分':424.0, '文化课最低分': 290.0, '专业最高分': 157.23,'专业最低分':152.10},
        {'年份': 2019, '学校': '山东青年政治学院', '省份':'江西', '科类': '艺文', '批次': '本科', '专业':'音乐与舞蹈', '文化课最高分':426.0, '文化课最低分': 294.0, '专业最高分': 170.77,'专业最低分':163.14},
        {'年份': 2019, '学校': '山东青年政治学院', '省份':'四川', '科类': '艺文', '批次': '本科', '专业':'音乐与舞蹈', '文化课最高分':436.0, '文化课最低分': 327.0, '专业最高分': 336.77,'专业最低分':329.8},
        {'年份': 2019, '学校': '山东青年政治学院', '省份':'河北', '科类': '艺术', '批次': '本科', '专业':'音乐与舞蹈', '文化课最高分':409.0, '文化课最低分': 290.0, '专业最高分': 158.0,'专业最低分':137.0},
        {'年份': 2019, '学校': '山东青年政治学院', '省份':'河南', '科类': '艺术', '批次': '本科', '专业':'音乐与舞蹈', '文化课最高分':405.0, '文化课最低分': 367.0, '专业最高分': 92.0,'专业最低分':84.0},
        {'年份': 2019, '学校': '山东青年政治学院', '省份':'安徽', '科类': '艺术', '批次': '本科', '专业':'音乐与舞蹈', '文化课最高分':476.0, '文化课最低分': 333.0, '专业最高分': 151.32,'专业最低分':141},
        {'年份': 2019, '学校': '山东青年政治学院', '省份':'甘肃', '科类': '艺术', '批次': '本科', '专业':'音乐与舞蹈', '文化课最高分':425.0, '文化课最低分': 279.0, '专业最高分': 229.0,'专业最低分':228.3},
        {'年份': 2019, '学校': '山东青年政治学院', '省份':'山东', '科类': '艺文', '批次': '本科', '专业':'设计学类', '文化课最高分':494.0, '文化课最低分': 327.0, '专业最高分': 256.0,'专业最低分':223.0},
        {'年份': 2019, '学校': '山东青年政治学院', '省份':'山东', '科类': '艺理', '批次': '本科', '专业':'设计学类', '文化课最高分':437.0, '文化课最低分': 293.0, '专业最高分': 251.0,'专业最低分':226.0},
        {'年份': 2019, '学校': '山东青年政治学院', '省份':'河北', '科类': '艺术', '批次': '本科', '专业':'设计学类', '文化课最高分':417.0, '文化课最低分': 296.0, '专业最高分': 248.7,'专业最低分':187.0},
        {'年份': 2019, '学校': '山东青年政治学院', '省份':'河南', '科类': '艺术', '批次': '本科', '专业':'设计学类', '文化课最高分':389.0, '文化课最低分': 354.0, '专业最高分': 251.0,'专业最低分':211.0}]
for d in data:
    outf.write(json.dumps(d)+'\n')
#%%

outf = open(r'C:\Myfile\File\学业资料\测评产品\Data\raw\莆田学院/raw_admission_info@莆田学院2019年福建省录取分数线.json','w')
data = [{'年份':2019,'学校':'莆田学院',"批次":"本科二批","省份":"福建","科类":"文史","最低分":514.0},
        {'年份':2019,'学校':'莆田学院',"批次":"本科二批","省份":"福建","科类":"理工","最低分":443.0},
        {'年份':2019,'学校':'莆田学院',"批次":"本科一批","省份":"福建","科类":"理工","最低分":493.0},
        {'年份':2019,'学校':'莆田学院',"批次":"本科批","省份":"福建", "科类":"体育文",  "最低分":572.0},
        {'年份':2019,'学校':'莆田学院',"批次":"本科批","省份":"福建", "科类":"体育理", "最低分":547.0},
        {'年份':2019,'学校':'莆田学院',"批次":"本科提前批","省份":"福建", "科类":"文史", "最低分":572.0},
        {'年份':2019,'学校':'莆田学院',"批次":"本科提前批","省份":"福建", "科类":"理工", "最低分":547.0},
        ]
for d in data:
    outf.write(json.dumps(d)+'\n')