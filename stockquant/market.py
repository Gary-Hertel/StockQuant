from stockquant.source.baostockdata import BaoStockData
from stockquant.source.sinadata import SinaData
from stockquant.source.aksharedata import AkShareData
from stockquant.source.tusharedata import TuShareData
from stockquant.utils.tools import get_localtime
from stockquant.utils.logger import logger


class Market:

    """
    SinaData
    """

    @staticmethod
    def tick(symbol):
        """
        获取指定股票的实时数据
        :param symbol: 例如："sh601003"，或者"sz002307"，前者是沪市，后者是深市
        :return:返回一个字典
        """
        logger.debug("It is recommended to increase the time interval when calling real-time data ！")
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

    """
    BaoStockData
    """

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
    def profit_data(symbol, year=None, quarter=None):
        """
        季频盈利能力
        方法说明：通过API接口获取季频盈利能力信息，可以通过参数设置获取对应年份、季度数据，提供2007年至今数据。
        返回类型：pandas的DataFrame类型。
        参数含义：
        symbol：股票代码，sh或sz+6位数字代码，或者指数代码，如：sh601398。sh：上海；sz：深圳。此参数不可为空；
        year：统计年份，为空时默认当前年；
        quarter：统计季度，可为空，默认当前季度。不为空时只有4个取值：1，2，3，4。
        """
        code = 'sh.' + str(symbol).split('sh')[1] if str(symbol).startswith("sh") else 'sz.' + str(symbol).split('sz')[1]
        return BaoStockData.query_profit_data(code, year, quarter)

    @staticmethod
    def operation_data(symbol, year=None, quarter=None):
        """
        季频营运能力
        方法说明：通过API接口获取季频营运能力信息，可以通过参数设置获取对应年份、季度数据，提供2007年至今数据。
        返回类型：pandas的DataFrame类型。
        参数含义：
        symbol：股票代码，sh或sz+6位数字代码，或者指数代码，如：sh601398。sh：上海；sz：深圳。此参数不可为空；
        year：统计年份，为空时默认当前年；
        quarter：统计季度，为空时默认当前季度。不为空时只有4个取值：1，2，3，4。
        """
        code = 'sh.' + str(symbol).split('sh')[1] if str(symbol).startswith("sh") else 'sz.' + str(symbol).split('sz')[1]
        return BaoStockData.query_operation_data(code, year, quarter)

    @staticmethod
    def growth_data(symbol, year=None, quarter=None):
        """
        季频成长能力
        方法说明：通过API接口获取季频成长能力信息，可以通过参数设置获取对应年份、季度数据，提供2007年至今数据。
        返回类型：pandas的DataFrame类型。
        参数含义：
        symbol：股票代码，sh或sz+6位数字代码，或者指数代码，如：sh601398。sh：上海；sz：深圳。此参数不可为空；
        year：统计年份，为空时默认当前年；
        quarter：统计季度，为空时默认当前季度。不为空时只有4个取值：1，2，3，4。
        """
        code = 'sh.' + str(symbol).split('sh')[1] if str(symbol).startswith("sh") else 'sz.' + str(symbol).split('sz')[1]
        return BaoStockData.query_growth_data(code, year, quarter)

    @staticmethod
    def balance_data(symbol, year=None, quarter=None):
        """
        季频偿债能力
        通过API接口获取季频偿债能力信息，可以通过参数设置获取对应年份、季度数据，提供2007年至今数据。
        返回类型：pandas的DataFrame类型。
        参数含义：
        symbol：股票代码，sh或sz+6位数字代码，或者指数代码，如：sh601398。sh：上海；sz：深圳。此参数不可为空；
        year：统计年份，为空时默认当前年；
        quarter：统计季度，为空时默认当前季度。不为空时只有4个取值：1，2，3，4。
        """
        code = 'sh.' + str(symbol).split('sh')[1] if str(symbol).startswith("sh") else 'sz.' + str(symbol).split('sz')[1]
        return BaoStockData.query_balance_data(code, year, quarter)

    @staticmethod
    def cash_flow_data(symbol, year=None, quarter=None):
        """
        季频现金流量
        方法说明：通过API接口获取季频现金流量信息，可以通过参数设置获取对应年份、季度数据，提供2007年至今数据。
        返回类型：pandas的DataFrame类型.
        参数含义：
        symbol：股票代码，sh或sz+6位数字代码，或者指数代码，如：sh601398。sh：上海；sz：深圳。此参数不可为空；
        year：统计年份，为空时默认当前年；
        quarter：统计季度，为空时默认当前季度。不为空时只有4个取值：1，2，3，4。
        """
        code = 'sh.' + str(symbol).split('sh')[1] if str(symbol).startswith("sh") else 'sz.' + str(symbol).split('sz')[1]
        return BaoStockData.query_cash_flow_data(code, year, quarter)

    @staticmethod
    def dupont_data(symbol, year=None, quarter=None):
        """
        季频杜邦指数
        方法说明：通过API接口获取季频杜邦指数信息，可以通过参数设置获取对应年份、季度数据，提供2007年至今数据。
        返回类型：pandas的DataFrame类型。
        参数含义：
        symbol：股票代码，sh或sz+6位数字代码，或者指数代码，如：sh601398。sh：上海；sz：深圳。此参数不可为空；
        year：统计年份，为空时默认当前年；
        quarter：统计季度，为空时默认当前季度。不为空时只有4个取值：1，2，3，4。
        """
        code = 'sh.' + str(symbol).split('sh')[1] if str(symbol).startswith("sh") else 'sz.' + str(symbol).split('sz')[1]
        return BaoStockData.query_dupont_data(code, year, quarter)

    @staticmethod
    def performance_express_report(symbol, start_date, end_date):
        """
        季频公司业绩快报
        方法说明：通过API接口获取季频公司业绩快报信息，可以通过参数设置获取起止年份数据，提供2006年至今数据。
        返回类型：pandas的DataFrame类型。
        参数含义：
        symbol：股票代码，sh或sz+6位数字代码，或者指数代码，如：sh601398。sh：上海；sz：深圳。此参数不可为空；
        start_date：开始日期，发布日期或更新日期在这个范围内；
        end_date：结束日期，发布日期或更新日期在这个范围内。
        """
        code = 'sh.' + str(symbol).split('sh')[1] if str(symbol).startswith("sh") else 'sz.' + str(symbol).split('sz')[1]
        return BaoStockData.query_performance_express_report(code, start_date, end_date)

    @staticmethod
    def forcast_report(symbol, start_date, end_date):
        """
        季频公司业绩预告
        方法说明：通过API接口获取季频公司业绩预告信息，可以通过参数设置获取起止年份数据，提供2003年至今数据。
        返回类型：pandas的DataFrame类型。
        参数含义：
        symbol：股票代码，sh或sz+6位数字代码，或者指数代码，如：sh601398。sh：上海；sz：深圳。此参数不可为空；
        start_date：开始日期，发布日期或更新日期在这个范围内；
        end_date：结束日期，发布日期或更新日期在这个范围内。
        """
        code = 'sh.' + str(symbol).split('sh')[1] if str(symbol).startswith("sh") else 'sz.' + str(symbol).split('sz')[1]
        return BaoStockData.query_forcast_report(code, start_date, end_date)

    @staticmethod
    def deposit_rate_data(start_date=None, end_date=None):
        """
        存款利率
        方法说明：通过API接口获取存款利率，可以通过参数设置获取对应起止日期的数据。
        返回类型：pandas的DataFrame类型。
        参数含义：
        start_date：开始日期，格式XXXX-XX-XX，发布日期在这个范围内，可以为空；
        end_date：结束日期，格式XXXX-XX-XX，发布日期在这个范围内，可以为空。
        """
        return BaoStockData.query_deposit_rate_data(start_date, end_date)

    @staticmethod
    def loan_rate_data(start_date=None, end_date=None):
        """
        贷款利率
        方法说明：通过API接口获取贷款利率，可以通过参数设置获取对应起止日期的数据。
        返回类型：pandas的DataFrame类型。
        参数含义：
        start_date：开始日期，格式XXXX-XX-XX，发布日期在这个范围内，可以为空；
        end_date：结束日期，格式XXXX-XX-XX，发布日期在这个范围内，可以为空。
        """
        return BaoStockData.query_loan_rate_data(start_date, end_date)

    @staticmethod
    def required_reserve_ratio_data(start_date=None, end_date=None, yearType=None):
        """
        存款准备金率
        方法说明：通过API接口获取存款准备金率，可以通过参数设置获取对应起止日期的数据。
        返回类型：pandas的DataFrame类型。
        参数含义：
        start_date：开始日期，格式XXXX-XX-XX，发布日期在这个范围内，可以为空；
        end_date：结束日期，格式XXXX-XX-XX，发布日期在这个范围内，可以为空；
        yearType:年份类别，默认为0，查询公告日期；1查询生效日期。
        """
        return BaoStockData.query_required_reserve_ratio_data(start_date, end_date, yearType)

    @staticmethod
    def money_supply_data_month(start_date=None, end_date=None):
        """
        货币供应量
        方法说明：通过API接口获取货币供应量，可以通过参数设置获取对应起止日期的数据。
        返回类型：pandas的DataFrame类型。
        参数含义：
        start_date：开始日期，格式XXXX-XX，发布日期在这个范围内，可以为空；
        end_date：结束日期，格式XXXX-XX，发布日期在这个范围内，可以为空。
        """
        return BaoStockData.query_money_supply_data_month(start_date, end_date)

    @staticmethod
    def money_supply_data_year(start_date=None, end_date=None):
        """
        货币供应量(年底余额)
        方法说明：通过API接口获取货币供应量(年底余额)，可以通过参数设置获取对应起止日期的数据。
        返回类型：pandas的DataFrame类型。
        参数含义：
        start_date：开始日期，格式XXXX，发布日期在这个范围内，可以为空；
        end_date：结束日期，格式XXXX，发布日期在这个范围内，可以为空。
        """
        return BaoStockData.query_money_supply_data_year(start_date, end_date)

    @staticmethod
    def shibor_data(start_date=None, end_date=None):
        """
        银行间同业拆放利率
        方法说明：通过API接口获取银行间同业拆放利率，可以通过参数设置获取对应起止日期的数据。
        返回类型：pandas的DataFrame类型。
        参数含义：
        start_date：开始日期，格式XXXX，发布日期在这个范围内，可以为空；
        end_date：结束日期，格式XXXX，发布日期在这个范围内，可以为空。
        """
        return BaoStockData.query_shibor_data(start_date, end_date)

    @staticmethod
    def stock_industry(symbol=None, date=None):
        """
        行业分类
        方法说明：通过API接口获取行业分类信息，更新频率：每周一更新。
        返回类型：pandas的DataFrame类型。
        参数含义：
        symbol：A股股票代码，sh或sz+6位数字代码，或者指数代码，如：sh601398。sh：上海；sz：深圳。可以为空；
        date：查询日期，格式XXXX-XX-XX，为空时默认最新日期。
        """
        if symbol:
            code = 'sh.' + str(symbol).split('sh')[1] if str(symbol).startswith("sh") else 'sz.' + str(symbol).split('sz')[1]
        else:
            code = None

        return BaoStockData.query_stock_industry(code, date)

    @staticmethod
    def sz50_stocks(date=None):
        """
        上证50成分股
        方法说明：通过API接口获取上证50成分股信息，更新频率：每周一更新。
        返回类型：pandas的DataFrame类型。
        参数含义：
        date：查询日期，格式XXXX-XX-XX，为空时默认最新日期。
        """
        return BaoStockData.query_sz50_stocks(date)

    @staticmethod
    def hs300_stocks(date=None):
        """"
        沪深300成分股
        方法说明：通过API接口获取沪深300成分股信息，更新频率：每周一更新。
        返回类型：pandas的DataFrame类型。
        参数含义：
        date：查询日期，格式XXXX-XX-XX，为空时默认最新日期。
        """
        return BaoStockData.query_hs300_stocks(date)

    @staticmethod
    def zz500_stocks(date=None):
        """
        中证500成分股
        方法说明：通过API接口获取中证500成分股信息，更新频率：每周一更新。
        返回类型：pandas的DataFrame类型。
        date：查询日期，格式XXXX-XX-XX，为空时默认最新日期。
        """
        return BaoStockData.query_zz500_stocks(date)

    """
    AkShareData
    """

    @staticmethod
    def stock_sse_summary_df():
        """
        上海证券交易所-股票数据总貌
        限量: 单次返回最近交易日的股票数据总貌数据(当前交易日的数据需要交易所收盘后统计)
        """
        return AkShareData.stock_sse_summary_df()

    @staticmethod
    def stock_szse_summary():
        """
        深圳证券交易所-市场总貌
        限量: 单次返回最近交易日的市场总貌数据(当前交易日的数据需要交易所收盘后统计)
        """
        return AkShareData.stock_szse_summary()

    @staticmethod
    def all_stock_tick():
        """
        描述: A 股数据是从新浪财经获取的数据, 重复运行本函数会被新浪暂时封 IP, 建议增加时间间隔
        限量: 单次返回所有 A 股上市公司的实时行情数据
        """
        logger.debug("It is recommended to increase the time interval when calling real-time data ！")
        return AkShareData.all_stock_tick()

    @staticmethod
    def stock_zh_index_spot():
        """
        描述: 股票指数数据是从新浪财经获取的数据
        限量: 单次返回所有指数的实时行情数据
        """
        logger.debug("It is recommended to increase the time interval when calling real-time data ！")
        return AkShareData.stock_zh_index_spot()

    """
    TuShareData
    """

    @staticmethod
    def new_stock():
        """获取新股上市列表数据"""
        return TuShareData.new_stock()

    @staticmethod
    def stocks_list():
        """股票列表,获取基础信息数据，包括股票代码、名称、上市日期、退市日期等"""
        return TuShareData.stocks_list()


if __name__ == '__main__':

    # print(Market.stocks_list(day="2021-01-28"))
    print(Market.stock_basic_info())