from flask import Flask
import requests
from lxml import etree  # pip install lxml

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/pe_ttm/<code>')
def show_pe(code):
    ms = MyStock()
    return str(ms.catch_pe(code))


@app.route('/indexid/<id>')
def get_index_stock(id):
    session = requests.session()
    r = session.get(
        f'http://vip.stock.finance.sina.com.cn/corp/go.php/vII_NewestComponent/indexid/{id}.phtml')# 解析HTML
    print(r.text)
    html = etree.HTML(r.content)
    stock_code = html.xpath("//table[@id='NewStockTable']//tr/td[1]/div/text()")
    stock_url = html.xpath("//table[@id='NewStockTable']//tr//a/@href")
    stock_name = html.xpath("//table[@id='NewStockTable']//tr//a/text()")
    print(stock_url)
    rr = dict(zip(stock_name, stock_url))
    return rr


class MyStock:
    def __init__(self):
        self.session = requests.session()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"}
        self.session.get("https://www.xueqiu.com", headers=self.headers, verify=False)

    # 获取pe_ttm
    def catch_pe(self, code):
        url = f'https://stock.xueqiu.com/v5/stock/quote.json?symbol={code}&extend=detail'
        print(url)
        r = self.session.get(url, headers=self.headers, verify=False)
        rj = r.json()
        print(rj)
        return rj['data']['quote']['pe_ttm']


if __name__ == '__main__':
    # SSL忽略告警
    requests.packages.urllib3.disable_warnings()

    # 启动
    app.run(debug=True)
