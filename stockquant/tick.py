from dataclasses import dataclass


@dataclass(init=False)
class Tick:
    """ 实时行情数据"""
    symbol: str                             # 股票代码
    name: str                               # 股票名称
    percent: float                          # 涨跌幅度
    updown: float                           # 涨跌点数
    open: float                             # 今日开盘价
    yesterday_close: float                  # 昨日收盘价
    last: float                             # 当前价格
    high: float                             # 今日最高价
    low: float                              # 今日最低价
    bid_price: float                        # 竞买价
    ask_price: float                        # 竞卖价
    transactions: int                       # 成交数量
    turnover: float                         # 成交金额
    bid1_quantity: int                      # 买一数量
    bid1_price: float                       # 买一报价
    bid2_quantity: int                      # 买二数量
    bid2_price: float                       # 买二报价
    bid3_quantity: int                      # 买三数量
    bid3_price: float                       # 买三报价
    bid4_quantity: int                      # 买四数量
    bid4_price: float                       # 买四报价
    bid5_quantity: int                      # 买五数量
    bid5_price: float                       # 买五报价
    ask1_quantity: int                      # 卖一数量
    ask1_price: float                       # 卖一报价
    ask2_quantity: int                      # 卖二数量
    ask2_price: float                       # 卖二报价
    ask3_quantity: int                      # 卖三数量
    ask3_price: float                       # 卖三报价
    ask4_quantity: int                      # 卖四数量
    ask4_price: float                       # 卖四报价
    ask5_quantity: int                      # 卖五数量
    ask5_price: float                       # 卖五报价
    timestamp: str                          # 时间戳