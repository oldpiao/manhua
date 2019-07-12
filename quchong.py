import re
import json


class Chapter2Heavy(object):

    def __init__(self):
        self.chapter = []
        self.re_chapter = []
        self.nums = []
        self.re_chapter_nums = []

    def add(self, chapter, num, spetial_re=None, child_re=None):
        if spetial_re is not None:
            spetial = re.search(spetial_re, chapter['name'])
            if spetial is not None:
                for i in spetial.groups():
                    if i is not None:
                        num = i + '_' + num
                        chapter['spetial'] = i
        if child_re is not None:
            child = re.search(child_re, chapter['name'])
            if child is not None:
                # print(child.groups())
                for i in child.groups():
                    if i is not None:
                        num = num + '_' + i
                        chapter['child'] = i
        # print(chapter)
        if num in self.nums:
            self.re_chapter.append(chapter)
            self.re_chapter_nums.append(num)
        else:
            self.chapter.append(chapter)
            self.nums.append(num)


def calculate2(num):
    num_dict = {'零': '0', '一': '1', '二': '2', '三': '3', '四': '4',
                '五': '5', '六': '6', '七': '7', '八': '8', '九': '9',}
    new_num = ''
    for i in num:
        new_num += num_dict[i]
    return int(new_num)


def calculate(num):
    num_dict = {
        '一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9,
        '零': 0,
        '十': lambda x: x*10,
        '百': lambda x: x*100,
        '千': lambda x: x*1000,
        '万': lambda x: x*10000,
        '兆': lambda x: x*1000000,  # 百万
        '亿': lambda x: x*100000000,
    }
    new_num, wei = 0, None
    for i in num:
        if i == '零':
            pass
        elif isinstance(num_dict[i], int):
            if wei is not None:
                new_num += wei
            wei = num_dict[i]
        else:
            if wei is None:
                wei = 1
            wei = num_dict[i](wei)
    new_num += wei
    return new_num


def chapter_to_heavy(names, urls, spetial_re=r'(特别篇)|(番外)|(漫漫长夜)',
                child_re=r'([上中下])|'
                         r'\d+[^0-9]+(\d+)|'
                         r'\d+.*?([一二三四五六七八九零十百千万亿兆]+)|'
                         r'[一二三四五六七八九零十百千万亿兆]+.*?(\d+)|'
                         r'[一二三四五六七八九零十百千万亿兆]+[^一二三四五六七八九零十百千万亿兆]+([一二三四五六七八九零十百千万亿兆]+)'
                ):
    '''
    1: 特别篇之作者解说        # 没有章节号
    2: 第84话                  # 数字章节号
    3: 特别篇九                # 汉字数字
    4: 第九十四话              # 汉字数字带十百千万
    5: 第十八话二              # 子话
    6: 第86话2                 # 子话
    7: 第55话（2）             # 子话
    8: 第02话 下               # 子话
    9: 特别篇12                # 非主章节
    10: 番外1                   # 非主章节
    '''
    c2h = Chapter2Heavy()
    for name, url in zip(names, urls):
        chapter = {'name': name, 'url': url}
        num = re.search(r'\d+\.\d+', name)
        if num is not None:
            c2h.add(chapter, num.group(), spetial_re, child_re)
            continue
        num = re.search(r'\d+', name)
        if num is not None:
            c2h.add(chapter, str(int(num.group())), spetial_re, child_re)
            continue
        num = re.search(r'[一二三四五六七八九零十百千万亿兆]+', name)
        if num is None:
            c2h.add(chapter, chapter['name'], spetial_re, child_re)
            continue
        elif re.search(r'[十百千万亿兆]', num.group()) is None:
            c2h.add(chapter, str(calculate2(num.group())), spetial_re, child_re)
            continue
        else:
            c2h.add(chapter, str(calculate(num.group())), spetial_re, child_re)
    return c2h


def t_calculate():
    nums = [
        '零一',
        '十', '十一', '二十一',
        '百', '一百', '一百一十', '一百零一', '一百一十一',
        '千', '万', '十万', '兆', '一百万', '一千万零四百零四', '亿', '一千万亿'
    ]
    for i in nums:
        print(calculate(i))


if __name__ == '__main__':
    # child_re = r'([上中下])|\d+[^0-9]+(\d+)|\d+.*?([一二三四五六七八九零十百千万亿兆]+)|[一二三四五六七八九零十百千万亿兆]+.*?(\d+)|[一二三四五六七八九零十百千万亿兆]+[^一二三四五六七八九零十百千万亿兆]+([一二三四五六七八九零十百千万亿兆]+)'
    # print(re.search(child_re, '第01话 上').groups())
    # exit()
    with open('../download/镖人/镖人.json', 'r') as f:
        data = json.loads(f.read())
    names, urls = [], []
    for i in data:
        names.append(i['name'])
        urls.append(i['url'])
    c2h = chapter_to_heavy(names, urls)
    for i in c2h.chapter:
        print(i)
    for i in c2h.re_chapter:
        print(i)
    for i in c2h.chapter:
        print(i['name'], end=' ')
    print()
    for i in c2h.re_chapter:
        print(i['name'], end=' ')
    print()
    for i in c2h.nums:
        print(i, end=' ')
    print()
    for i in c2h.re_chapter_nums:
        print(i, end=' ')

