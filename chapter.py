import requests
from lxml.etree import HTML


def get_chapter():
    # 漫画目录页地址
    url = 'https://www.gmanhua.com/manhua593390/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
    }
    response = requests.get(url=url, headers=headers)
    tree = HTML(response.text)
    # 拿到所有的章节标号并拼接成地址，为了方便将贺图什么的去掉了
    # 实际调用时需要根据实际情况修改一下
    chapter = tree.xpath("//ul[@class='nr6 lan2']//li/a/@href")
    chapter_url = ['https://www.gmanhua.com'+c for c in chapter if c.startswith("/ch", 0, 3)]
    # 减一是因为网站bug多了一个第七话
    return chapter_url[0:len(chapter_url)-1]


if __name__ == '__main__':
    a = get_chapter()
    print(a)

