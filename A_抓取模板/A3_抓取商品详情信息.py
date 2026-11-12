import time
from urllib import response

from curl_cffi import requests
from lxml import etree
from print_color import print
import json,random
from urllib.parse import urljoin
import os
import pandas as pd

# 提取一份data/2/products.json数据  名字+链接列表
with open('data/2/products.json', 'r', encoding='utf-8') as f:
    tree = json.load(f)


class Stars():
    def __init__(self):
        # 填入官网网址，做后续url拼接
        self.url = ''
        self.headers = {}  # self.session = requests.Session(impersonate="chrome120")  self.html = self.session.get(self.url,headers = self.headers).text


    def get_main_name(self,html):
        main_name = ''
        return main_name

    def get_main_price(self,html):
        main_price = ''
        return main_price

    def get_main_sku(self,html):
        main_sku = ''
        return main_sku

    def get_main_desc(self,html):
        main_desc = ''
        return main_desc

    def get_main_image(self,html):
        main_image = []
        return main_image

    def get_main_zdy_zd(self,html):
        main_zdy_zd = {}
        return main_zdy_zd


    def check_variant(self, html):
        """判断是否存在变体商品：有 variations_form 即视为有变体"""
        try:
            return bool(html.xpath('//form[contains(@class,"variations_form")]'))
        except Exception as e:
            print(f'检测变体失败:{e}')
            return False

    def get_variants_list(self, html):
        variants_list = []


        return variants_list

        """抓取所有变体：数据全在 variations_form 的 data-product_variations JSON 里"""

    def run(self):

        for Categories, urls in tree.items():
            for category_url,product_urls in urls.items():
                for product_url in product_urls:
                    response = requests.get(product_url, headers=self.headers,impersonate='chrome120',timeout=3)
                    time.sleep(random.uniform(0.1,0.35))

                    if response.status_code == 200:
                        all_product_info = []

                        html = etree.HTML(response.text)
                        # 没有变体的情况
                        if not self.check_variant(html):
                            print(f'{product_url}没有变体',color='purple')
                            product_info = {
                                'Tpye': 'simple',
                                '分类来源': Categories,
                                '商品名称': self.get_main_name(html) if self.get_main_name(html) else None,
                                '价格': self.get_main_price(html) if self.get_main_price(html) else None,
                                'SKU': self.get_main_sku(html) if self.get_main_sku(html) else None,
                                'body_描述': self.get_main_desc(html) if self.get_main_desc(html) else None,
                                '主图链接': ', '.join(self.get_main_image(html)) if self.get_main_image(html) else None,  # 列表转字符串，用逗号拼起来
                                '自定义字段': str(self.get_main_zdy_zd(html))if self.get_main_zdy_zd(html) else None,  # 字典转字符串（或者提取需要的键）

                            }

                            all_product_info.append(product_info)

                        else: # 有变体的情况
                            print(f'{product_url}有变体', color='blue')
                            variants_list = self.get_variants_list(html)
                            for variant in variants_list:

                                vari_price = ''
                                variant_sku = ''
                                variant_images = []
                                variant_parent = ''
                                # 变体属性:指的是颜色，尺寸等等，所以可能有多个
                                variant_attribute_name1 = ''
                                variant_attribute_value1 = ''
                                variant_attribute_name2 = ''
                                variant_attribute_value2 = ''

                                product_info = {
                                    'Tpye': 'variation',
                                    '分类来源': Categories,
                                    'parent' : variant_parent,
                                    '价格': vari_price if vari_price else None,
                                    'SKU': variant_sku if variant_sku else None,
                                    '主图链接': ', '.join(variant_images) if variant_images else None,  # 列表转字符串，用逗号拼起来
                                    '变体属性名1': variant_attribute_name1 if variant_attribute_name1 else None,
                                    '变体属性值1': variant_attribute_value1 if variant_attribute_value1 else None,
                                    '变体属性名2': variant_attribute_name2 if variant_attribute_name2 else None,
                                    '变体属性值2': variant_attribute_value2 if variant_attribute_value2 else None,

                                    '商品名称': self.get_main_name(html) if self.get_main_name(html) else None,
                                    'body_描述': self.get_main_desc(html) if self.get_main_desc(html) else None,
                                    '自定义字段': str(self.get_main_zdy_zd(html)) if self.get_main_zdy_zd(html) else None,  # 字典转字符串（或者提取需要的键）

                                }

                                all_product_info.append(product_info)




                        df = pd.DataFrame(all_product_info)
                        df.to_csv('all_products.csv', index=False, encoding='utf-8-sig')
                    else:
                        print(f'{self.url}的响应状态码是{response.status_code},注意查看cookie是否过期',color='yellow')



if __name__ == '__main  __':
