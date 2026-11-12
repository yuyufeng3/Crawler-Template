# 爬虫模板 (Crawler Template)

先抓导航栏分类信息，分类链接里抓取商品详情信息。

## 🚀 如何使用

1. 克隆代码到本地：
   `git clone https://github.com/yuyufeng3/Crawler-Template.git`

2. 创建并激活虚拟环境：
   `python -m venv venv`
   `venv\Scripts\activate` (Windows)

3. 安装依赖库：
   `pip install -r requirements.txt`

4. 安装 Playwright 浏览器内核：
   `playwright install chromium`

5. 修改 `A_抓取模板` 里的 `self.url` 后，运行代码即可。
