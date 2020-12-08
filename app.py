from flask import Flask
import requests
from lxml import etree  # pip install lxml
import json

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


# 获取股票的TTM市盈率
@app.route('/pe_ttm/<code>')
def show_pe(code):
    ms = MyStock()
    return str(ms.catch_pe(code))


# 获取指数的成分股
@app.route('/indexid/<id>')
def get_index_stock(id):
    res = ''
    session = requests.session()
    for i in range(1):
        url = f'http://vip.stock.finance.sina.com.cn/corp/view/vII_NewestComponent.php?page=9&indexid={id}'
        # url = f'http://vip.stock.finance.sina.com.cn/corp/go.php/vII_NewestComponent/indexid/{id}.phtml'
        r = session.get(url)
        # print(r.text)
        html = etree.HTML(r.content)
        # stock_code = html.xpath("//table[@id='NewStockTable']//tr/td[1]/div/text()")
        stock_url = html.xpath("//table[@id='NewStockTable']//tr//a/@href")
        stock_name = html.xpath("//table[@id='NewStockTable']//tr//a/text()")
        # print(stock_url)
        stock_code = []
        for s in stock_url:
            stock_code.append(s.split('/')[5])
        dict_stock = dict(zip(stock_code, stock_name))
        ms = MyStock()
        for sc in dict_stock:
            res += sc.upper() + ':' + dict_stock[sc] + ':' + str(ms.catch_pe(sc)) + '<br>'
    return res


# 获取指数的成分股
@app.route('/indexid300')
def get_index_stock_300():
    res = ''
    session = requests.session()
    url = f'http://60.push2.eastmoney.com/api/qt/clist/get?cb=jQuery112405739809083964376_1607432107466&pn=1&pz=500&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=b:BK0500+f:!50&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152,f45&_=1607432107486'
    r = session.get(url)
    # rj = r.json()
    # print(rj)
    rt = r.text
    dict_stock = json.loads(rt[42:-2])
    # print(dict_stock)
    ms = MyStock()
    for sc in dict_stock['data']['diff']:
        # print(sc)
        code = str(sc['f12'])
        if sc['f13'] == 0:
            code = 'SZ' + code
        elif sc['f13'] == 1:
            code = 'SH' + code
        res += code + ':' + sc['f14'] + ':' + str(ms.catch_pe(code)) + '<br>'
    return res


class MyStock:
    def __init__(self):
        self.session = requests.session()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"}
        self.session.get("https://www.xueqiu.com", headers=self.headers, verify=False)

    # 获取pe_ttm
    def catch_pe(self, code):
        url = f'https://stock.xueqiu.com/v5/stock/quote.json?symbol={code.upper()}&extend=detail'
        # print(url)
        r = self.session.get(url, headers=self.headers, verify=False)
        rj = r.json()
        # print(rj)
        return rj['data']['quote']['pe_ttm']


if __name__ == '__main__':
    # SSL忽略告警
    requests.packages.urllib3.disable_warnings()

    # 启动
    app.run(debug=True)
