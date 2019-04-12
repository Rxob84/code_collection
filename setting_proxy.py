"""

@koharite

https://qiita.com/koharite/items/731fcf5146c7b0c4e800

"""
from bs4 import BeautifulSoup
import requests

# 社内プロキシ設定
proxy = {"http": "http://proxy.mei.co.jp:8080", "https": "http://proxy.mei.co.jp:8080"}  # http,httpsの両方ないとだめだった。

r = requests.get('https://github.com/timeline.json', proxies=proxy)
print(r.text)


def get_bs(url):
    html = requests.get(url, proxies=proxy)
    bs_obj = BeautifulSoup(html.content, "html.parser")
    return bs_obj


htmlSource = get_bs("https://en.wikipedia.org/wiki/Kevin_Bacon")

# ページ内のリンクを表示する
for link in htmlSource.findAll("a"):  # "a"がhtmlでのリンクを示すタグ？
    if "href" in link.attrs:          # →ではなく"href"っぽい。
        print(link.attrs["href"])
