from stockquant.source.baostockdata import BaoStockData
from stockquant.source.sinadata import SinaData
from stockquant.source.tushare_pro import TuShare
from stockquant.utils.tools import get_localtime


class Market:

    @staticmethod
    def tick(symbol):
        """
        获取指定股票的实时数据
        :param symbol: 例如："sh601003"，或者"sz002307"，前者是沪市，后者是深市
        :return:返回一个字典
        """
        return SinaData.get_realtime_data(symbol)

    @staticmethod
    def shenzhen_component_index():
        """
        获取深圳成指
        :return:返回一个字典
        """
        return SinaData.shenzhen_component_index()

    @staticmethod
    def shanghai_component_index():
        """
        获取上证综指
        :return:
        """
        return SinaData.shanghai_component_index()

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
        return BaoStockData.query_history_k_data_plus(symbol, timeframe, adj=adj, start_date=start_date, end_date=end_date)

    @staticmethod
    def stocks_list(day=None):
        """股票列表,获取基础信息数据，包括股票代码、名称、上市日期、退市日期等"""
        return BaoStockData.query_all_stock(day=day)

    @staticmethod
    def today_is_open():
        """查询今日沪深股市是否开盘，如果开盘返回True,反之False"""
        today = get_localtime()[0: 10]
        result = BaoStockData.query_trade_dates(start_date=today, end_date=today)['is_trading_day'][0]
        return True if result == '1' else False

    @staticmethod
    def stock_basic_info(symbol=None, symbol_name=None):
        """
        证券基本资料
        方法说明：获取证券基本资料，可以通过参数设置获取对应证券代码、证券名称的数据。
        返回类型：pandas的DataFrame类型。
        :param symbol:A股股票代码，sh或sz+6位数字代码，或者指数代码，如：sh601398。sh：上海；sz：深圳。可以为空；
        :param symbol_name:股票名称，支持模糊查询，可以为空。
        """
        code = 'sh.' + str(symbol).split('sh')[1] if str(symbol).startswith("sh") else 'sz.' + str(symbol).split('sz')[1]
        return BaoStockData.query_stock_basic(code, symbol_name)

    @staticmethod
    def dividend_data(symbol, year, yearType):
        """
        查询除权除息信息
        :param symbol：股票代码，sh或sz+6位数字代码，或者指数代码，如：sh601398。sh：上海；sz：深圳。此参数不可为空；
        :param year：年份，如：2017。此参数不可为空；
        :param yearType：年份类别。"report":预案公告年份，"operate":除权除息年份。此参数不可为空。
        """
        code = 'sh.' + str(symbol).split('sh')[1] if str(symbol).startswith("sh") else 'sz.' + str(symbol).split('sz')[1]
        return BaoStockData.query_dividend_data(code, year, yearType)

    @staticmethod
    def adjust_factor(symbol, start_date=None, end_date=None):
        """
        查询复权因子信息
        BaoStock提供的是涨跌幅复权算法复权因子
        :param symbol:股票代码，sh或sz+6位数字代码，或者指数代码，如：sh601398。sh：上海；sz：深圳。此参数不可为空；
        :param start_date：开始日期，为空时默认为2015-01-01，包含此日期；
        :param end_date：结束日期，为空时默认当前日期，包含此日期。
        """
        code = 'sh.' + str(symbol).split('sh')[1] if str(symbol).startswith("sh") else 'sz.' + str(symbol).split('sz')[1]
        return BaoStockData.query_adjust_factor(code, start_date, end_date)

    @staticmethod
    def new_stock():
        """获取新股上市列表数据"""
        return TuShare.new_stock()


if __name__ == '__main__':

    # print(Market.stocks_list(day="2021-01-28"))
    print(Market.stock_basic_info())