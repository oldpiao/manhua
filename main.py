import os
import json
import threading

from manhua_download import search, get_manhua_use_url


OLD_RENWU = 'old_renwu.json'


def save_renwu(data):
    with open(OLD_RENWU, 'w') as f:
        f.write(json.dumps(data))


def read_renwu():
    with open(OLD_RENWU, 'r') as f:
        data = json.loads(f.read())
    return data


def search_and_download():
    try:
        old_download = read_renwu()
        for i in old_download:
            print(i)
        if old_download !=[] and input('发现历史任务,是否开启历史任务(Y/N): ').lower() == 'y':
            all_download = old_download
        else:
            all_download = []
    except:
        all_download = []
    while True:
        key_word = input('搜索漫画(空字符退出): ')
        if key_word == '':
            break
        datas = search(key_word=key_word)
        bianhaos = []
        while True:
            print('编号: %d) %s' % (0, '选好开下'))
            for i in range(len(datas)):
                if i in bianhaos:
                    continue
                kong = 20 - len(datas[i]['title'])
                kong = kong if kong > 1 else 1
                print('编号: %d) %s %s 最新章节: %s' % (i + 1, datas[i]['title'], '  ' * kong, datas[i]['new_title']))
            try:
                j = int(input('根据编号选择要下载的漫画: '))
                os.system("cls")
                if j == 0:
                    break
                elif j - 1 in bianhaos:
                    print('该漫画已在待下载队列，请选择其他漫画。')
                elif j - 1 < 0 or j - 1 >= len(datas):
                    print('警告: 请输入正确的编号。')
                else:
                    bianhaos.append(j - 1)
            except:
                print('警告: 请输入正确的编号。')
        all_download.append([datas, bianhaos])
    save_renwu(all_download)
    ts = []
    for i in all_download:
        datas = i[0]
        bianhaos = i[1]
        for j in bianhaos:
            path_name = (datas[j]['url'], datas[j]['title'])
            print(path_name)
            t = threading.Thread(target=get_manhua_use_url, args=path_name)
            t.start()
            ts.append(t)
    for i in ts:
        i.join()
    save_renwu([])


if __name__ == '__main__':
    search_and_download()