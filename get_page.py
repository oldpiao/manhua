import json
import os

import requests
from bs4 import BeautifulSoup
from bs4 import BeautifulStoneSoup


def get_page(url, zhang_dir, page=1):
    url_page = url[:-5]+'-'+str(page)+'.html'
    html = requests.get(url_page)
    soup = BeautifulSoup(html.content, 'lxml')
    try:
        img_url = soup.find_all('div', class_='chapter-content')[0].img['src']
    except:
        return
    img = requests.get(img_url).content
    img_file = os.path.join(zhang_dir, str(page)+'.jpg')
    print(img_file)
    with open(img_file, 'wb') as f:
        f.write(img)
    get_page(url, zhang_dir, page+1)


def run(file_dir, data):
    begin = False
    for i in data:
        if i['name'] == '第六十三话 任务追踪':
            begin = True
        if not begin:
            continue
        zhang_dir = os.path.join(file_dir, i['name'])
        if not os.path.isdir(zhang_dir):
            os.makedirs(zhang_dir)
        get_page(i['url'], zhang_dir)


if __name__ == '__main__':
    file_dir = '../download/狼烟吹雪'
    with open('狼烟吹雪.json', 'r') as f:
        data = json.loads(f.read())
    run(file_dir, data)
    # url = 'https://m.gufengmh8.com/manhua/kuibazhilangyanchuixue/170973.html'
    # get_page(url, file_dir+'/test')
