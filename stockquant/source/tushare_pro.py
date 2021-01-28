import tushare as ts
from stockquant.config import config
from stockquant.utils.tools import get_date


class TuShare:

    def __init__(self):
        pass

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