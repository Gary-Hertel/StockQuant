import baostock as bs
import pandas as pd
from stockquant.utils.logger import logger
from stockquant.config import config


class BaoStockData:

    def __init__(self):
        pass

    @staticmethod
    def fetch_kline(symbol, timeframe, adj=None, start_date=None, end_date=None):
        """
        获取k线数据
        注意：
            股票停牌时，对于日线，开、高、低、收价都相同，且都为前一交易日的收盘价，成交量、成交额为0，换手率为空。
        :param symbol:股票代码，sh或sz+6位数字代码，或者指数代码，如：sh601398。sh：上海；sz：深圳。此参数不可为空；
        :param timeframe:k线周期，"5m"为5分钟，"15m"为15分钟，"30m"为30分钟，"1h"为1小时，"1d"为日，"1w"为一周，"1M"为一月。指数没有分钟线数据；周线每周最后一个交易日才可以获取，月线每月最后一个交易日才可以获取。
        :param adj:复权类型，默认是"3"不复权；前复权:"2"；后复权:"1"。已支持分钟线、日线、周线、月线前后复权。 BaoStock提供的是涨跌幅复权算法复权因子，具体介绍见：复权因子简介或者BaoStock复权因子简介。
        :param start_date:开始日期（包含），格式“YYYY-MM-DD”，为空时取2015-01-01；
        :param end_date:结束日期（包含），格式“YYYY-MM-DD”，为空时取最近一个交易日；
        :return:返回一个列表
        """
        frequency = ''
        if timeframe == "5m":
            frequency = "5"
        elif timeframe == "15m":
            frequency = "15"
        elif timeframe == "30m":
            frequency = "30"
        elif timeframe == "1h":
            frequency = "60"
        elif timeframe == "1d":
            frequency = "d"
        elif timeframe == "1w":
            frequency = 'w'
        elif timeframe == "1M":
            frequency = "m"
        else:
            logger.error("timeframe error ！")

        fields = ''
        if 'm' in timeframe or 'h' in timeframe:
            fields = "date,time,code,open,high,low,close,volume,amount,adjustflag"
        elif "d" in timeframe:
            fields = "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,isST"
        elif 'w' in timeframe or 'M' in timeframe:
            fields = "date,code,open,high,low,close,volume,amount,adjustflag,turn,pctChg"
        else:
            logger.error("timeframe error !")

        stock_name = 'sh.' + str(symbol).split('sh')[1] if str(symbol).startswith("sh") else 'sz.' + str(symbol).split('sz')[1]
        adjust_flag = "3" if not adj else adj

        lg = bs.login()
        if lg.error_code != "0":
            logger.error("error: {}".format(lg.error_msg))

        rs = bs.query_history_k_data_plus(
            code=stock_name,
            fields=fields,
            start_date=start_date,
            end_date=end_date,
            frequency=frequency,
            adjustflag=adjust_flag
        )
        if rs.error_code != "0":
            logger.error('fetch kline data error: {}'.format(rs.error_msg))

        data_list = []
        while (rs.error_code == '0') & rs.next():
            data_list.append(rs.get_row_data())
        result = pd.DataFrame(data_list, columns=rs.fields)

        lg = bs.logout()
        if lg.error_code != "0":
            logger.error("error: {}".format(lg.error_msg))

        if 'm' in timeframe or 'h' in timeframe:
            result = result.drop("date", axis=1)
        result = result.drop('code', axis=1)
        result = result.values.tolist()
        return result


if __name__ == '__main__':

    config.loads('config.json')
    bao = BaoStockData()
    print(bao.fetch_kline("sh000001", "1d", adj='2'))