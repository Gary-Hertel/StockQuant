"""
Author: Gary-Hertel
Email:  garyhertel@foxmail.com
Date:   2022-01-23
"""

import json

import requests

from stockquant.tick import Tick


class MoneyData:

    @staticmethod
    def get_realtime_data(symbol: str):
        """
        获取指定股票的实时数据
        :param symbol: 例如："sh601003"，或者"sz002307"，前者是沪市，后者是深市
        :return:返回一个字典
        """
        code = f"0{symbol.lstrip('sh')}" if symbol.startswith("sh") else f"1{symbol.lstrip('sz')}"
        tick = Tick()
        response = requests.get(f"http://api.money.126.net/data/feed/{code},money.api").text
        response = response.lstrip("_ntes_quote_callback(")
        response = response.rstrip(");")
        data = json.loads(response)
        data = data[code]
        tick.timestamp = data["time"]
        tick.symbol = symbol
        tick.name = data["name"]
        tick.percent = data["percent"]
        tick.updown = data["updown"]
        tick.open = data["open"]
        tick.yesterday_close = data["yestclose"]
        tick.last = data["price"]
        tick.high = data["high"]
        tick.low = data["low"]
        tick.bid_price = data["bid1"]
        tick.ask_price = data["ask1"]
        tick.transactions = data["volume"]
        tick.turnover = data["turnover"]
        tick.bid1_quantity = data["bidvol1"]
        tick.bid1_price = data["bid1"]
        tick.bid2_quantity = data["bidvol2"]
        tick.bid2_price = data["bid2"]
        tick.bid3_quantity = data["bidvol3"]
        tick.bid3_price = data["bid3"]
        tick.bid4_quantity = data["bidvol4"]
        tick.bid4_price = data["bid4"]
        tick.bid5_quantity = data["bidvol5"]
        tick.bid5_price = data["bid5"]
        tick.ask1_quantity = data["askvol1"]
        tick.ask1_price = data["ask1"]
        tick.ask2_quantity = data["askvol2"]
        tick.ask2_price = data["ask2"]
        tick.ask3_quantity = data["askvol3"]
        tick.ask3_price = data["ask3"]
        tick.ask4_quantity = data["askvol4"]
        tick.ask4_price = data["ask4"]
        tick.ask5_quantity = data["askvol5"]
        tick.ask5_price = data["ask5"]
        return tick

    @staticmethod
    def shenzhen_component_index():
        """
        获取深圳成指
        :return:返回一个字典
        """
        response = requests.get("http://api.money.126.net/data/feed/1399001,money.api").text
        response = response.lstrip("_ntes_quote_callback(")
        response = response.rstrip(");")
        data = json.loads(response)
        data = data["1399001"]
        result = {
            "指数名称": data["name"],
            "当前点数": data["price"],
            "涨跌点数": data["price"] - data["yestclose"],
            "涨跌率": data["percent"],
            "成交数量": data["volume"],
            "成交金额": data["turnover"]
        }
        return result

    @staticmethod
    def shanghai_component_index():
        """
        获取上证综指
        :return:
        """
        response = requests.get("http://api.money.126.net/data/feed/0000001,money.api").text
        response = response.lstrip("_ntes_quote_callback(")
        response = response.rstrip(");")
        data = json.loads(response)
        data = data["0000001"]
        result = {
            "指数名称": data["name"],
            "当前点数": data["price"],
            "涨跌点数": data["price"] - data["yestclose"],
            "涨跌率": data["percent"],
            "成交数量": data["volume"],
            "成交金额": data["turnover"]
        }
        return result


if __name__ == '__main__':
    
    tick = MoneyData.get_realtime_data(symbol="sh603176")
    print(tick)
    
    sh = MoneyData.shanghai_component_index()
    print(sh)
    
    sz = MoneyData.shenzhen_component_index()
    print(sz)