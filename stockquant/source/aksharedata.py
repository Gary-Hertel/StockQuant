import akshare as ak


class AkShareData:

    @staticmethod
    def stock_sse_summary_df():
        """
        上海证券交易所-股票数据总貌
        限量: 单次返回最近交易日的股票数据总貌数据(当前交易日的数据需要交易所收盘后统计)
        """
        stock_sse_summary_df = ak.stock_sse_summary()
        return stock_sse_summary_df

    @staticmethod
    def stock_szse_summary():
        """
        深圳证券交易所-市场总貌
        限量: 单次返回最近交易日的市场总貌数据(当前交易日的数据需要交易所收盘后统计)
        """
        stock_szse_summary_df = ak.stock_szse_summary(date="20200619")
        return stock_szse_summary_df

    @staticmethod
    def all_stock_tick():
        """
        描述: A 股数据是从新浪财经获取的数据, 重复运行本函数会被新浪暂时封 IP, 建议增加时间间隔
        限量: 单次返回所有 A 股上市公司的实时行情数据
        """
        stock_zh_a_spot_df = ak.stock_zh_a_spot()
        return stock_zh_a_spot_df

    @staticmethod
    def stock_zh_index_spot():
        """
        描述: 股票指数数据是从新浪财经获取的数据
        限量: 单次返回所有指数的实时行情数据
        """
        stock_df = ak.stock_zh_index_spot()
        return stock_df


if __name__ == '__main__':

    aks = AkShareData()
    print(aks.all_stock_tick())