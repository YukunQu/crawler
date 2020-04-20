# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 15:32:46 2020

@author: qyk
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Apr 10 09:16:01 2020

@author: qyk
"""
import re
import os
import copy
import json
import requests
import numpy as np

from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36",
}

#%%
def _get_title_info(title):
    title_info = {}
    title_info['年份'] = 2019
    title = title.split('2019')
    
    local_list = ['北京', '天津', '上海', '重庆', '河北', '河南', '山东', 
                  '山西', '安徽', '江西', '江苏', '浙江', '湖北', '湖南', 
                  '广东', '广西', '云南', '贵州', '四川', '陕西', '青海', 
                  '宁夏', '黑龙江', '吉林', '辽宁', '西藏', '新疆', '内蒙古', 
                  '海南', '福建', '甘肃', '港澳台']
    title_info['学校'] = title[0]
    for local in local_list:
        if local in title[1]:
            title_info['省份'] = local    
    
    title_info['科类'] = ''
    discipline_list = ['理工','文史','艺术','体育','综合']
    for discipline in discipline_list:
        if discipline in title[1]:
            title_info['科类'] = discipline
    
    title_info['批次'] = ''
    grade_list = ['本科','本科普通批','一本','本科一批','一批本科','二本','本科批'
            '本科二批','二批本科','国家专项','提前批','高校专项','预科','医学类',
            '本科A批']
    for grade in grade_list:
        if grade in title[1]:
            if grade in ['一本','本科一批','一批本科']:
                title_info['批次'] = '本科一批'
            elif grade in ['二本','本科二批','二批本科','本二批']:
                title_info['批次'] = '本科二批'
            else:
                title_info['批次'] = grade
    return title_info


def get_admission_info(title,url,method):
    uncrawl = False
    # get school information from title
    title_info = _get_title_info(title)
    
    # create dir and open file
    prepath = 'C:\Myfile\File\学业资料\测评产品\Data/raw'
    dire = os.path.join(prepath,title_info['学校'])
    if not os.path.exists(dire):
        os.mkdir(dire)
    file_name = 'raw_admission_info@{}.json'.format(title)
    output_file = os.path.join(dire,file_name) 
    outf = open(output_file, 'w')
    
    # get score information from html table
    resp = requests.request('Get',url,headers=headers)
    if resp.status_code == 200:
        resp.encoding = 'gb2312'
        html_content = resp.text
    else:
        print('{} 404 not found',format(title))
    
    if isinstance(html_content, str):
        soup = BeautifulSoup(html_content,features='html.parser')
        
        # get score table
        print(title,url)
        uncrawl = method(soup, title_info, outf)
    else:
        uncrawl = True
    outf.close()
    if uncrawl:
        print('The data did not be crawled.')
        
    else:
        print('The data was crawled')
    return uncrawl


    
def _huaqiaodaxue(soup,title_info,outf):
    table_content = soup.find_all('table')
    if len(table_content):
        table_content = table_content[0]
        rows = table_content.findAll(lambda tag: tag.name=='tr')
        
        ks = ['最高分','平均分','最低分']
        for i in range(2,len(rows)):
            ds = [td.get_text(strip=True) for td in rows[i].find_all('td')]
            ds = [float(d) for d in ds[2:5]]
            if len(ks) == len(ds):
                tmp = copy.deepcopy(title_info)
                tmp['专业方向'] = None
                tmp.update(dict(zip(ks, ds)))       
                outf.write(json.dumps(tmp)+'\n')
        uncrawl = False
    else:
        uncrawl = True
    return uncrawl


def _xiangongcheng(soup,title_info,outf):
    table_content = soup.find_all('table')
    if len(table_content):
        table_content = table_content[0]
        rows = table_content.findAll(lambda tag: tag.name=='tr')
        
        ks = ['专业方向','科类','录取人数','最低分']
        for i in range(1,len(rows)):
            ds = [td.get_text(strip=True) for td in rows[i].find_all('td')]
            ds[-2] = int(ds[-2])
            ds[-1] = float(ds[-1]) 
            if len(ks) == len(ds):
                tmp = copy.deepcopy(title_info)
                tmp.update(dict(zip(ks, ds)))       
                outf.write(json.dumps(tmp)+'\n') 
        uncrawl = False
    else:
        uncrawl = True
    return uncrawl   
    

def is_num_by_except(string):
    try:
        num_float = float(string)
        return num_float
    except ValueError:
        return None
    

def _xiamendaxue(soup,title_info,outf):
    table_content = soup.find_all('table')
    if len(table_content):
        table_content = table_content[0]
        rows = table_content.findAll(lambda tag: tag.name=='tr')
        for i in range(3,len(rows)):
            ds = [td.get_text(strip=True) for td in rows[i].find_all('td')]
            tmp = copy.deepcopy(title_info)
            tmp['专业方向'] = None
            tmp['科类'] = '文史'
            tmp['最低分'] = is_num_by_except(ds[2])
            outf.write(json.dumps(tmp)+'\n')
            tmp = copy.deepcopy(title_info)
            tmp['专业方向'] = None
            tmp['科类'] = '理工'
            tmp['最低分'] = is_num_by_except(ds[5])
            outf.write(json.dumps(tmp)+'\n')
        uncrawl = False
    else:
        uncrawl = True
    return uncrawl   


def _beijingdierwaiguoyuxueyuan(soup,title_info,outf):
    
    table_content = soup.find_all('table')
    if len(table_content):
        table_content = table_content[0]
        rows = table_content.findAll(lambda tag: tag.name=='tr')
     
        ks = [td.get_text(strip=True) for td in rows[0].find_all('th')]
        if title_info['省份'] == '北京':
            ks = ks[:-1]
        else:
            ks = ks[2:9]
        for i in range(1, len(rows)):
            ds = [td.get_text(strip=True) for td in rows[i].find_all('td')]
            if title_info['省份'] == '北京':
                ds = ds[:-1]
            else:
                ds = ds[2:9]
            ds = [is_num_by_except(d) for d in ds]
            if len(ks)==len(ds):
                # save data
                tmp = copy.deepcopy(title_info)
                tmp.update(dict(zip(ks, ds)))       
                outf.write(json.dumps(tmp)+'\n')
                uncrawl = False
            else:
                uncrawl = True      
    else:
        uncrawl = True  
    return uncrawl

def _zhongguohaiyangdaxue(soup,title_info,outf):
    table_content = soup.find_all('table')
    if len(table_content):
        table_content = table_content[0]
        rows = table_content.findAll(lambda tag: tag.name=='tr')
        ks = [td.get_text(strip=True) for td in rows[0].find_all('td')]
        ks = ks[1:]
        for i in range(2,len(rows)):
            ds = [td.get_text(strip=True) for td in rows[i].find_all('td')]
            tmp = copy.deepcopy(title_info)
            tmp['专业方向'] = None
            tmp['科类'] = '理工/综合改革'
            tmp['最高分'] = is_num_by_except(ds[1])
            tmp['平均分'] = is_num_by_except(ds[2])
            tmp['最低分'] = is_num_by_except(ds[3])
            outf.write(json.dumps(tmp)+'\n')
            tmp = copy.deepcopy(title_info)
            if '文史' in ks:
                tmp['专业方向'] = None
                tmp['科类'] = '文史'
                tmp['最高分'] = is_num_by_except(ds[5])
                tmp['平均分'] = is_num_by_except(ds[6])
                tmp['最低分'] = is_num_by_except(ds[7])
                outf.write(json.dumps(tmp)+'\n')
            else:
                continue
        uncrawl = False
    else:
        uncrawl = True
    return uncrawl   


def _haerbingongchengdaxue(soup,title_info,outf):
    text = soup.find_all('div',{'class':'main'})
    text = text[0].get_text(strip=True)
    num = re.findall('实际录取(.*?)人',text)
    score = re.findall('录取最低分(.*?)分',text)
    kelei = ['理工','文史']
    for n,s,k in zip(num,score,kelei):
        tmp = copy.deepcopy(title_info)
        tmp['专业方向'] = None
        tmp['科类'] = k
        tmp['录取人数'] = n
        tmp['最低分'] = is_num_by_except(s)
        outf.write(json.dumps(tmp)+'\n')
    uncrawl = False
    return uncrawl   


def _dongbeinongyedaxue(soup,title_info,outf):
    uncrawl = False
    table_content = soup.find_all('table')
    if len(table_content):
        table_content = table_content[0]
        rows = table_content.findAll(lambda tag: tag.name=='tr')
        
        ks = [td.get_text(strip=True) for td in rows[0].find_all('td')]
        
        for i in range(2, len(rows)):
            ds = [td.get_text(strip=True) for td in rows[i].find_all('td')]
            ds = [is_num_by_except(d) for d in ds] 
            if len(ks)==len(ds):
                # save data
                tmp = copy.deepcopy(title_info)
                tmp.update(dict(zip(ks, ds)))       
                outf.write(json.dumps(tmp)+'\n')
            else:
                uncrawl = True           
    else:
        uncrawl = True
    return uncrawl


def _fujiangongchengxueyuan(soup,title_info,outf):
    table_content = soup.find_all('table')
    if len(table_content):
        table_content = table_content[0]
        rows = table_content.findAll(lambda tag: tag.name=='tr')
        
        ks = [td.get_text(strip=True) for td in rows[0].find_all('td')]
        ks = ks[-5:]
    
        for i in range(1,len(rows)):
            ds = [td.get_text(strip=True) for td in rows[i].find_all('td')]
            ds = [is_num_by_except(d) for d in ds[-5:]]
            if len(ks) == len(ds):
                tmp = copy.deepcopy(title_info)
                tmp.update(dict(zip(ks, ds)))       
                outf.write(json.dumps(tmp)+'\n')
        uncrawl = False
    else:
        uncrawl = True
    return uncrawl


def _huazhongkejidaxue(soup,title_info,outf):
    table_content = soup.find_all('table')
    if len(table_content):
        table_content = table_content[0]
        rows = table_content.findAll(lambda tag: tag.name=='tr')
        
        ks = [td.get_text(strip=True) for td in rows[0].find_all('td')]
        
        for i in range(1, len(rows)):
            ds = [td.get_text(strip=True) for td in rows[i].find_all('td')]
            if len(ks)==len(ds):
                # save data
                tmp = copy.deepcopy(title_info)
                tmp.update(dict(zip(ks, ds)))       
                outf.write(json.dumps(tmp)+'\n')
            else:
                uncrawl = True           
    else:
            uncrawl = True
    return uncrawl


def _shanghaijidianxueyuan(soup,title_info,outf):
    uncrawl = False
    table_content = soup.find_all('table')
    if len(table_content):
        table_content = table_content[0]
        rows = table_content.findAll(lambda tag: tag.name=='tr')
        
        for i in range(2, len(rows)):
            ds = [td.get_text(strip=True) for td in rows[i].find_all('td')]
            # save data
            tmp = copy.deepcopy(title_info)
            print(ds)
            cengjipilei = ds[1].split('（')
            
            tmp['批次'] = cengjipilei[0]
            print(tmp['批次'])
            tmp['科类'] = cengjipilei[-1].split('）')[0]
            print(tmp['科类'])
            if len(ds) == 5:
                tmp['最低分'] = is_num_by_except(ds[3])
                zhongwaihezuo = is_num_by_except(ds[3])
            else:
                tmp['最低分'] = zhongwaihezuo
            outf.write(json.dumps(tmp)+'\n')        
    else:
            uncrawl = True
    return uncrawl


def _zhongguolaodongguanxixueyuan(soup,title_info,outf):
    uncrawl = False
    table_content = soup.find_all('table')
    if len(table_content):
        table_content = table_content[0]
        rows = table_content.findAll(lambda tag: tag.name=='tr')
        subject =['文史','理工','综合改革']
        for i in range(3, len(rows)):
        
           ds = [td.get_text(strip=True) for td in rows[i].find_all('td')]
           ds = ds[-3:]
           for s,d in zip(subject,ds):
               tmp = copy.deepcopy(title_info)
               tmp['科类'] = s
               try:
                   d = float(d)
               except ValueError:
                   continue
               tmp['最低分'] = d
               outf.write(json.dumps(tmp)+'\n')         
    else:
        uncrawl = True
    return uncrawl


def _qingdaokejidaxue(soup,title_info,outf):
    # get score table
    uncrawl = False
    table_content = soup.find_all('table')
    if len(table_content):
        table_content = table_content[0]
        rows = table_content.findAll(lambda tag: tag.name=='tr')
        
        ks = [td.get_text(strip=True) for td in rows[2].find_all('td')]

        for i in range(3, len(rows)):
            ds = [td.get_text(strip=True) for td in rows[i].find_all('td')]
            if len(ks)==len(ds):
                # save data
                tmp = copy.deepcopy(title_info)
                tmp.update(dict(zip(ks, ds)))       
                outf.write(json.dumps(tmp)+'\n')
            else:
                uncrawl = True           
    else:
        uncrawl = True    
    return uncrawl


def _huananshifandaxue(soup,title_info,outf):
    uncrawl = False
    table_content = soup.find_all('table')
    if len(table_content):
        table_content = table_content[0]
        rows = table_content.findAll(lambda tag: tag.name=='tr')
        subject = ['理工','文史']
        for i in range(3,len(rows)):
            ds = [td.get_text(strip=True) for td in rows[i].find_all('td')]
            for su in subject:
                tmp = copy.deepcopy(title_info)
                tmp['科类'] = su
                if '理工' == su:
                    tmp['最高分'] = ds[1]
                    tmp['最低分'] = ds[2]
                    outf.write(json.dumps(tmp)+'\n')
                else:
                    tmp['最高分'] = ds[3]
                    tmp['最低分'] = ds[4]     
                    outf.write(json.dumps(tmp)+'\n')
    else:
        uncrawl = True
    return  uncrawl


def _beijingnongxueyuan(soup,title_info,outf):
    uncrawl = False
    text = soup.find_all('div',{'class':'main'})
    text = text[0].get_text(strip=True)
    score = re.findall('最低录取分(.*?)分|最低分(.*?)分|录取最低分(.*?)分',text)
    print(score)
    if len(score):
        tmp = copy.deepcopy(title_info)
        tmp['科类'] = None
        tmp['最低分'] = is_num_by_except(score[0])
        outf.write(json.dumps(tmp)+'\n')
    else:
        tmp1 = copy.deepcopy(title_info)
        tmp2 = copy.deepcopy(title_info)
        tmp1['科类'] = '理工'
        tmp2['科类'] = '文史'
        s1 =  re.findall('理工最低(.*?)分|理工类最低分(.*?)。',text)
        s2 = re.findall('文史最低(.*?)分|文史类最低分(.*?)，',text)
        print(s1,s2)
        tmp1['最低分'] = s1[0]
        tmp2['最低分'] = s2[0]
        outf.write(json.dumps(tmp1)+'\n')
        outf.write(json.dumps(tmp2)+'\n')
    return uncrawl     


def _sichuandaxue(soup,title_info,outf):
    uncrawl = False
    table_content = soup.find_all('table')
    if len(table_content):
        table_content = table_content[0]
        rows = table_content.findAll(lambda tag: tag.name=='tr')
        ks = [td.get_text(strip=True) for td in rows[0].find_all('td')]
        ks = ks[1:]
        ds = [td.get_text(strip=True) for td in rows[2].find_all('td')]
        if len(ks) == 1:
            tmp = copy.deepcopy(title_info)
            tmp['专业方向'] = None
            tmp['科类'] = '理工'

            tmp['最低分'] = is_num_by_except(ds[2])
            outf.write(json.dumps(tmp)+'\n')
        elif len(ks) == 2:
            print(ds)
            if len(ds) == 5:
                tmp = copy.deepcopy(title_info)
                tmp['科类'] = '理工'
                tmp['最低分'] = is_num_by_except(ds[2])
                outf.write(json.dumps(tmp)+'\n')  
                tmp = copy.deepcopy(title_info)
                tmp['科类'] = '文史'
                tmp['最低分'] = is_num_by_except(ds[4])
                outf.write(json.dumps(tmp)+'\n')
            elif len(ds) == 3:
                tmp = copy.deepcopy(title_info)
                tmp['科类'] = '理工'
                tmp['最低分'] = is_num_by_except(ds[1])
                outf.write(json.dumps(tmp)+'\n')  
                tmp = copy.deepcopy(title_info)
                tmp['科类'] = '文史'
                tmp['最低分'] = is_num_by_except(ds[2])
                outf.write(json.dumps(tmp)+'\n')
            else:
                uncrawl = True
        else:
            uncrawl = True
    else:
        uncrawl = True
    return uncrawl   


def _chongqinggongchengxueyuan(soup,title_info,outf):
    uncrawl = False
    table_content = soup.find_all('table')
    if len(table_content):
        table_content = table_content[0]
        rows = table_content.findAll(lambda tag: tag.name=='tr')
        if len(rows) == 4:
            ds = [td.get_text(strip=True) for td in rows[2].find_all('td')]
            tmp = copy.deepcopy(title_info)
            tmp['批次'] = ds[1]
            tmp_score = ds[4]
            tmp['最低分'] = float(tmp_score.split('分')[0])
            outf.write(json.dumps(tmp)+'\n')       
        else:
            if title_info['科类'] == '艺术':
                ds = [td.get_text(strip=True) for td in rows[3].find_all('td')]
                tmp = copy.deepcopy(title_info)
                tmp['批次'] = ds[1]
                tmp['最低分'] = float(ds[4])
                outf.write(json.dumps(tmp)+'\n')
            else:
                ds_art = [td.get_text(strip=True) for td in rows[3].find_all('td')]
                ds_science = [td.get_text(strip=True) for td in rows[4].find_all('td')]
                tmp1 = copy.deepcopy(title_info)
                tmp2 = copy.deepcopy(title_info)
                tmp1['批次'] = ds_art[0]
                tmp2['批次'] = ds_art[0]
                tmp1['科类'] = '文史'
                tmp2['科类'] = '理工'
                tmp1['最低分'] = float(ds_art[3])
                tmp2['最低分'] = float(ds_science[2])
                outf.write(json.dumps(tmp1)+'\n')
                outf.write(json.dumps(tmp2)+'\n')
    else:
        uncrawl = False
    return uncrawl


def _hubeidaxue(soup,title_info,outf):
    uncrawl = False
    table_content = soup.find_all('table')
    if len(table_content): 
        table_content = table_content[0]
        rows = table_content.findAll(lambda tag: tag.name=='tr')
        if title_info['科类'] == '体育' or title_info['科类'] == '艺术':
            for i in range(3,len(rows)):
                ds = [td.get_text(strip=True) for td in rows[i].find_all('td')]
                tmp = copy.deepcopy(title_info)
                tmp['批次'] = ds[2]
                tmp['专业'] = ds[3]
                tmp['最高分'] = float(ds[4])
                tmp['最低分'] = float(ds[5])
                outf.write(json.dumps(tmp)+'\n')
        elif title_info['科类'] == '理工' or title_info['科类'] == '文史' or title_info['科类'] == '综合':
                row1 = [td.get_text(strip=True) for td in rows[0].find_all('td')]
                row3 = [td.get_text(strip=True) for td in rows[2].find_all('td')] 
                tmp = copy.deepcopy(title_info)       
                tmp['科类'] = row1[-1]
                tmp['最高分'] = float(row3[2])
                tmp['最低分'] = float(row3[3])    
                outf.write(json.dumps(tmp)+'\n')
        else:
            uncrawl = True
    else:
        uncrawl = True
    return uncrawl    


def _shandongzhengzhiqingnianxueyuan(soup,title_info,outf):
    uncrawl = False
    table_content = soup.find_all('table')
    if len(table_content): 
        table_content = table_content[0]
        rows = table_content.findAll(lambda tag: tag.name=='tr')
        for i in range(2,len(rows)):
            ds = [td.get_text(strip=True) for td in rows[i].find_all('td')]
            for sub,index in zip(['文史','理工'],[[3,4,5],[6,7,8]]):
                tmp = copy.deepcopy(title_info) 
                tmp['专业'] = sub
                tmp['最高分'] = is_num_by_except(ds[index[0]])
                tmp['最低分'] = is_num_by_except(ds[index[1]])
                tmp['平均分'] = is_num_by_except(ds[index[2]])
                outf.write(json.dumps(tmp)+'\n')
    else:
        uncrawl = True
    return uncrawl        
    
#%%

with open(r"""C:\Myfile\File\学业资料\测评产品/scoreline_title_url.json""",'r') as f:
             title_url = json.load(f)    

school_name = '山东青年政治学院'

res_title = np.load(r'C:\Myfile\File\学业资料\测评产品\Data\crawl_log/third_crawl_residue.npy')
res_num = []
for r in res_title:
    if school_name in r:
        res_num.append(r)
        
the_school = []
for t in title_url.keys():
    if school_name in t:
        the_school.append(t)
if len(the_school) == len(res_num):
    print('All url have not been crawled.')
else:
    print('The part of url have been crawled.')

print(title_url[res_num[0]])
#%%
uncrawl_list = []
for title in the_school:
    url = title_url[title]
    uncrawl = get_admission_info(title, url,_shandongzhengzhiqingnianxueyuan)
    uncrawl_list.append(uncrawl)

#%%
vali = []
with open(r'C:\Myfile\File\学业资料\测评产品\Data\raw\湖北大学/raw_admission_info@湖北大学2019年云南普通本科（文史类）录取分数线.json','r') as f:
    for line in f.readlines():
        dic = json.loads(line)
        vali.append(dic)
print(vali)