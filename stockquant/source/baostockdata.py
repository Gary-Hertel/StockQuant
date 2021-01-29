import baostock as bs
import pandas as pd
from stockquant.utils.logger import logger
from stockquant.config import config


class BaoStockData:

    def __init__(self):
        pass

    @staticmethod
    def query_trade_dates(start_date=None, end_date=None):
        """
        交易日查询
        方法说明：通过API接口获取股票交易日信息，可以通过参数设置获取起止年份数据，提供上交所1990-今年数据。 返回类型：pandas的DataFrame类型。
        :param start_date:开始日期，为空时默认为2015-01-01。
        :param end_date:结束日期，为空时默认为当前日期。
        """
        lg = bs.login()
        if lg.error_code != '0':
            logger.error('login respond  error_msg:' + lg.error_msg)

        rs = bs.query_trade_dates(start_date=start_date, end_date=end_date)
        if rs.error_code != '0':
            logger.error('query_trade_dates respond  error_msg:' + rs.error_msg)

        data_list = []
        while (rs.error_code == '0') & rs.next():
            data_list.append(rs.get_row_data())
        result = pd.DataFrame(data_list, columns=rs.fields)

        bs.logout()
        return result

    @staticmethod
    def query_all_stock(day=None):
        """
        证券代码查询
        方法说明：获取指定交易日期所有股票列表。通过API接口获取证券代码及股票交易状态信息，与日K线数据同时更新。可以通过参数‘某交易日’获取数据（包括：A股、指数），提供2006-今数据。
        返回类型：pandas的DataFrame类型。
        更新时间：与日K线同时更新。
        :param day:需要查询的交易日期，为空时默认当前日期。
        """
        lg = bs.login()
        if lg.error_code != '0':
            logger.error('login respond  error_msg:' + lg.error_msg)

        rs = bs.query_all_stock(day=day)
        if rs.error_code != '0':
            logger.error('query_all_stock respond  error_msg:' + rs.error_msg)

        data_list = []
        while (rs.error_code == '0') & rs.next():
            data_list.append(rs.get_row_data())
        result = pd.DataFrame(data_list, columns=rs.fields)

        bs.logout()
        return result

    @staticmethod
    def query_stock_basic(code=None, code_name=None):
        """
        证券基本资料
        方法说明：获取证券基本资料，可以通过参数设置获取对应证券代码、证券名称的数据。
        返回类型：pandas的DataFrame类型。
        :param code:A股股票代码，sh或sz.+6位数字代码，或者指数代码，如：sh.601398。sh：上海；sz：深圳。可以为空；
        :param code_name:股票名称，支持模糊查询，可以为空。
        """
        lg = bs.login()
        if lg.error_code != '0':
            logger.error('login respond  error_msg:' + lg.error_msg)

        rs = bs.query_stock_basic(code=code, code_name=code_name)
        if rs.error_code != '0':
            logger.error('query_stock_basic respond  error_msg:' + rs.error_msg)

        data_list = []
        while (rs.error_code == '0') & rs.next():
            data_list.append(rs.get_row_data())
        result = pd.DataFrame(data_list, columns=rs.fields)

        bs.logout()
        return result

    @staticmethod
    def query_history_k_data_plus(symbol, timeframe, adj=None, start_date=None, end_date=None):
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
            logger.error('query_history_k_data_plus respond error: {}'.format(rs.error_msg))

        data_list = []
        while (rs.error_code == '0') & rs.next():
            data_list.append(rs.get_row_data())
        result = pd.DataFrame(data_list, columns=rs.fields)

        bs.logout()

        if 'm' in timeframe or 'h' in timeframe:
            result = result.drop("date", axis=1)
        result = result.drop('code', axis=1)
        result = result.values.tolist()
        return result

    @staticmethod
    def query_dividend_data(code, year, yearType):
        """
        查询除权除息信息
        :param code：股票代码，sh或sz.+6位数字代码，或者指数代码，如：sh.601398。sh：上海；sz：深圳。此参数不可为空；
        :param year：年份，如：2017。此参数不可为空；
        :param yearType：年份类别。"report":预案公告年份，"operate":除权除息年份。此参数不可为空。
        """
        lg = bs.login()
        if lg.error_code != '1':
            logger.error('login respond  error_msg:' + lg.error_msg)

        rs_list = []
        rs_dividend = bs.query_dividend_data(code=code, year=year, yearType=yearType)
        while (rs_dividend.error_code == '0') & rs_dividend.next():
            rs_list.append(rs_dividend.get_row_data())

        result_dividend = pd.DataFrame(rs_list, columns=rs_dividend.fields)

        bs.logout()
        return result_dividend

    @staticmethod
    def query_adjust_factor(code, start_date=None, end_date=None):
        """
        查询复权因子信息
        BaoStock提供的是涨跌幅复权算法复权因子
        :param code:股票代码，sh或sz.+6位数字代码，或者指数代码，如：sh.601398。sh：上海；sz：深圳。此参数不可为空；
        :param start_date：开始日期，为空时默认为2015-01-01，包含此日期；
        :param end_date：结束日期，为空时默认当前日期，包含此日期。
        """
        lg = bs.login()
        if lg.error_code != '0':
            logger.error('login respond  error_msg:' + lg.error_msg)

        rs_list = []
        rs_factor = bs.query_adjust_factor(code=code, start_date=start_date, end_date=end_date)
        while (rs_factor.error_code == '0') & rs_factor.next():
            rs_list.append(rs_factor.get_row_data())
        result_factor = pd.DataFrame(rs_list, columns=rs_factor.fields)

        bs.logout()
        return result_factor

    @staticmethod
    def query_profit_data(code, year=None, quarter=None):
        """
        季频盈利能力
        方法说明：通过API接口获取季频盈利能力信息，可以通过参数设置获取对应年份、季度数据，提供2007年至今数据。
        返回类型：pandas的DataFrame类型。
        参数含义：
        code：股票代码，sh或sz.+6位数字代码，或者指数代码，如：sh.601398。sh：上海；sz：深圳。此参数不可为空；
        year：统计年份，为空时默认当前年；
        quarter：统计季度，可为空，默认当前季度。不为空时只有4个取值：1，2，3，4。
        """
        lg = bs.login()
        if lg.error_code != '0':
            logger.error('login respond  error_msg:' + lg.error_msg)

        profit_list = []
        rs_profit = bs.query_profit_data(code=code, year=year, quarter=quarter)
        while (rs_profit.error_code == '0') & rs_profit.next():
            profit_list.append(rs_profit.get_row_data())
        result_profit = pd.DataFrame(profit_list, columns=rs_profit.fields)

        bs.logout()
        return result_profit

    @staticmethod
    def query_operation_data(code, year=None, quarter=None):
        """
        季频营运能力
        方法说明：通过API接口获取季频营运能力信息，可以通过参数设置获取对应年份、季度数据，提供2007年至今数据。
        返回类型：pandas的DataFrame类型。
        参数含义：
        code：股票代码，sh或sz.+6位数字代码，或者指数代码，如：sh.601398。sh：上海；sz：深圳。此参数不可为空；
        year：统计年份，为空时默认当前年；
        quarter：统计季度，为空时默认当前季度。不为空时只有4个取值：1，2，3，4。
        """
        lg = bs.login()
        if lg.error_code != '0':
            logger.error('login respond  error_msg:' + lg.error_msg)

        operation_list = []
        rs_operation = bs.query_operation_data(code=code, year=year, quarter=quarter)
        while (rs_operation.error_code == '0') & rs_operation.next():
            operation_list.append(rs_operation.get_row_data())
        result_operation = pd.DataFrame(operation_list, columns=rs_operation.fields)

        bs.logout()
        return result_operation

    @staticmethod
    def query_growth_data(code, year=None, quarter=None):
        """
        季频成长能力
        方法说明：通过API接口获取季频成长能力信息，可以通过参数设置获取对应年份、季度数据，提供2007年至今数据。
        返回类型：pandas的DataFrame类型。
        参数含义：
        code：股票代码，sh或sz.+6位数字代码，或者指数代码，如：sh.601398。sh：上海；sz：深圳。此参数不可为空；
        year：统计年份，为空时默认当前年；
        quarter：统计季度，为空时默认当前季度。不为空时只有4个取值：1，2，3，4。
        """
        lg = bs.login()
        if lg.error_code != '0':
            logger.error('login respond  error_msg:' + lg.error_msg)

        growth_list = []
        rs_growth = bs.query_growth_data(code=code, year=year, quarter=quarter)
        while (rs_growth.error_code == '0') & rs_growth.next():
            growth_list.append(rs_growth.get_row_data())
        result_growth = pd.DataFrame(growth_list, columns=rs_growth.fields)

        bs.logout()
        return result_growth

    @staticmethod
    def query_balance_data(code, year=None, quarter=None):
        """
        季频偿债能力
        通过API接口获取季频偿债能力信息，可以通过参数设置获取对应年份、季度数据，提供2007年至今数据。
        返回类型：pandas的DataFrame类型。
        参数含义：
        code：股票代码，sh或sz.+6位数字代码，或者指数代码，如：sh.601398。sh：上海；sz：深圳。此参数不可为空；
        year：统计年份，为空时默认当前年；
        quarter：统计季度，为空时默认当前季度。不为空时只有4个取值：1，2，3，4。
        """
        lg = bs.login()
        if lg.error_code != '0':
            logger.error('login respond  error_msg:' + lg.error_msg)

        balance_list = []
        rs_balance = bs.query_balance_data(code=code, year=year, quarter=quarter)
        while (rs_balance.error_code == '0') & rs_balance.next():
            balance_list.append(rs_balance.get_row_data())
        result_balance = pd.DataFrame(balance_list, columns=rs_balance.fields)

        bs.logout()
        return result_balance

    @staticmethod
    def query_cash_flow_data(code, year=None, quarter=None):
        """
        季频现金流量
        方法说明：通过API接口获取季频现金流量信息，可以通过参数设置获取对应年份、季度数据，提供2007年至今数据。
        返回类型：pandas的DataFrame类型.
        参数含义：
        code：股票代码，sh或sz.+6位数字代码，或者指数代码，如：sh.601398。sh：上海；sz：深圳。此参数不可为空；
        year：统计年份，为空时默认当前年；
        quarter：统计季度，为空时默认当前季度。不为空时只有4个取值：1，2，3，4。
        """
        lg = bs.login()
        if lg.error_code != '0':
            logger.error('login respond  error_msg:' + lg.error_msg)

        cash_flow_list = []
        rs_cash_flow = bs.query_cash_flow_data(code=code, year=year, quarter=quarter)
        while (rs_cash_flow.error_code == '0') & rs_cash_flow.next():
            cash_flow_list.append(rs_cash_flow.get_row_data())
        result_cash_flow = pd.DataFrame(cash_flow_list, columns=rs_cash_flow.fields)

        bs.logout()
        return result_cash_flow

    @staticmethod
    def query_dupont_data(code, year=None, quarter=None):
        """
        季频杜邦指数
        方法说明：通过API接口获取季频杜邦指数信息，可以通过参数设置获取对应年份、季度数据，提供2007年至今数据。
        返回类型：pandas的DataFrame类型。
        参数含义：
        code：股票代码，sh或sz.+6位数字代码，或者指数代码，如：sh.601398。sh：上海；sz：深圳。此参数不可为空；
        year：统计年份，为空时默认当前年；
        quarter：统计季度，为空时默认当前季度。不为空时只有4个取值：1，2，3，4。
        """
        lg = bs.login()
        if lg.error_code != '0':
            logger.error('login respond  error_msg:' + lg.error_msg)

        dupont_list = []
        rs_dupont = bs.query_dupont_data(code=code, year=year, quarter=quarter)
        while (rs_dupont.error_code == '0') & rs_dupont.next():
            dupont_list.append(rs_dupont.get_row_data())
        result_profit = pd.DataFrame(dupont_list, columns=rs_dupont.fields)

        bs.logout()
        return result_profit

    @staticmethod
    def query_performance_express_report(code, start_date, end_date):
        """
        季频公司业绩快报
        方法说明：通过API接口获取季频公司业绩快报信息，可以通过参数设置获取起止年份数据，提供2006年至今数据。
        返回类型：pandas的DataFrame类型。
        参数含义：
        code：股票代码，sh或sz.+6位数字代码，或者指数代码，如：sh.601398。sh：上海；sz：深圳。此参数不可为空；
        start_date：开始日期，发布日期或更新日期在这个范围内；
        end_date：结束日期，发布日期或更新日期在这个范围内。
        """
        lg = bs.login()
        if lg.error_code != '0':
            logger.error('login respond  error_msg:' + lg.error_msg)

        rs = bs.query_performance_express_report(code, start_date=start_date, end_date=end_date)
        if rs.error_code != '0':
            logger.error('query_performance_express_report respond  error_msg:' + rs.error_msg)

        result_list = []
        while (rs.error_code == '0') & rs.next():
            result_list.append(rs.get_row_data())
        result = pd.DataFrame(result_list, columns=rs.fields)

        bs.logout()
        return result

    @staticmethod
    def query_forcast_report(code, start_date, end_date):
        """
        季频公司业绩预告
        方法说明：通过API接口获取季频公司业绩预告信息，可以通过参数设置获取起止年份数据，提供2003年至今数据。
        返回类型：pandas的DataFrame类型。
        参数含义：
        code：股票代码，sh或sz.+6位数字代码，或者指数代码，如：sh.601398。sh：上海；sz：深圳。此参数不可为空；
        start_date：开始日期，发布日期或更新日期在这个范围内；
        end_date：结束日期，发布日期或更新日期在这个范围内。
        """
        lg = bs.login()
        if lg.error_code != '0':
            logger.error('login respond  error_msg:' + lg.error_msg)

        rs_forecast = bs.query_forecast_report(code, start_date=start_date, end_date=end_date)
        if rs_forecast.error_code != '0':
            logger.error('query_forecast_reprot respond  error_msg:' + rs_forecast.error_msg)

        rs_forecast_list = []
        while (rs_forecast.error_code == '0') & rs_forecast.next():
            rs_forecast_list.append(rs_forecast.get_row_data())
        result_forecast = pd.DataFrame(rs_forecast_list, columns=rs_forecast.fields)

        bs.logout()
        return result_forecast

    @staticmethod
    def query_deposit_rate_data(start_date=None, end_date=None):
        """
        存款利率
        方法说明：通过API接口获取存款利率，可以通过参数设置获取对应起止日期的数据。
        返回类型：pandas的DataFrame类型。
        参数含义：
        start_date：开始日期，格式XXXX-XX-XX，发布日期在这个范围内，可以为空；
        end_date：结束日期，格式XXXX-XX-XX，发布日期在这个范围内，可以为空。
        """
        lg = bs.login()
        if lg.error_code != '0':
            logger.error('login respond  error_msg:' + lg.error_msg)

        rs = bs.query_deposit_rate_data(start_date=start_date, end_date=end_date)
        if rs.error_code != '0':
            logger.error('query_deposit_rate_data respond  error_msg:' + rs.error_msg)

        data_list = []
        while (rs.error_code == '0') & rs.next():
            data_list.append(rs.get_row_data())
        result = pd.DataFrame(data_list, columns=rs.fields)

        bs.logout()
        return result

    @staticmethod
    def query_loan_rate_data(start_date=None, end_date=None):
        """
        贷款利率
        方法说明：通过API接口获取贷款利率，可以通过参数设置获取对应起止日期的数据。
        返回类型：pandas的DataFrame类型。
        参数含义：
        start_date：开始日期，格式XXXX-XX-XX，发布日期在这个范围内，可以为空；
        end_date：结束日期，格式XXXX-XX-XX，发布日期在这个范围内，可以为空。
        """
        lg = bs.login()
        if lg.error_code != '0':
            logger.error('login respond  error_msg:' + lg.error_msg)

        rs = bs.query_loan_rate_data(start_date=start_date, end_date=end_date)
        if rs.error_code != '0':
            logger.error('query_loan_rate_data respond  error_msg:' + rs.error_msg)

        data_list = []
        while (rs.error_code == '0') & rs.next():
            data_list.append(rs.get_row_data())
        result = pd.DataFrame(data_list, columns=rs.fields)

        bs.logout()
        return result

    @staticmethod
    def query_required_reserve_ratio_data(start_date=None, end_date=None, yearType=None):
        """
        存款准备金率
        方法说明：通过API接口获取存款准备金率，可以通过参数设置获取对应起止日期的数据。
        返回类型：pandas的DataFrame类型。
        参数含义：
        start_date：开始日期，格式XXXX-XX-XX，发布日期在这个范围内，可以为空；
        end_date：结束日期，格式XXXX-XX-XX，发布日期在这个范围内，可以为空；
        yearType:年份类别，默认为0，查询公告日期；1查询生效日期。
        """
        yearType = yearType or '0'

        lg = bs.login()
        if lg.error_code != '0':
            logger.error('login respond  error_msg:' + lg.error_msg)

        rs = bs.query_required_reserve_ratio_data(start_date=start_date, end_date=end_date, yearType=yearType)
        if rs.error_code != '0':
            logger.error('query_required_reserve_ratio_data respond  error_msg:' + rs.error_msg)

        data_list = []
        while (rs.error_code == '0') & rs.next():
            data_list.append(rs.get_row_data())
        result = pd.DataFrame(data_list, columns=rs.fields)

        bs.logout()
        return result

    @staticmethod
    def query_money_supply_data_month(start_date=None, end_date=None):
        """
        货币供应量
        方法说明：通过API接口获取货币供应量，可以通过参数设置获取对应起止日期的数据。
        返回类型：pandas的DataFrame类型。
        参数含义：
        start_date：开始日期，格式XXXX-XX，发布日期在这个范围内，可以为空；
        end_date：结束日期，格式XXXX-XX，发布日期在这个范围内，可以为空。
        """
        lg = bs.login()
        if lg.error_code != '0':
            logger.error('login respond  error_msg:' + lg.error_msg)

        rs = bs.query_money_supply_data_month(start_date=start_date, end_date=end_date)
        if rs.error_code != '0':
            logger.error('query_money_supply_data_month respond  error_msg:' + rs.error_msg)

        data_list = []
        while (rs.error_code == '0') & rs.next():
            data_list.append(rs.get_row_data())
        result = pd.DataFrame(data_list, columns=rs.fields)

        bs.logout()
        return result

    @staticmethod
    def query_money_supply_data_year(start_date=None, end_date=None):
        """
        货币供应量(年底余额)
        方法说明：通过API接口获取货币供应量(年底余额)，可以通过参数设置获取对应起止日期的数据。
        返回类型：pandas的DataFrame类型。
        参数含义：
        start_date：开始日期，格式XXXX，发布日期在这个范围内，可以为空；
        end_date：结束日期，格式XXXX，发布日期在这个范围内，可以为空。
        """
        lg = bs.login()
        if lg.error_code != '0':
            logger.error('login respond  error_msg:' + lg.error_msg)

        rs = bs.query_money_supply_data_year(start_date=start_date, end_date=end_date)
        if rs.error_code != '0':
            logger.error('query_money_supply_data_year respond  error_msg:' + rs.error_msg)

        data_list = []
        while (rs.error_code == '0') & rs.next():
            data_list.append(rs.get_row_data())
        result = pd.DataFrame(data_list, columns=rs.fields)

        bs.logout()
        return result

    @staticmethod
    def query_shibor_data(start_date=None, end_date=None):
        """
        银行间同业拆放利率
        方法说明：通过API接口获取银行间同业拆放利率，可以通过参数设置获取对应起止日期的数据。
        返回类型：pandas的DataFrame类型。
        参数含义：
        start_date：开始日期，格式XXXX，发布日期在这个范围内，可以为空；
        end_date：结束日期，格式XXXX，发布日期在这个范围内，可以为空。
        """
        lg = bs.login()
        if lg.error_code != '0':
            logger.error('login respond  error_msg:' + lg.error_msg)

        rs = bs.query_shibor_data(start_date=start_date, end_date=end_date)
        if rs.error_code != '0':
            logger.error('query_shibor_data respond  error_msg:' + rs.error_msg)

        data_list = []
        while (rs.error_code == '0') & rs.next():
            data_list.append(rs.get_row_data())
        result = pd.DataFrame(data_list, columns=rs.fields)

        bs.logout()
        return result

    @staticmethod
    def query_stock_industry(code=None, date=None):
        """
        行业分类
        方法说明：通过API接口获取行业分类信息，更新频率：每周一更新。
        返回类型：pandas的DataFrame类型。
        参数含义：
        code：A股股票代码，sh或sz.+6位数字代码，或者指数代码，如：sh.601398。sh：上海；sz：深圳。可以为空；
        date：查询日期，格式XXXX-XX-XX，为空时默认最新日期。
        """
        lg = bs.login()
        if lg.error_code != '0':
            logger.error('login respond  error_msg:' + lg.error_msg)

        rs = bs.query_stock_industry(code, date)
        if rs.error_code != '0':
            logger.error('query_stock_industry respond  error_msg:' + rs.error_msg)

        industry_list = []
        while (rs.error_code == '0') & rs.next():
            industry_list.append(rs.get_row_data())
        result = pd.DataFrame(industry_list, columns=rs.fields)

        bs.logout()
        return result

    @staticmethod
    def query_sz50_stocks(date=None):
        """
        上证50成分股
        方法说明：通过API接口获取上证50成分股信息，更新频率：每周一更新。
        返回类型：pandas的DataFrame类型。
        参数含义：
        date：查询日期，格式XXXX-XX-XX，为空时默认最新日期。
        """
        lg = bs.login()
        if lg.error_code != '0':
            logger.error('login respond  error_msg:' + lg.error_msg)

        rs = bs.query_sz50_stocks(date)
        if rs.error_code != '0':
            logger.error('query_sz50_stocks respond  error_msg:' + rs.error_msg)

        sz50_stocks = []
        while (rs.error_code == '0') & rs.next():
            sz50_stocks.append(rs.get_row_data())
        result = pd.DataFrame(sz50_stocks, columns=rs.fields)

        bs.logout()
        return result

    @staticmethod
    def query_hs300_stocks(date=None):
        """"
        沪深300成分股
        方法说明：通过API接口获取沪深300成分股信息，更新频率：每周一更新。
        返回类型：pandas的DataFrame类型。
        参数含义：
        date：查询日期，格式XXXX-XX-XX，为空时默认最新日期。
        """
        lg = bs.login()
        if lg.error_code != '0':
            logger.error('login respond  error_msg:' + lg.error_msg)

        rs = bs.query_hs300_stocks(date)
        if rs.error_code != '0':
            logger.error('query_hs300_stocks respond  error_msg:' + rs.error_msg)

        hs300_stocks = []
        while (rs.error_code == '0') & rs.next():
            hs300_stocks.append(rs.get_row_data())
        result = pd.DataFrame(hs300_stocks, columns=rs.fields)

        bs.logout()
        return result

    @staticmethod
    def query_zz500_stocks(date=None):
        """
        中证500成分股
        方法说明：通过API接口获取中证500成分股信息，更新频率：每周一更新。
        返回类型：pandas的DataFrame类型。
        date：查询日期，格式XXXX-XX-XX，为空时默认最新日期。
        """
        lg = bs.login()
        if lg.error_code != '0':
            logger.error('login respond  error_msg:' + lg.error_msg)

        rs = bs.query_zz500_stocks(date)
        if rs.error_code != '0':
            logger.error('query_zz500_stocks respond  error_msg:' + rs.error_msg)

        zz500_stocks = []
        while (rs.error_code == '0') & rs.next():
            zz500_stocks.append(rs.get_row_data())
        result = pd.DataFrame(zz500_stocks, columns=rs.fields)

        bs.logout()
        return result


if __name__ == '__main__':

    config.loads('config.json')
    bao = BaoStockData()
    # print(bao.query_history_k_data_plus("sh000001", "1d", adj='2'))
    print(bao.query_trade_dates())