# cookie 测试
# 作者: David
# Github: https://github.com/HEUDavid/WeiboSpider

import json
import time

import requests


class CookieTest:

    def __init__(self, cookie_path):
        self.cookie_path = cookie_path
        self.Session = requests.Session()
        self.Session.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'}
        self.Session.cookies.update(self.load_cookie())

    def load_cookie(self):
        try:
            with open(self.cookie_path, 'r') as f:
                data = json.load(f)
            return data
        except BaseException:
            print(self.cookie_path, '未找到')
            return None

    def get_page(self, url='https://s.weibo.com/'):

        for i in range(5):
            try:
                html = self.Session.get(url, timeout=(5, 25))  # 连接超时 读取超时
            except ConnectionResetError:
                # ConnectionResetError: [Errno 104] Connection reset by peer
                time.sleep(5)
            except Exception as e:
                print('\n' * 2)
                print(e)
                print('\n' * 2)
                time.sleep(5)
            else:
                break
        else:
            print(url)
            print('重试解决不了问题')
            return None

        return html.text.replace('\u200b', '')

    def is_OK(self, html):
        # PC 版
        if "CONFIG['islogin'] = '1'" in html:
            return True
        # 触屏版
        elif 'login: [1][0]' in html:
            return True
        # 旧版
        elif '详细资料' in html:
            return True
        else:
            return False


def main():
    cookie_path = './cookies/' + 'cookie_965019007@qq.com.json'
    test = CookieTest(cookie_path)

    url1 = 'https://m.weibo.cn/'  # 触屏版
    url2 = 'https://weibo.cn/'  # 旧版 还有问题
    url3 = 'https://weibo.com/'  # PC 版
    url4 = 'https://s.weibo.com/'  # PC 版 高级搜索

    html = test.get_page(url4)
    # print(html)
    print(test.is_OK(html))


# main()
