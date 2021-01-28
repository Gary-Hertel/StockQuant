"""回测模块"""

__all__ = ["BackTest", "backtest_save", "plot_asset"]

import os
import finplot as fplt
from matplotlib import pyplot as plt
from stockquant.utils.tools import *
from stockquant.utils.storage import save_to_csv_file, read_csv_file


class BackTest:
    def __init__(self):
        try:
            os.remove("./回测.csv")
        except:
            pass
        self.kline = None
        self.start_time = 0  # 回测开始时间
        backtest_save(
            "时间",
            "操作",
            "价格",
            "数量",
            "多头数量",
            "多头均价",
            "此次盈亏",
            "总资金"
        )
        backtest_save(
            get_localtime(),
            "开始回测",
            0,
            0,
            0,
            0,
            0,
            0
        )

    def initialize(self, kline, origin_data=None):
        """
        历史k线入口函数
        :param kline: 传入递增的k线
        :param origin_data: 传入原始k线数据计算回测进度
        :return:
        """
        length1 = len(kline)
        if length1 == 1:
            self.start_time = get_cur_timestamp()
            print("{} 开始回测！".format(get_localtime()))
        if origin_data:
            length2 = len(origin_data)
            speed_of_progress = "{}%".format(round(length1 / length2 * 100, 2))
            print("{} 当前回测进度：{}".format(get_localtime(), speed_of_progress))
            if length1 == length2:
                cost = get_cur_timestamp() - self.start_time
                print("回测完成，共计用时{}秒！".format(cost))
        self.kline = kline
        return self.kline

    @property
    def timestamp(self):
        """历史k线上的时间戳"""
        return self.kline[-1][0]

    @property
    def close(self):
        """当根k线收盘价"""
        result = self.kline[-1][4]
        return float(result)

    @property
    def high(self):
        """当前k线最高价"""
        result = self.kline[-1][2]
        return float(result)

    @property
    def low(self):
        """当前k线最低价"""
        result = self.kline[-1][3]
        return float(result)

    @property
    def open(self):
        """当根k线开盘价"""
        result = self.kline[-1][1]
        return float(result)

    @property
    def volume(self):
        """当前k线成交量"""
        result = self.kline[-1][5]
        return float(result)

    def history_high(self, param):
        """历史k线最高价"""
        result = self.kline[-param][2]
        return float(result)

    def history_low(self, param):
        """历史k线最低价"""
        result = self.kline[-param][3]
        return float(result)

    def history_open(self, param):
        """历史k线开盘价"""
        result = self.kline[-param][1]
        return float(result)

    def history_close(self, param):
        """历史k线收盘价"""
        result = self.kline[-param][4]
        return float(result)

    @property
    def long_quantity(self):
        result = read_backtest_info()[4]
        return float(result)

    @property
    def long_avg_price(self):
        result = read_backtest_info()[5]
        return float(result)

    @property
    def short_quantity(self):
        """单向持仓模式下当前持仓均价"""
        result = read_backtest_info()[6]
        return float(result)

    @property
    def short_avg_price(self):
        result = read_backtest_info()[7]
        return float(result)

    def buy(self, price, amount, long_quantity, long_avg_price, profit, asset):
        backtest_save(self.timestamp, "BUY", price, amount, long_quantity, long_avg_price, profit, asset)

    def sell(self, price, amount, long_quantity, long_avg_price, profit, asset):
        backtest_save(self.timestamp, "SELL", price, amount, long_quantity, long_avg_price, profit, asset)


def backtest_save(timestamp, action, price, amount, long_quantity, long_avg_price, profit, asset):
    """保存回测信息至csv文件"""
    try:
        price = float(price)
        amount = float(amount)
        long_quantity = float(long_quantity)
        long_avg_price = float(long_avg_price)
        profit = float(profit)
        asset = float(asset)
    except:
        pass
    data = (timestamp, action, price, amount, long_quantity, long_avg_price, profit, asset)
    save_to_csv_file(data, ".\回测.csv")


def read_backtest_info():
    """读取回测过程中保存至csv文件的持仓信息"""
    data = read_csv_file(".\回测.csv")[-1]
    return data


def read_backtest_asset():
    """读取回测完成后的总资金数据"""
    data = read_csv_file(".\回测.csv")
    data.pop(0)
    data.pop(0)
    time = []
    asset = []
    profit = []
    for i in data:
        result = i
        if float(result[-1]) != 0:
            time.append(result[0])
            asset.append(float(result[-1]))
            if float(result[-2]) > 0:
                profit.append(float(result[-2]))
    rate_of_win = "{}%".format(round(len(profit) / len(data) * 100, 2) * 2)
    information = {"time": time, "asset": asset, "rate_of_win": rate_of_win}
    return information


def plot_asset():
    """回测完成后调用此函数绘制资金曲线图"""
    x = read_backtest_asset()["time"]
    y = read_backtest_asset()["asset"]
    profit = y[-1] - y[0]   # 累计收益
    yields = "{}%".format(round((profit / y[0]) * 100), 2)  # 收益率
    maximum_retreat = "{}%".format(round((min(y) - y[0]) / y[0] * 100, 2))  # 最大回撤
    rate = read_backtest_asset()["rate_of_win"]     # 胜率
    print("累计收益:", profit)
    print("总收益率:", yields)
    print("最大回撤:", maximum_retreat)
    print("系统胜率:", rate)
    plt.rcParams['axes.unicode_minus'] = False
    plt.figure(figsize=(15, 6))
    plt.subplot(facecolor="black")
    plt.plot(x, y, color="c", linestyle="-", linewidth=1.0)
    plt.xlabel("date")
    plt.ylabel("asset")
    plt.title("Asset Picture")
    # plt.xticks(rotation=15)
    plt.xticks(())  # 关闭x轴标签
    figManager = plt.get_current_fig_manager()
    figManager.window.showMaximized()
    os.rename(".\回测.csv", ".\回测 {}.csv".format(get_cur_timestamp()))
    plt.show()


def plot_signal(kline, buy_signal=None, sell_signal=None, *args):
    """回测完成后调用此函数绘制k线图与指标"""
    fplt.foreground = '#FFFFFF'
    fplt.background = '#333333'
    fplt.odd_plot_background = '#333333'
    fplt.cross_hair_color = "#FFFFFF"
    ax, ax2, ax3 = fplt.create_plot('历史K线图', init_zoom_periods=100, maximize=True, rows=3)
    fplt.add_legend("K线主图", ax)
    fplt.add_legend("成交量", ax2)
    fplt.add_legend("指标副图", ax3)

    df = pd.DataFrame(kline)
    df = df[[0, 1, 2, 3, 4, 5]]
    columns = ['time', 'open', 'high', 'low', 'close', 'volume']
    df.columns = columns
    df = df.astype(
        {
            'time': 'datetime64[ns]',
            'open': 'float64',
            'high': 'float64',
            'low': 'float64',
            'close': 'float64',
            'volume': 'float64'
        }
    )
    candlesticks = df['time open close high low'.split()]
    volumes = df['time open close volume'.split()]
    fplt.candlestick_ochl(candlesticks)
    fplt.volume_ocv(volumes, ax=ax2)

    if args:
        count = 1
        for i in args:
            indicators = pd.Series(i)
            fplt.plot(df['time'], indicators, legend="指标{}".format(count), ax=ax3)
            count += 1
    if buy_signal:
        for i in buy_signal:
            df.loc[df['high'] == buy_signal[buy_signal.index(i)], "buy_signal"] = df['high']
        fplt.plot(df['time'], df['buy_signal'], ax=ax, color="#FF0000", style='^', width=2, legend='买入信号')
    if sell_signal:
        for i in sell_signal:
            df.loc[df['low'] == sell_signal[sell_signal.index(i)], "sell_signal"] = df['low']
        fplt.plot(df['time'], df['sell_signal'], ax=ax, color="#00FF00", style='v', width=2, legend='卖出信号')
    fplt.show()
