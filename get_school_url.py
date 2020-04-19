# -*- coding: utf-8 -*-
"""
Created on Sat Apr  4 23:18:10 2020

@author: qyk
"""
import os
import requests
import datetime
import json
import re

from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36",
}


def get_schools_score_url():
    link = []
    title = []
    for page in range(1,101):
        if page == 1:
            target_url = 'http://www.gaokao.com/baokao/lqfsx/dxfsx/index.shtml'
        else:
            base_url = 'http://www.gaokao.com/baokao/lqfsx/dxfsx/index_{}.shtml'
            target_url = base_url.format(page)
        
        # request and get html
        resp = requests.request('Get',url=target_url,headers=headers)
        if resp.status_code == 200:
            resp.encoding = 'gb2312'
            html_content =  resp.text
        else:
            print('404 not found')
        
        if isinstance(html_content, str):
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # get score link and title
            targ = soup.find_all('a',{'target':'_blank',
                                     'title':re.compile('^(?!.*公布)')},
                                text=re.compile('.*录取分数线'),)
            temp_link = [t['href'] for t in targ]
            temp_title = [t['title'] for t in targ]
            
        else:
            print('---------------')
            print('data mismatch')
            print(page)
        link.extend(temp_link)
        title.extend(temp_title)
    school_scoreline_url = dict(zip(title,link))
    return school_scoreline_url

scr = get_schools_score_url()
today = datetime.datetime.today().strftime('%Y%m%d')
output_file = os.path.join('C:\Myfile\File\学业资料\测评产品','raw_scoreline_url_data@%s.json'%(today))
outf = open(output_file, 'w')
outf.write(json.dumps(scr))
outf.close()


#%%
# get school name
# load json file to dict
import json
import pandas as pd
with open('C:\\Myfile\\File\\学业资料\\测评产品\\raw_scoreline_url_data@20200405.json','r') as load_f:
    load_dict = json.load(load_f)

school = list(load_dict.keys())
school = [s.split('2019')[0] for s in school]  # 提取出每个title 属于的学校或者学院字符串
school  = list(set(school))
school = pd.Series(school,name='学校')
school.to_csv('C:\Myfile\File\学业资料\测评产品/school_name.csv',encoding="utf_8_sig")
