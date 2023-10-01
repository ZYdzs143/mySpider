import chapter
from cartoon import*


def main():
    # 拿到所有话访问地址
    ch = chapter.get_chapter()
    # 倒序是因为网站目录是倒序的，方便命名，倒序一下
    for n, c in enumerate(ch[-1::-1]):
        #  获得某一话的cid和key
        cid, key = get_cid_key(c)
        #  获得所有图片下载链接
        ul = get_url(cid, key, c)
        #  下载图片
        get_img(ul, n, c)


# 按装订区域中的绿色按钮以运行脚本。
if __name__ == '__main__':
    main()

# 访问 https://www.jetbrains.com/help/pycharm/ 获取 PyCharm 帮助
