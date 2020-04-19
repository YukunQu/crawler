# vi: set ft=python sts=4 ts=4 sw=4 et:

import json
import time
import datetime
import requests

from bs4 import BeautifulSoup

# simulate a user
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36",
}

#-- sina
def _search_spec_score_request(local_name, page):
    local_dict = {
        "北京": 1,
        "天津": 2,
        "上海": 3,
        "重庆": 4,
        "河北": 5,
        "河南": 6,
        "山东": 7,
        "山西": 8,
        "安徽": 9,
        "江西": 10,
        "江苏": 11,
        "浙江": 12,
        "湖北": 13,
        "湖南": 14,
        "广东": 15,
        "广西": 16,
        "云南": 17,
        "贵州": 18,
        "四川": 19,
        "陕西": 20,
        "青海": 21,
        "宁夏": 22,
        "黑龙江": 23,
        "吉林": 24,
        "辽宁": 25,
        "西藏": 26,
        "新疆": 27,
        "内蒙古": 28,
        "海南": 29,
        "福建": 30,
        "甘肃": 31,
        "港澳台": 32,
    }
    
    assert local_name in local_dict
    assert isinstance(page, int)

    base_url = 'http://kaoshi.edu.sina.com.cn/college/scorelist?'
    params = {
        "tab": "major",
        "wl": "",
        "local": local_dict[local_name],
        "provid": "",
        "batch": "",
        "syear": "",
        "page": page,
    }

    resp = requests.request("GET", base_url, headers=headers, params=params)
    if resp.status_code==200:
        resp.encoding = 'utf-8'
        return resp.text
    else:
        return None

def get_spec_score_from_sina(local_name):
    today = datetime.datetime.today().strftime('%Y%m%d')
    output_file = 'raw_sina_data@%s_%s.json'%(local_name, today)
    outf = open(output_file, 'w')
 
    # first query
    page = 1
    total_page_num = 0
    html_content = _search_spec_score_request(local_name, page)
    if isinstance(html_content, str):
        soup = BeautifulSoup(html_content, 'html.parser')
        # get total page number
        pg_content = soup.find_all('div', {'class': 'pageNumWrap'})
        if len(pg_content):
            pg_content = pg_content[0]
        else:
            print('No page info found!')
            return
        total_item_num = int(pg_content['totalnum'])
        total_page_num = int(pg_content['totalpage'])
        print('Find %s items @ %s - %s pages'%(total_item_num, local_name,
                                               total_page_num))

        # get score table
        table_content = soup.find_all('table', {'class': 'tbL2'})
        if len(table_content):
            table_content = table_content[0]
        else:
            print('No table found!')
            return
        rows = table_content.findAll(lambda tag: tag.name=='tr')
        ks = [td.get_text(strip=True) for td in rows[0].find_all('td')]
        for i in range(1, len(rows)):
            ds = [td.get_text(strip=True) for td in rows[i].find_all('td')]
            if len(ks)==len(ds):
                # save data
                tmp = dict(zip(ks, ds))
                outf.write(json.dumps(tmp)+'\n')
            else:
                print('---------------')
                print('data mismatch')
                print(rows[i])

    # continue query
    while page < total_page_num:
        time.sleep(1)
        page += 1
        print('Crawl page %s'%(page))
        html_content = _search_spec_score_request(local_name, page)
        if isinstance(html_content, str):
            soup = BeautifulSoup(html_content, 'html.parser')

            # get score table
            table_content = soup.find_all('table', {'class': 'tbL2'})
            if len(table_content):
                table_content = table_content[0]
            else:
                print('No table found!')
                return
            rows = table_content.findAll(lambda tag: tag.name=='tr')
            ks = [td.get_text(strip=True) for td in rows[0].find_all('td')]
            for i in range(1, len(rows)):
                ds = [td.get_text(strip=True) for td in rows[i].find_all('td')]
                if len(ks)==len(ds):
                    # save data
                    tmp = dict(zip(ks, ds))
                    outf.write(json.dumps(tmp)+'\n')
                else:
                    print('---------------')
                    print('data mismatch')
                    print(rows[i])
    
    outf.close()



#-- crawl data from sina
get_spec_score_from_sina('新疆')

