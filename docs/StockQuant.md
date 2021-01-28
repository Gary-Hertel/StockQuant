# StockQuant

`Gary-Hertel`

------



# 行情

## Tick行情

### Tick数据

```python
from stockquant.quant import *

config.loads('config.json')
tick = Market.tick("sh601003")
```

### Tick对象数据结构

|        调用方式        | 数据类型 |  字段说明  |
| :--------------------: | :------: | :--------: |
|     `tick.symbol`      | `string` |  股票名称  |
|      `tick.last`       | `float`  |  当前价格  |
|      `tick.open`       | `float`  | 今日开盘价 |
|      `tick.high`       | `float`  | 今日最高价 |
|       `tick.low`       | `float`  | 今日最低价 |
| `tick.yesterday_close` | `float`  | 昨日收盘价 |
|    `tick.bid_price`    | `float`  |   竞买价   |
|    `tick.ask_price`    | `float`  |   竞卖价   |
|  `tick.transactions`   | `float`  |  成交数量  |
|    `tick.turnover`     | `float`  |  成交金额  |
|  `tick.bid1_quantity`  | `float`  |  买一数量  |
|   `tick.bid1_price`    | `float`  |  买一报价  |
|  `tick.bid2_quantity`  | `float`  |  买二数量  |
|   `tick.bid2_price`    | `float`  |  买二报价  |
|  `tick.bid3_quantity`  | `float`  |  买三数量  |
|   `tick.bid3_price`    | `float`  |  买三报价  |
|  `tick.bid4_quantity`  | `float`  |  买四数量  |
|   `tick.bid4_price`    | `float`  |  买四报价  |
|  `tick.bid5_quantity`  | `float`  |  买五数量  |
|   `tick.bid5_price`    | `float`  |  买五报价  |
|  `tick.ask1_quantity`  | `float`  |  卖一数量  |
|   `tick.ask1_price`    | `float`  |  卖一报价  |
|  `tick.ask2_quantity`  | `float`  |  卖二数量  |
|   `tick.ask2_price`    | `float`  |  卖二报价  |
|  `tick.ask3_quantity`  | `float`  |  卖三数量  |
|   `tick.ask3_price`    | `float`  |  卖三报价  |
|  `tick.ask4_quantity`  | `float`  |  卖四数量  |
|   `tick.ask4_price`    | `float`  |  卖四报价  |
|  `tick.ask5_quantity`  | `float`  |  卖五数量  |
|   `tick.ask5_price`    | `float`  |  卖五报价  |
|    `tick.timestamp`    |  `str`   |   时间戳   |

------

## Kline行情

```python
kline = Market.kline("sh601003", "1d", adj=None, start_date=None, end_date=None)
```



------

## 上证综指与深圳成指

```python
Market.shanghai_component_index()		# 获取上证综指
```

```python
Market.shenzhen_component_index()		# 获取深圳成指
```

------

## 其他

```python
Market.stocks_list()		# 股票列表,获取基础信息数据，包括股票代码、名称、上市日期、退市日期等
```

```python
Market.today_is_open()	# 查询今日沪深股市是否开盘，如果开盘返回True,反之False
```

```python
Market.new_stock()		# 获取新股上市列表数据
```

------

# 金融指标

```python
from stockquant.quant import *


config.loads('config.json')
kline = Market.kline("sh601003", "1d")
```

|         指标名称         |               调用方式                |                            返回值                            |
| :----------------------: | :-----------------------------------: | :----------------------------------------------------------: |
|     `指数移动平均线`     |        `ATR(14, kline=kline)`         |                          `一维数组`                          |
|     `k线数据的长度`      |       `CurrentBar(kline=kline)`       |                          `整型数字`                          |
|          `布林`          |        `BOLL(20, kline=kline)`        | `{"upperband": 上轨， "middleband": 中轨， "lowerband": 下轨}` |
|        `顺势指标`        |        `CCI(20, kline=kline)`         |                          `一维数组`                          |
|       `周期最高价`       |      `HIGHEST(20, kline=kline)`       |                          `一维数组`                          |
|       `移动平均线`       |       `MA(20, 30, kline=kline)`       |                          `一维数组`                          |
|   `指数平滑异同平均线`   |    `MACD(14, 26, 9, kline=kline)`     |     `{'DIF': DIF数组, 'DEA': DEA数组, 'MACD': MACD数组}`     |
|       `指数平均数`       |      `EMA(20, 30, kline=kline)`       |                          `一维数组`                          |
| `考夫曼自适应移动平均线` |      `KAMA(20, 30, kline=kline)`      |                          `一维数组`                          |
|        `随机指标`        |     `KDJ(20, 30, 9, kline=kline)`     |               `{'k': k值数组， 'd': d值数组}`                |
|       `周期最低价`       |       `LOWEST(20, kline=kline)`       |                          `一维数组`                          |
|         `能量潮`         |          `OBV(kline=kline)`           |                          `一维数组`                          |
|        `强弱指标`        |        `RSI(20, kline=kline)`         |                          `一维数组`                          |
|       `变动率指标`       |        `ROC(20, kline=kline)`         |                          `一维数组`                          |
|    `随机相对强弱指数`    |  `STOCHRSI(20, 30, 9, kline=kline)`   |       `{'stochrsi': stochrsi数组, 'fastk': fastk数组}`       |
|       `抛物线指标`       |          `SAR(kline=kline)`           |                          `一维数组`                          |
|        `标准方差`        | `STDDEV(20, kline=kline, nbdev=None)` |                          `一维数组`                          |
|   `三重指数平滑平均线`   |        `TRIX(20, kline=kline)`        |                          `一维数组`                          |
|         `成交量`         |         `VOLUME(kline=kline)`         |                          `一维数组`                          |

------

`2021/01/19`

