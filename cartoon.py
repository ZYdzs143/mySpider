import js2py
import requests
from lxml.etree import HTML
import re
import datetime
from urllib.parse import quote
import time
import random


#  获取某一话的cid和key, 用于获得下载链接的js代码
def get_cid_key(url):
    """
    :param url: 某一话的地址，例如:第三话'http://www.gmanhua.com/ch3-1556147/'
    :return: cid和key用于获得该话所有图片下载链接
    """
    headers = {
        'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.43',
        'Referer': url
    }
    # 获取网页源码
    response = requests.post(url=url, headers=headers)
    tree = HTML(response.text)
    # 拿到cid的值
    cid = tree.xpath('//script[8]/text()')[0].strip(' ;').split(';')[-7][-7:]
    # 拿到初始的js代码
    js = tree.xpath('/html/body/script/text()')[0].strip(' ').replace('eval', 'var zx=')
    # 执行初始的js代码，拿到解密后的js代码，现在结果仍然是一个js代码，但实际上数据已经很严然的出现了，不需要再执行了，直接正则表达式提取
    key = "".join(re.compile(r'\'(\w)').findall(js2py.eval_js(js)))
    return cid, key


# 获取第1页和后续的下载链接，因为第一页和后续所用key不同
def get_url(cid, key, base_url):
    """
    :param cid: cid
    :param key: key
    :param base_url: 某一话的地址，例如：第三话'http://www.gmanhua.com/ch3-1556147/'
    :return: 某一话所有图片的下载链接
    """
    #  标准时间
    data = {
        'd': quote(datetime.datetime.now().strftime('%a %b %d %Y %H:%M:%S GMT 0800 (中国标准时间)'))
    }
    params = {
        'cid': cid,
        'page': '1',
        'key': key,
        'showcount': '20'  # 一页20张图片，可选5，10，20
    }
    url_list = []
    # 执行两次，第一次拿到第一页图片的下载链接，第二次拿到其他页图片的下载链接
    for i in range(2):
        if i == 0:
            #  拼接成一个地址，该地址用于获得js代码
            url = base_url + 'chapterimagefun.ashx?'
            # url = 'http://www.gmanhua.com/ch2-1555475/chapterimagefun.ashx?'
            headers = {
                'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.43',
                'Referer': base_url  # Referer参数很重要，不加的话下载下来的图片是错的
            }
            response = requests.post(url=url, headers=headers, data=data, params=params)
            #  拿到js代码后执行，获得第一页的下载链接，
            url_list += list(js2py.eval_js(response.text))[0:20]
        else:
            url = base_url.strip('/') + '-p2/chapterimagefun.ashx?'
            # url = 'http://www.gmanhua.com/ch2-1555475-p2/chapterimagefun.ashx?'
            headers = {
                'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.43',
                'Referer': base_url.strip('/') + '-p2/'
            }
            params['page'] = '21'
            response = requests.post(url=url, headers=headers, data=data, params=params)
            #  拿到js代码后执行，获得第n(n>1)页的下载链接，
            url_list += list(js2py.eval_js(response.text))
    return url_list


def get_img(url_list, n, base_ref):
    """

    :param url_list: 某一话所有图片的下载链接
    :param n: 第n话，主要是为了给下载下来的图片命名防止混淆
    :param base_ref: 某一话的地址，例如：第三话'http://www.gmanhua.com/ch3-1556147/'
    :return:
    """
    for num, url in enumerate(url_list):
        # base_ref = 'http://www.gmanhua.com/ch3-1556147/'
        time.sleep(random.choice([2, 3, 4]))
        # 一页20张图片，Referer参数随页数变化改变，第一页.../ch3-1556147/...,第二页.../ch3-1556147-p2/...,类推
        if num // 20 < 1:
            ref = base_ref
        else:
            ref = base_ref.strip('/') + '-p' + str(num // 20 + 1) + '/'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
            'Referer': ref,
        }
        response = requests.get(url=url, headers=headers)
        #  将图片保存到文件夹中
        with open(f'D:/python_all/temp/img1/img/{n}_{num + 1}.jpg', 'wb') as fp:
            fp.write(response.content)


if __name__ == '__main__':
    a, b = get_cid_key('https://www.gmanhua.com/ch4-1556805/')
    cc = get_url(a, b, 'https://www.gmanhua.com/ch4-1556805/')
    get_img(cc, 4, 'https://www.gmanhua.com/ch4-1556805/')

