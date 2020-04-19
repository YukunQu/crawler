# -*- coding: utf-8 -*-
"""
Created on Mon Apr  6 12:35:52 2020

@author: qyk
"""
import requests
import json

from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36",
}

# get score line from school url

def _get_html_content(url):
    resp = requests.request('Get',url,headers=headers)
    if resp.status_code == 200:
        resp.encoding = 'gb2312'
        return  resp.text
    else:
        print('404 not found')   
        return None

def zhongguominhangUniversity(url):
    html_content = _get_html_content(url)
    soup = BeautifulSoup(html_content,'html.parser')
    
    