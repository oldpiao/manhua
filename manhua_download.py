import json
import os
import time
import re

import requests
from bs4 import BeautifulSoup
import threading

from quchong import chapter_to_heavy

DOWNLOAD_DIR = '../download'


def get_pages(url, zhang_dir, page=1, retry=1):
    if page == 1:
        url_page = url
    else:
        url_page = url[:-5]+'-'+str(page)+'.html'
    html = requests.get(url_page)
    soup = BeautifulSoup(html.content, 'lxml')
    try:
        img_url = soup.find_all('div', class_='chapter-content')[0].img['src']
    except:
        return
    try:
        img = requests.get(img_url).content
    except:
        if retry <= 3:
            time.sleep(10)
            get_pages(url, zhang_dir, page, retry+1)
        return
    img_file = os.path.join(zhang_dir, str(page)+'.jpg')
    print("正在下载: ", img_file)
    with open(img_file, 'wb') as f:
        f.write(img)
    get_pages(url, zhang_dir, page+1)


def get_manhua(file_dir, zhangs, begin=None, is_re=False):
    my_re, to_re = r'[\/:*?"<>|]', '_'
    n = 0
    if is_re:
        print('即将开始下载重复章节,共%d章' % len(zhangs))
        name_prefix = '重复_'
    else:
        print('即将开始下载正常章节,共%d章' % len(zhangs))
        name_prefix = ''
    for zhang in zhangs:
        n += 1
        str_n = '0'*(3-len(str(n)))+str(n)
        zhang['name'] = re.sub(my_re, to_re, zhang['name'])
        zhang['name'] = name_prefix+str_n+'_'+zhang['name']
        print('正在下载章节: %s url: %s' % (zhang['name'], zhang['url']))
        if begin is not None:
            begin = re.sub(my_re, to_re, begin)
            if zhang['name'] != begin:
                continue
            else:
                begin = None
        zhang_dir = os.path.join(file_dir, zhang['name'])
        if os.path.isdir(zhang_dir):
            try:
                page = max([int(img[:-4]) for img in os.listdir(zhang_dir)])
            except:
                get_pages(zhang['url'], zhang_dir)
            else:
                get_pages(zhang['url'], zhang_dir, page=page+1)
        else:
            os.makedirs(zhang_dir)
            get_pages(zhang['url'], zhang_dir)


def get_manhua_use_url(url, relpath=None, begin=None, root_dir=None, distinct=False):
    host = 'https://m.gufengmh8.com/'
    if root_dir is None:
        root_dir = DOWNLOAD_DIR or '.'
    if relpath is None:
        paths = url.split('/')
        for i in paths[::-1]:
            if i != '':
                relpath = i
                break
    file_path = os.path.join(root_dir, relpath)
    if not os.path.isdir(file_path):
        os.makedirs(file_path)
    json_name = os.path.basename(file_path)
    if json_name == '':
        json_name = os.path.basename(os.path.dirname(file_path))
    json_file = os.path.join(file_path, json_name+'.json')
    json_file_duplicated_data = os.path.join(file_path, json_name + '_duplicated_data.json')
    if os.path.isfile(json_file):
        with open(json_file, 'r') as f:
            chapter = json.loads(f.read())
    else:
        html = requests.get(url)
        soup = BeautifulSoup(html.content, 'lxml')
        names, urls = [], []
        for each_zhang in soup.find_all('ul', class_='Drama autoHeight')[0].find_all('li'):
            names.append(each_zhang.span.get_text())
            urls.append(host + each_zhang.a['href'])
        result = chapter_to_heavy(names, urls)
        chapter = result.chapter
        re_chapter = result.re_chapter
        print("章节信息存储在: %s" % json_file)
        with open(json_file, 'w') as f:
            f.write(json.dumps(chapter))
        print("重复章节信息存储在: %s" % json_file_duplicated_data)
        with open(json_file_duplicated_data, 'w') as f:
            f.write(json.dumps(re_chapter))
    get_manhua(file_path, chapter, begin=begin, is_re=False)
    if not distinct:
        try:
            with open(json_file_duplicated_data, 'r') as f:
                re_chapter = json.loads(f.read())
            get_manhua(file_path, re_chapter, begin=begin, is_re=True)
        except:
            print('没有重复章节')


def search(key_word='斗罗大陆'):
    search_url = 'https://m.gufengmh8.com/search/?keywords=%s' % key_word
    html = requests.get(search_url)
    soup = BeautifulSoup(html.content, 'lxml')
    datas = []
    for each_one in soup.find_all('div', class_='itemBox'):
        data = {
            'img': each_one.find('mip-img')['src'],
            'title': each_one.find('a', attrs={'class': 'title'}).get_text(),
            'url': each_one.find('a', attrs={'class': 'title'})['href'],
            'type': each_one.find('span', attrs={'class': 'pd'}).get_text(),
            'time': each_one.find('span', attrs={'class': 'date'}).get_text(),
            'new_title': each_one.find('a', attrs={'class': 'coll'}).get_text(),
            'new_url': each_one.find('a', attrs={'class': 'coll'})['href'],
        }
        datas.append(data)
        # print(data)
        # print(each_one)
    return datas


if __name__ == '__main__':
    search()

# if __name__ == '__main__':
    # https://m.gufengmh8.com/
    # path = 'https://m.gufengmh8.com/manhua/kuibazhilangyanchuixue/'  # 狼烟吹雪
    # path = 'https://m.gufengmh8.com/manhua/kuibazhiyoulongqishi/'  # 幽龙骑士
    path_names = [
        # ('https://m.gufengmh8.com/manhua/touxingjiuyuetianyishijie/', '偷星九月天_异世界'),
        # ('https://m.gufengmh8.com/manhua/touxingjiuyuetianqianzhuanheiyuetieqi/', '偷星九月天前传黑月铁骑'),
        # ('https://m.gufengmh8.com/manhua/touxingjiuyuetian2/', '偷星九月天2'),
        # ('https://m.gufengmh8.com/manhua/yirenzhixia/', '一人之下'),
        # ('https://m.gufengmh8.com/manhua/jinjidejuren/', '进击的巨人'),
        # ('https://m.gufengmh8.com/manhua/jinjidejurenyuanhuaji/', '进击的巨人原话集'),
        # ('https://m.gufengmh8.com/manhua/jinjidejurenLOSTGIRLS/', '进击的巨人LOST GIRLS'),
        # ('https://m.gufengmh8.com/manhua/jinjidejurenBeforethefall/', '进击的巨人Before_the_fall'),
        # ('https://m.gufengmh8.com/manhua/yiquanchaoren/', '一拳超人')
        ('https://m.gufengmh8.com/manhua/biaoren/', '镖人')

    ]
    # for path_name in path_names:
    #     get_manhua_use_url(*path_name)
    t_pool = []
    for path_name in path_names:
        print(path_name)
        t = threading.Thread(target=get_manhua_use_url, args=path_name)
        t_pool.append(t)
    for i in t_pool:
        i.start()
    #
