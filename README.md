# StockQuant

`Gary-Hertel`

请勿提交`issue`！可以加入交流群与其他朋友一起自学交流，加微信`mzjimmy`

------

## 一、配置文件的设置

**启动框架需要先导入必要的模块，并且载入一次配置文件！**

配置文件是一个`json`格式的文件`config.json`，在`docs`文件夹中有模板文件，其内容如下，将其中的信息替换成自己的即可：

```json
{
    "LOG": {
        "level": "debug",
        "handler": "stream"
    },
    "DINGTALK": "your dingding token",
    "TUSHARE": "your tushare token",
    "SENDMAIL": {
        "from": "your qq email address",
        "password": "your qq email authorization code",
        "to": "your qq email address",
        "server": "smtp.qq.com",
        "port": 587
    }
}
```

其中的内容说明：

+ `LOG`：日志配置
  + `level`：日志显示的等级，可选`debug`、`info`、`error`、`warning`、`critical`
  + `handler`：日志的输出方式，可选`stream`、`file`、`time`
+ `DINGTALK`：你的钉钉`webhook token`
+ `TUSHARE`：你的`tushare_pro token`
+ `SENDMAIL`：邮箱配置
  + `from`：发件邮箱，推荐使用`QQ`邮箱
  + `password`：你的`QQ`邮箱授权码，非`QQ`密码
  + `to`：收件邮箱，推荐使用`QQ`邮箱并在微信上绑定此邮箱以实现微信接收消息
  + `server`：邮箱服务器，`QQ`邮箱默认使用此服务器
  + `port`：邮箱端口，`QQ`邮箱默认此端口即可

除了配置的这些信息外，也可以向配置文件中添加任意的信息，但注意**不能与默认设置内容中大写的内容名称相同，即使你添加的信息是小写亦不可**！要在策略中使用向配置文件中增加的信息，示例如下：

> 比如我们向配置文件中添加一项信息
>
> ```json
> {
>     "LOG": {
>         "level": "debug",
>         "handler": "stream"
>     },
>     "DINGTALK": "your dingding token",
>     "TUSHARE": "your tushare token",
>     "SENDMAIL": {
>         "from": "your qq email address",
>         "password": "your qq email authorization code",
>         "to": "your qq email address",
>         "server": "smtp.qq.com",
>         "port": 587
>     },
>     "person_name": "Gary-Hertel"
> }
> ```
>
> 要在策略中使用，只需：
>
> ```python
> config.person_name
> ```



------

## 二、框架的启用

在我们配置好配置文件后，将其放入我们的项目中，接下来就可以使用我们的框架了：

```python
from stockquant.quant import *		# 导入必要的模块

config.loads('config.json')			# 载入配置文件
```



------

## 三、行情数据

行情数据获取，具体参数请看方法内部的说明文档，在开发工具中，按住`ctrl`用鼠标点击一下方法的名称即可查看。

| 说明                     |                           调用方式                           |
| :----------------------- | :----------------------------------------------------------: |
| 获取指定股票的实时数据   |                    `Market.tick(symbol)`                     |
| 获取深圳成指             |             `Market.shenzhen_component_index()`              |
| 获取上证综指             |             `Market.shanghai_component_index()`              |
| 获取历史k线数据          | `Market.kline(symbol, timeframe, adj=None, start_date=None, end_date=None)` |
| 股票列表                 |                `Market.stocks_list(day=None)`                |
| 查询今日沪深股市是否开盘 |                   `Market.today_is_open()`                   |
| 证券基本资料             |   `Market.stock_basic_info(symbol=None, symbol_name=None)`   |
| 查询除权除息信息         |        `Market.dividend_data(symbol, year, yearType)`        |
| 查询复权因子信息         | `Market.adjust_factor(symbol, start_date=None, end_date=None)` |
| 季频盈利能力             |    `Market.profit_data(symbol, year=None, quarter=None)`     |
| 季频营运能力             |   `Market.operation_data(symbol, year=None, quarter=None)`   |
| 季频成长能力             |    `Market.growth_data(symbol, year=None, quarter=None)`     |
| 季频偿债能力             |    `Market.balance_data(symbol, year=None, quarter=None)`    |
| 季频现金流量             |   `Market.cash_flow_data(symbol, year=None, quarter=None)`   |
| 季频杜邦指数             |    `Market.dupont_data(symbol, year=None, quarter=None)`     |
| 季频公司业绩快报         | `Market.performance_express_report(symbol, start_date, end_date)` |
| 季频公司业绩预告         |    `Market.forcast_report(symbol, start_date, end_date)`     |
| 存款利率                 |  `Market.deposit_rate_data(start_date=None, end_date=None)`  |
| 贷款利率                 |   `Market.loan_rate_data(start_date=None, end_date=None)`    |
| 存款准备金率             | `Market.required_reserve_ratio_data(start_date=None, end_date=None, yearType=None)` |
| 货币供应量               | `Market.money_supply_data_month(start_date=None, end_date=None)` |
| 货币供应量(年底余额)     | `Market.money_supply_data_year(start_date=None, end_date=None)` |
| 银行间同业拆放利率       |     `Market.shibor_data(start_date=None, end_date=None)`     |
| 获取行业分类信息         |       `Market.stock_industry(symbol=None, date=None)`        |
| 获取上证50成分股信息     |               `Market.sz50_stocks(date=None)`                |
| 沪深300成分股            |               `Market.hs300_stocks(date=None)`               |
| 中证500成分股            |               `Market.zz500_stocks(date=None)`               |
| 获取新股上市列表数据     |                     `Market.new_stock()`                     |

**Note: 获取指定股票的实时数据时，Tick对象数据结构如下：**

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



## 四、技术指标

```python
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

## 五、日志

日志模块对于分析程序的运行状况至关重要，`StockQuant`内置日志模块，可用来方便记录程序运行状况与排查问题。

日志一共分成5个等级，从低到高分别是：

1. DEBUG
2. INFO
3. WARNING
4. ERROR
5. CRITICAL

```python
logger.debug("DEBUG日志")
logger.info("INFO日志")
logger.warning("WARNING日志")
logger.error("ERROR日志")
logger.critical("CRITICAL日志")
```

配置文件中，`level`如设置成`debug`级别，则会输出所有级别的日志，如设置成`info`级别，只会输出`info`及以上级别的日志，而不会输出`debug`级别的日志。

配置文件中，`handler`如设置为`stream`，是打印日志到控制台；如设为`file`是保存至文件，文件大小按`1M`进行分割，会保留最近的`1000`份日志文件；如设置为`time`是按照每天进行分割。

**`Note`：如果是在宝塔面板上运行程序，记得将配置文件中`LOG`的`handler`设置不要设置为`stream`，否则会一直写入日志，并且不会自动分割日志。**



------

## 六、信息推送

信息推送对于风控通知来说是至关重要的。`StockQuant`内置信息推送模块，可直接调用以推送信息至钉钉或邮箱。

### 1.钉钉

`Note`：需在配置文件中设置钉钉`WebHook Api`，建立钉钉群聊后添加一个`WebHook`机器人，创建机器人时指定关键字如`交易`。

#### （1）推送文本类型信息

推送文本类型信息时需包含关键字，否则无法送达。

```python
Dingralk.text("交易提醒：sh600519的价格已达到2000元！")
```

#### （2）推送`markdown`类型信息

推送`markdown`信息时无需包含关键字（前提是你的关键字设置的是`交易`）。下面看一个示例：

```python
from stockquant.quant import *

config.loads('config.json')

tick = Market.tick("sh600519")

content = "### 订单更新推送\n\n" \
            "> **股票名称:** {symbol}\n\n" \
            "> **当前价格:** {last}\n\n" \
            "> **成交数量:** {transactions}\n\n" \
            "> **成交金额:** {turnover}\n\n" \
            "> **时间戳:** {timestamp}".format(
                symbol=tick.symbol,
                last=tick.last,
                transactions=tick.transactions,
                turnover=tick.turnover,
                timestamp=tick.timestamp
            )
DingTalk.markdown(content)
```

### 2.邮件

```python
sendmail("交易提醒：sh600519的价格已达到2000美元！")
```



------

## 七、数据存储

```python
txt_save(content, filename)						 # 保存数据至txt文件
txt_read(filename)								# 读取txt文件中的数据
save_to_csv_file(tuple, path)					 # 保存文件至csv文件
read_csv_file(path)								# 读取csv文件中保存的数据
```



------

## 八、时间戳转换的一些方法

```python
sleep(seconds)							# 休眠，作用等同于time.sleep()
get_cur_timestamp()						# 获取当前时间戳（秒）
ts_to_utc_str(ts)						# 将时间戳转换为UTC时间格式
get_cur_timestamp_ms()					# 获取当前时间戳(毫秒)
get_cur_datetime_m()					# 获取当前日期时间字符串，包含 年 + 月 + 日 + 时 + 分 + 秒
get_datetime()							# 获取日期字符串，包含 年 + 月 + 日
date_str_to_dt(date_str)				# 日期字符串转换到datetime对象
dt_to_date_str(dt)						# datetime对象转换到日期字符串
get_utc_time()							# 获取当前utc时间
get_localtime()							# 获取本地时间
ts_to_datetime_str(ts)					# 将时间戳转换为日期时间格式，年-月-日 时:分:秒
datetime_str_to_ts(dt_str)				# 将日期时间格式字符串转换成时间戳
datetime_to_timestamp(dt)				# 将datetime对象转换成时间戳
utctime_str_to_ts(utctime_str)			# 将UTC日期时间格式字符串转换成时间戳
utctime_str_to_mts(utctime_str)			# 将UTC日期时间格式字符串转换成时间戳（毫秒）
```



## 九、自动交易

```python
"""
股票自动交易，使用的是easytrader开源项目。
仅支持windows系统，云主机与虚拟机上无法运行。
具体用法，可参考哔哩哔哩教学视频：
    https://www.bilibili.com/video/BV1zK411u7uG
"""


from stockquant.quant import *


class Strategy:

    def __init__(self):
        self.trade = Trade(config_file="config.json", symbol="sh512980")    # 初始化trade模块

        self.do_action()

    def do_action(self):
        price = Market.tick("sh512980").ask1_price          # 获取卖一价格
        success, error = self.trade.buy(price, amount)      # 买入
        success, error = self.trade.sell(price, amount)     # 卖出
        success, error = self.trade.get_positions()         # 查询当前持仓
        success, error = self.trade.get_balance()           # 查询资金信息
        success, error = self.trade.get_today_orders()      # 查询今日委托
        success, error = self.trade.get_today_deals()       # 查询今日成交
        if error:
            DingTalk.text("交易提醒：失败：{}".format(error))
            pass
        logger.info("success:{}".format(success))


if __name__ == '__main__':

    Strategy()
```



------

`updated at 2021/03/03`