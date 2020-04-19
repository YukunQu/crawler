# -*- coding: utf-8 -*-
"""
Created on Sat Apr 10 09:16:01 2020

@author: qyk
"""
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
    grade_list = ['本科','本科普通批','一本','本科一批','一批本科','二本',
                  '本科二批','二批本科','国家专项','提前批','高校专项','预科']
    for grade in grade_list:
        if grade in title[1]:
            if grade in ['一本','本科一批','一批本科']:
                title_info['批次'] = '本科一批'
            elif grade in ['二本','本科二批','二批本科']:
                title_info['批次'] = '本科二批'
            else:
                title_info['批次'] = grade
    return title_info


def get_admission_info(title,url,ks_tag='th'):
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
        table_content = soup.find_all('table')
        if len(table_content):
            table_content = table_content[0]
            rows = table_content.findAll(lambda tag: tag.name=='tr')
            
            ks = [td.get_text(strip=True) for td in rows[0].find_all('{}'.format(ks_tag))]
    
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
    else:
        uncrawl = True
    outf.close()
    if uncrawl:
        print('The data did not be crawled.')
    else:
        print('The data was crawled')
    return uncrawl


#%%first crawl

with open(r"""C:\Myfile\File\学业资料\测评产品/scoreline_title_url.json""",'r') as f:
             title_url = json.load(f)

first_uncrawl = []
for title,url in title_url.items():
    first_uncrawl.append(get_admission_info(title,url,'th'))

np.save(r'C:\Myfile\File\学业资料\测评产品\Data\crawl_log/first_uncrawl.npy',first_uncrawl)

title_all = list(title_url.keys())
crawl_residue = []
for fu,title in zip(first_uncrawl,title_all):
    if fu:
        crawl_residue.append(title)
np.save(r'C:\Myfile\File\学业资料\测评产品\Data\crawl_log/first_crawl_residue.npy',crawl_residue)


#%% second crawl
first_crawl_residue = crawl_residue
second_crawl_residue = []
for tit in first_crawl_residue:
    scr = get_admission_info(tit, title_url[tit],'td')
    if scr:
        second_crawl_residue.append(tit)
np.save(r'C:\Myfile\File\学业资料\测评产品\Data\crawl_log/second_crawl_residue',second_crawl_residue)


#%%
# third crawl to crawl image

def get_admission_img(title,url):
    uncrawl = False
    # get school information from title
    title_info = _get_title_info(title)
    
    # create dir and open file
    prepath = 'C:\Myfile\File\学业资料\测评产品\Data/raw'
    dire = os.path.join(prepath,title_info['学校'])
    if not os.path.exists(dire):
        os.mkdir(dire)
    file_name = 'raw_admission_info@{}.png'.format(title)
    output_file = os.path.join(dire,file_name) 
    
    # get score information from html image
    resp = requests.request('Get',url,headers=headers)
    if resp.status_code == 200:
        resp.encoding = 'gb2312'
        html_content = resp.text
    else:
        print('{} 404 not found',format(title))
        
    if isinstance(html_content, str):
        soup = BeautifulSoup(html_content,features='html.parser') 
        
        # Download image
        main_content = soup.find_all('div',{'class':'main'}) 
        if len(main_content):
            main_content = main_content[0]
            img = main_content.find_all('img')
            if len(img) > 1:
                img_url = [i['src'] for i in img[:-1]]
                for i in img_url:
                    img_content = requests.get(i).content
                    with open(output_file,'wb')as f : # 循环写入图片
                        f.write(img_content)
            else:
                uncrawl = True
        else:
            uncrawl = True
    else:
        uncrawl = True
    if uncrawl:
        print('The data {} did not crawled.'.format(title))
    else:
        print('The data {} crawled'.format(title))
    return uncrawl    


with open(r"""C:\Myfile\File\学业资料\测评产品/scoreline_title_url.json""",'r') as f:
             title_url = json.load(f)
second_crawl_residue = np.load(r'C:\Myfile\File\学业资料\测评产品\Data\crawl_log/second_crawl_residue.npy')
third_crawl_resiude = []
for tl in second_crawl_residue:
    tr = get_admission_img(tl,title_url[tl])
    if tr:
        third_crawl_resiude.append(tl)

