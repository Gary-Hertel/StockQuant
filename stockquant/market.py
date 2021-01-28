from stockquant.source.baostock import BaoStockData
from stockquant.source.sina import Sina
from stockquant.source.tushare_pro import TuShare


class Market:

    @staticmethod
    def tick(symbol):
        """
        获取指定股票的实时数据
        :param symbol: 例如："sh601003"，或者"sz002307"，前者是沪市，后者是深市
        :return:返回一个字典
        """
        return Sina.get_realtime_data(symbol)

    @staticmethod
    def shenzhen_component_index():
        """
        获取深圳成指
        :return:返回一个字典
        """
        return Sina.shenzhen_component_index()

    @staticmethod
    def shanghai_component_index():
        """
        获取上证综指
        :return:
        """
        return Sina.shanghai_component_index()

    @staticmethod
    def kline(symbol, timeframe, adj=None, start_date=None, end_date=None):
        """
        获取历史k线数据
        :param symbol:例如："sh601003"，或者"sz002307"，前者是沪市，后者是深市
        :param timeframe:k线周期，区分大小写，支持："5m", "15m", "30m", "1h", "1d", "1w", "1M，分别为5、15、30分钟、1小时、1天、1周、1月
        :param adj:复权类型，默认是"3"不复权；前复权:"2"；后复权:"1"。已支持分钟线、日线、周线、月线前后复权。 BaoStock提供的是涨跌幅复权算法复权因子
        :param start_date:开始日期（包含），格式“YYYY-MM-DD”，为空时取2015-01-01；
        :param end_date:结束日期（包含），格式“YYYY-MM-DD”，为空时取最近一个交易日；
        :return:返回一个列表,其中每一条k线数据包含在一个列表中
        """
        return BaoStockData.fetch_kline(symbol, timeframe, adj=adj, start_date=start_date, end_date=end_date)

    @staticmethod
    def stocks_list():
        """股票列表,获取基础信息数据，包括股票代码、名称、上市日期、退市日期等"""
        return TuShare.stocks_list()

    @staticmethod
    def today_is_open():
        """查询今日沪深股市是否开盘，如果开盘返回True,反之False"""
        return TuShare.today_is_open()

    @staticmethod
    def new_stock():
        """获取新股上市列表数据"""
        return TuShare.new_stock()