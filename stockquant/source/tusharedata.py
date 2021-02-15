import tushare as ts
from stockquant.config import config


class TuShareData:

    @staticmethod
    def new_stock():
        """获取新股上市列表数据"""
        pro = ts.pro_api(config.tushare_api)
        result = pro.new_share()
        return result

    @staticmethod
    def stocks_list():
        """股票列表,获取基础信息数据，包括股票代码、名称、上市日期、退市日期等"""
        pro = ts.pro_api(config.tushare_api)
        response = pro.query('stock_basic', exchange='', list_status='L',
                             fields='ts_code,symbol,name,area,industry,list_date')
        return response