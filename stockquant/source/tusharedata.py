import tushare as ts
from stockquant.config import config


class TuShareData:

    @staticmethod
    def new_stock():
        """获取新股上市列表数据"""
        pro = ts.pro_api(config.tushare_api)
        result = pro.new_share()
        return result