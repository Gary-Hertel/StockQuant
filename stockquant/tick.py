import json


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

    def __str__(self):
        info = json.dumps(self.data)
        return info

    def __repr__(self):
        return str(self)