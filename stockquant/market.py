import json
import requests
import tushare as ts
from stockquant.config import config
from stockquant.utils.tools import get_date, datetime_str_to_ts
import pandas as pd


class Market:

    @staticmethod
    def tick(symbol):
        return Tick.get_realtime_data(symbol)

    @staticmethod
    def kline(symbol, timeframe, adj=None, start_date=None, end_date=None):
        """
        获取历史k线数据
        :param symbol:例如："sh601003"，或者"sz002307"，前者是沪市，后者是深市
        :param timeframe:k线周期，只能小写，支持："5m", "15m", "30m", "1h", "1d"，分别为5、15、30分钟、1小时、1天
        :param adj:复权类型(只针对股票)：None未复权 qfq前复权 hfq后复权 , 默认None未复权
        :param start_date:开始日期 (格式：YYYYMMDD)
        :param end_date:结束日期 (格式：YYYYMMDD)
        :return:返回一个列表,其中每一条k线数据包含在一个列表中，包含时间戳、开、高、低、收、成交量6个数据，日k线数据时间戳为20201106.0这种格式（浮点数），其他周期为秒时间戳
        """
        adj = adj or None
        if "m" in timeframe or "h" in timeframe:
            if timeframe == "5m" or timeframe == "15m" or timeframe == "30m":
                timeframe = int(timeframe.split("m")[0])
            elif timeframe == "1h":
                timeframe = 60
            url = "http://money.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_MarketData.getKLineData?symbol=%s&scale=%d" % (
                symbol, timeframe)
            response = requests.get(url).json()
            kline = []
            for i in response:
                kline.append(
                    [
                        datetime_str_to_ts(i["day"]),
                        float(i["open"]),
                        float(i["high"]),
                        float(i["low"]),
                        float(i["close"]),
                        float(i["volume"])
                    ]
                )
            return kline
        elif "d" in timeframe:
            if symbol.startswith("sh"):
                symbol = symbol.split("sh")[1] + "." + "SH"
            elif symbol.startswith("sz"):
                symbol = symbol.split("sz")[1] + "." + "SZ"
            ts.set_token(config.tushare_api)
            response = ts.pro_bar(ts_code=symbol, adj=adj, start_date=start_date, end_date=end_date)
            response = response.drop(['ts_code'], axis=1)
            response = response.drop(['pre_close'], axis=1)
            response = response.drop(['change'], axis=1)
            response = response.drop(['pct_chg'], axis=1)
            response = response.drop(['amount'], axis=1)
            timestamp = response['trade_date'].astype(int)
            df = pd.DataFrame(
                {
                    "timestamp": timestamp,
                    "open": response["open"],
                    "high": response["high"],
                    "low": response["low"],
                    "close": response["close"],
                    "volume": response["vol"]
                }
            )
            kline = df.values.tolist()
            kline.reverse()
            return kline

    @staticmethod
    def shenzhen_component_index():
        """
        获取深圳成指
        :return:返回一个字典
        """
        response = requests.get("http://hq.sinajs.cn/list=s_sz399001").text
        data = response.split(",")
        result = {
            "指数名称": data[0].replace('"', "").split("=")[1],
            "当前点数": float(data[1]),
            "涨跌点数": float(data[2]),
            "涨跌率": float(data[3]),
            "成交数量": float(data[4]),
            "成交金额": float(data[5].split('";')[0])
        }
        return result

    @staticmethod
    def shanghai_component_index():
        """
        获取上证综指
        :return:
        """
        response = requests.get("http://hq.sinajs.cn/list=s_sh000001").text
        data = response.split(",")
        result = {
            "指数名称": data[0].replace('"', "").split("=")[1],
            "当前点数": float(data[1]),
            "涨跌点数": float(data[2]),
            "涨跌率": float(data[3]),
            "成交数量": float(data[4]),
            "成交金额": float(data[5].split('";')[0])
        }
        return result

    @staticmethod
    def stocks_list():
        """股票列表,获取基础信息数据，包括股票代码、名称、上市日期、退市日期等"""
        pro = ts.pro_api(config.tushare_api)
        response = pro.query('stock_basic', exchange='', list_status='L',
                             fields='ts_code,symbol,name,area,industry,list_date')
        return response

    @staticmethod
    def today_is_open():
        """查询今日沪深股市是否开盘，如果开盘返回True,反之False"""
        pro = ts.pro_api(config.tushare_api)
        response = pro.query('trade_cal', start_date=get_date(), end_date=get_date())
        list = response.values.tolist()
        if list[0][2] == 0:
            return False
        else:
            return True

    @staticmethod
    def new_stock():
        """获取新股上市列表数据"""
        pro = ts.pro_api(config.tushare_api)
        response = pro.new_share()
        return response


class Tick:
    """ 实时行情数据
    """

    def __init__(
            self, symbol=None, open=None, yesterday_close=None, last=None, high=None, low=None, bid_price=None, ask_price=None,
            transactions=None, turnover=None, bid1_quantity=None, bid1_price=None, bid2_quantity=None, bid2_price=None,
            bid3_quantity=None, bid3_price=None, bid4_quantity=None, bid4_price=None, bid5_quantity=None, bid5_price=None,
            ask1_quantity=None, ask1_price=None, ask2_quantity=None, ask2_price=None, ask3_quantity=None, ask3_price=None,
            ask4_quantity=None, ask4_price=None, ask5_quantity=None, ask5_price=None, timestamp=None
    ):
        self.symbol = symbol                        # 股票名称
        self.open = open                            # 今日开盘价
        self.yesterday_close = yesterday_close      # 昨日收盘价
        self.last = last                            # 当前价格
        self.high = high                            # 今日最高价
        self.low = low                              # 今日最低价
        self.bid_price = bid_price                  # 竞买价
        self.ask_price = ask_price                  # 竞卖价
        self.transactions = transactions            # 成交数量
        self.turnover = turnover                    # 成交金额
        self.bid1_quantity = bid1_quantity          # 买一数量
        self.bid1_price = bid1_price                # 买一报价
        self.bid2_quantity = bid2_quantity          # 买二数量
        self.bid2_price = bid2_price                # 买二报价
        self.bid3_quantity = bid3_quantity          # 买三数量
        self.bid3_price = bid3_price                # 买三报价
        self.bid4_quantity = bid4_quantity          # 买四数量
        self.bid4_price = bid4_price                # 买四报价
        self.bid5_quantity = bid5_quantity          # 买五数量
        self.bid5_price = bid5_price                # 买五报价
        self.ask1_quantity = ask1_quantity          # 卖一数量
        self.ask1_price = ask1_price                # 卖一报价
        self.ask2_quantity = ask2_quantity          # 卖二数量
        self.ask2_price = ask2_price                # 卖二报价
        self.ask3_quantity = ask3_quantity          # 卖三数量
        self.ask3_price = ask3_price                # 卖三报价
        self.ask4_quantity = ask4_quantity          # 卖四数量
        self.ask4_price = ask4_price                # 卖四报价
        self.ask5_quantity = ask5_quantity          # 卖五数量
        self.ask5_price = ask5_price                # 卖五报价
        self.timestamp = timestamp                  # 时间戳

    @property
    def data(self):
        d = {
            "symbol": self.symbol,
            "open": self.open,
            "yesterday_close": self.yesterday_close,
            "last": self.last,
            "high": self.high,
            "low": self.low,
            "bid_price": self.bid_price,
            "ask_price": self.ask_price,
            "transactions": self.transactions,
            "turnover": self.turnover,
            "bid1_quantity": self.bid1_quantity,
            "bid1_price": self.bid1_price,
            "bid2_quantity": self.bid2_quantity,
            "bid2_price": self.bid2_price,
            "bid3_quantity": self.bid3_quantity,
            "bid3_price": self.bid3_price,
            "bid4_quantity": self.bid4_quantity,
            "bid4_price": self.bid4_price,
            "bid5_quantity": self.bid5_quantity,
            "bid5_price": self.bid5_price,
            "ask1_quantity": self.ask1_quantity,
            "ask1_price": self.ask1_price,
            "ask2_quantity": self.ask2_quantity,
            "ask2_price": self.ask2_price,
            "ask3_quantity": self.ask3_quantity,
            "ask3_price": self.ask3_price,
            "ask4_quantity": self.ask4_quantity,
            "ask4_price": self.ask4_price,
            "ask5_quantity": self.ask5_quantity,
            "ask5_price": self.ask5_price,
            "timestamp": self.timestamp
        }
        return d

    @staticmethod
    def get_realtime_data(symbol):
        """
        获取指定股票的实时数据
        :param symbol: 例如："sh601003"，或者"sz002307"，前者是沪市，后者是深市
        :return:返回一个字典
        """
        tick = Tick(symbol)
        response = requests.get("http://hq.sinajs.cn/list=%s" % symbol).text
        data = response.split(",")
        tick.timestamp = data[-4] + " " + data[-3]
        tick.symbol = data[0].replace('"', "").split("=")[1]
        tick.open = float(data[1])
        tick.yesterday_close = float(data[2])
        tick.last = float(data[3])
        tick.high = float(data[4])
        tick.low = float(data[5])
        tick.bid_price = float(data[6])
        tick.ask_price = float(data[7])
        tick.transactions = round(float(data[8]))
        tick.turnover = round(float(data[9]))
        tick.bid1_quantity = round(float(data[10]))
        tick.bid1_price = float(data[11])
        tick.bid2_quantity = round(float(data[12]))
        tick.bid2_price = float(data[13])
        tick.bid3_quantity = round(float(data[14]))
        tick.bid3_price = float(data[15])
        tick.bid4_quantity = round(float(data[16]))
        tick.bid4_price = float(data[17])
        tick.bid5_quantity = round(float(data[18]))
        tick.bid5_price = float(data[19])
        tick.ask1_quantity = round(float(data[20]))
        tick.ask1_price = float(data[21])
        tick.ask2_quantity = round(float(data[22]))
        tick.ask2_price = float(data[23])
        tick.ask3_quantity = round(float(data[24]))
        tick.ask3_price = float(data[25])
        tick.ask4_quantity = round(float(data[26]))
        tick.ask4_price = float(data[27])
        tick.ask5_quantity = round(float(data[28]))
        tick.ask5_price = float(data[29])
        return tick

    def __str__(self):
        info = json.dumps(self.data)
        return info

    def __repr__(self):
        return str(self)