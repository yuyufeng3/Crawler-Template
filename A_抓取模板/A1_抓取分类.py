from curl_cffi import requests
from lxml import etree
from print_color import print
import json
from urllib.parse import urljoin
import os

# 保底方法 启用浏览器
from playwright.sync_api import sync_playwright


class Sun():
    def __init__(self):

        self.url = ''

        self.headers = {}

        # self.session = requests.Session(impersonate="chrome120")  self.html = self.session.get(self.url,headers = self.headers).text


    # f1 返回 {title:{url:str,child:{title:{title:str,child:{}}}}}
    def f1(self, html, dic):
        ml1 = html.xpath('//nav[@class="header__inline-menu"]/ul/li')
        for node in ml1:

            _name = node.xpath('./summary/span/text()')
            if _name:
                _name = ''.join(_name).strip()
            else:
                _name = ''

            _url = node.xpath('./a/@href')
            if _url:
                if _url[0] != '#':
                    _url = urljoin(self.url, _url[0])
                else:
                    _url = ''
            else:
                _url = ''

            print('这是一级元素名字和链接', _name, _url,color='green')

            dic[_name] = {'url': _url, 'child': {}}
            son_dict = dic[_name]['child']

            if isinstance(son_dict, dict):
                child = node.xpath('./div/ul/li')

                self.f2(son_dict, child)

        # 1. 抓首页 collections 链接：同时取 href 和链接文字（名字）
        pairs = []
        for a in html.xpath('//a[contains(@href, "/collections/")]'):
            href = a.get('href') or ''
            name = ' '.join(a.xpath('.//text()')).strip()  # ← 名字从 a 的文字取
            if href and name:
                pairs.append((urljoin(self.url, href), name))

        # 2. 按 url 去重（同一条 url 只留一个名字，不能 set 掉名字）
        seen_url = {}
        for url, name in pairs:
            if url not in seen_url:
                seen_url[url] = name

        # 3. 收集分类树里已存在的 url（一级/二级/三级）
        existing = set()
        for a in dic:
            existing.add(dic[a]['url'])
            for b in dic[a]['child']:
                existing.add(dic[a]['child'][b]['url'])
                for c in dic[a]['child'][b]['child']:
                    existing.add(dic[a]['child'][b]['child'][c]['url'])

        # 4. 不在 existing 里的，用【名字】当键归到 others
        others = {}
        for url, name in seen_url.items():
            if url not in existing:
                others[name] = {'url': url, 'child': {}}  # ← 键是 name，不是 url
        if others:
            dic['others'] = {'url': '', 'child': others}



    def f2(self, dic: dict, child_ls: list):
        for node in child_ls:

            _name = node.xpath('./summary/span/text()')
            if _name:
                _name = ''.join(_name).strip()
                # _name = ' '.join(''.join(_name).split()).strip()
            else:
                _name = ''

            _url = node.xpath('./a/@href')
            if _url:
                if _url[0] != '#':
                    _url = urljoin(self.url, _url[0])
                else:
                    _url = ''
            else:
                _url = ''
            print('这是二级元素名字和链接', _name, _url,color='purple')
            dic[_name] = {'url': _url, 'child': {}}
            son_dict = dic[_name]['child']

            if isinstance(son_dict, dict):
                child = node.xpath('./ul/li')
                self.f3(son_dict, child)

        return dic

    def f3(self, dic: dict, child_ls: list):
        for node in child_ls:
            _name = node.xpath('./a//text()')
            if _name:
                _name = ''.join(_name).strip()
            else:
                _name = ''

            _url = node.xpath('./a/@href')
            if _url:
                if _url[0] != '#':
                    _url = urljoin(self.url, _url[0])
                else:
                    _url = ''
            else:
                _url = ''

            if '/pages/' in _url:
                continue
            elif '/blogs/' in _url:
                continue
            print('这是三级元素名字和链接', _name, _url,color='blue')

            dic[_name] = {'url': _url, 'child': {}}


   # 功能:将最终字典扁平化处理
    def flatten(self, tree):
        result = {}
           #  内部递归函数
        def walk(node, ancestors):
            for name, info in node.items():
                path = ancestors + [name]


                parts = [' '.join(path[:i + 1]) for i in range(len(path))]  #range(5)  →  0, 1, 2, 3, 4
                key = ','.join(parts)
                if info['url']:  #url为空不存入字典
                    result[key] = info['url']

                child = info.get('child', {})
                if child:
                    walk(child, path)

        # 扁平化处理从这开始
        walk(tree, [])
        return result


    # def get_html(self):
    #     try:
    #         resp = requests.get(self.url, headers=self.headers, impersonate="chrome120", timeout=15)
    #         if resp.status_code != 200:
    #             print(f'状态码 {resp.status_code}: {url}', color='red')
    #             return ''
    #         return resp.text
    #     except Exception as e:
    #         print(f'curl 失败，切浏览器: {e}', color='yellow')
    #         return self.get_html_by_browser(self.url)
    #
    # def get_html_by_browser(self, url):
    #
    #     print(f'启动浏览器抓取: {url}', color='cyan')
    #     with sync_playwright() as p:
    #         browser = p.chromium.launch(headless=True)  # headless=True 不弹窗
    #         page = browser.new_page(
    #             user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    #         )
    #         try:
    #             page.goto(url, timeout=30000, wait_until='networkidle')
    #             html = page.content()  # 拿渲染后的 HTML
    #             return html
    #         except Exception as e:
    #             print(f'浏览器也失败了: {e}', color='red')
    #             return ''
    #         finally:
    #             browser.close()


    def run(self):

        """
        # 浏览器自动化方案
        response_text = self.get_html(self.url)
        if not response_text:
            return

        """
        response = requests.get(self.url, headers=self.headers, impersonate="chrome120")
        if response.status_code != 200:
            print('状态码不是200🐱',color='red')
            raise Exception(f"HTTP 请求失败，状态码: {response.status_code}")
        response_text = response.text

        html = etree.HTML(response_text)
        local_html_path = "Home.html"
        with open(local_html_path, 'w', encoding='utf-8') as f:
            f.write(response.text)

        tree = {}
        self.f1(html, tree)

        os.makedirs('data/1', exist_ok=True)

        # flatten函数作用 将字典扁平化 {"第一级名字,第一级名字 第二级名字,第一级名字 第二级名字 第三级名字":链接}
        flat = self.flatten(tree)
        # 输出扁平化字典
        print(json.dumps(flat, ensure_ascii=False, indent=2))
        with open('data/1/tree.json', 'w', encoding='utf-8') as f:
            json.dump(flat, f, ensure_ascii=False, indent=2)
if __name__ == '__main__':
    r = Sun()
    r.run()