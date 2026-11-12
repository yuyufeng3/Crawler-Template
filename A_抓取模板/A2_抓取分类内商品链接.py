from curl_cffi import requests
from lxml import etree
from print_color import print
import json
from urllib.parse import urljoin
import os,time,random

# 提取一份data/1/tree.json数据
with open('data/1/tree.json', 'r', encoding='utf-8') as f:
    tree = json.load(f)                       # 读成 dict



class Light():
    def __init__(self):
        # 填入官网网址，做后续url拼接
        self.url = ''
        self.headers = {}

        # self.session = requests.Session(impersonate="chrome120")  self.html = self.session.get(self.url,headers = self.headers).text

    def fun(self, dic):
        # 遍历 tree中的分类名与链接
        for name, url in tree.items():
            current_url = url
            if name in dic:

                if dic[name][f'分类页链接 {url}'] == []:
                    print()
                    print(f'发现{name}缓存内容为空:进行重新抓取', color='yellow')
                else:
                    print('命中缓存:', name, color='green')

                    continue
            products_urls = []
            while current_url:
                # 🐱 给个随机延时防封
                time.sleep(random.uniform(1.5, 3.5))  # 👈 加上这句，给个随机延时防封

                response = requests.get(current_url, headers=self.headers, impersonate="chrome120",timeout=30)
                if response.status_code == 200:
                    print('当前response.status_code为:', response.status_code, color='green')
                    html = response.text
                    if len(html) < 1000: print(' 内容太短，很可能是拦截 / 空壳页 ',color='yellow')

                    xml = etree.HTML(html)
                    # 先找所有产品，再在每个产品中找链接
                    products = xml.xpath('//div[contains(@class,"grid-item product-item")]')
                    for product in products:
                        href = product.xpath('.//h2[@class="c-product-tile__name"]/a/@href')
                        if href:
                            href = href[0]
                            href = urljoin(self.url, href)
                            if href not in products_urls:
                                products_urls.append(href)
                    if len(products_urls) == 0:  # 为空的分类页要不要跳过呢，还是留下方便检查是否真为空
                        print(f'在{name},\n{current_url}抓取到 {len(products_urls)} 条链接，已存入',color='yellow')

                    else:
                        print(f'在{name},\n{current_url}抓取到 {len(products_urls)} 条链接，已存入',color='purple')
                    print('')




                    # 找下一页(找准翻页逻辑)
                    next_link = xml.xpath('//link[@rel="next"]/@href')
                    # 防止下一页链接是本页，导致陷入死循环
                    if next_link and next_link[0] and urljoin(self.url, next_link[0]) != current_url:
                        current_url = urljoin(self.url, next_link[0])
                    else:
                        current_url = None

                # # 响应状态码不为 2**
                else:
                    print(f'在{name},\n{current_url}的当前response.status_code为:', response.status_code, color='red')
                    current_url = None


            dic[name] = {f'分类页链接 {url}':products_urls}



            with open('data/2/products.json', 'w', encoding='utf-8') as f:
                json.dump(dic, f, ensure_ascii=False, indent=2)





    def run(self):
        os.makedirs('data/2', exist_ok=True)
        finish_path = 'data/2/products.json'
        if os.path.exists(finish_path):
            with open(finish_path, 'r', encoding='utf-8') as f:
                dic = json.load(f)
            print(f'已有 {len(dic)} 个分类的进度，接着跑', color='yellow')
        else:
            dic = {}

        self.fun(dic)


if __name__ == '__main__':
    l = Light()
    l.run()