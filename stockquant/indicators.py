import numpy as np
import talib


def ATR(length, kline):
    """
    指数移动平均线
    :param length: 长度参数，如14获取的是14周期上的ATR值
    :param kline:传入指定k线数据
    :return:返回一个一维数组
    """
    records = kline
    kline_length = len(records)     # 计算k线数据的长度
    high_array = np.zeros(kline_length)     # 创建为零的数组
    low_array = np.zeros(kline_length)
    close_array = np.zeros(kline_length)
    t = 0
    for item in records:
        high_array[t] = item[2]
        low_array[t] = item[3]
        close_array[t] = item[4]
        t += 1
    result = talib.ATR(high_array, low_array, close_array, timeperiod=length)
    return result


def BOLL(length, kline):
    """
    布林指标
    :param length:长度参数
    :param kline:传入指定k线数据
    :return: 返回一个字典 {"upperband": 上轨数组， "middleband": 中轨数组， "lowerband": 下轨数组}
    """
    records = kline
    kline_length = len(records)
    close_array = np.zeros(kline_length)
    t = 0
    for item in records:
        close_array[t] = item[4]
        t += 1
    result = (talib.BBANDS(close_array, timeperiod=length, nbdevup=2, nbdevdn=2, matype=0))
    upperband = result[0]
    middleband = result[1]
    lowerband = result[2]
    dict = {"upperband": upperband, "middleband": middleband, "lowerband": lowerband}
    return dict


def CCI(length, kline):
    """
    顺势指标
    :param length:长度参数
    :param kline:传入指定k线数据
    :return:
    """
    high_list, low_list, close_list = [], [], []
    for i in kline:
        high_list.append(float(i[2]))
        low_list.append(float(i[3]))
        close_list.append(float(i[4]))
    high_arr = np.array(high_list)
    low_arr = np.array(low_list)
    close_arr = np.array(close_list)
    cci = talib.CCI(high_arr, low_arr, close_arr, timeperiod=length)
    return cci


def CurrentBar(kline):
    """
    获取k线数据的长度
    :param kline: 传入指定k线数据
    :return: 返回一个整型数字
    """
    records = kline
    kline_length = len(records)
    return kline_length


def HIGHEST(length, kline):
    """
    周期最高价
    :param length: 长度参数
    :param kline: 传入指定k线数据
    :return:返回一个一维数组
    """
    records = kline
    kline_length = len(records)
    high_array = np.zeros(kline_length)
    t = 0
    for item in records:
        high_array[t] = item[2]
        t += 1
    result = (talib.MAX(high_array, length))
    return result


def MA(length, kline):
    """
    移动平均线(简单移动平均)
    :param length:长度参数，如20获取的是20周期的移动平均
    :param kline:传入指定k线数据
    :return:返回一个一维数组
    """
    records = kline
    kline_length = len(records)
    close_array = np.zeros(kline_length)
    t = 0
    for item in records:
        close_array[t] = item[4]
        t += 1
    result = talib.SMA(close_array, length)
    return result


def MACD(fastperiod, slowperiod, signalperiod, kline):
    """
    计算MACD
    :param fastperiod: 参数1
    :param slowperiod: 参数2
    :param signalperiod: 参数3
    :param kline: 传入指定k线数据
    :return: 返回一个字典 {'DIF': DIF数组, 'DEA': DEA数组, 'MACD': MACD数组}
    """
    records = kline
    kline_length = len(records)
    close_array = np.zeros(kline_length)
    t = 0
    for item in records:
        close_array[t] = item[4]
        t += 1
    result = (talib.MACD(close_array, fastperiod=fastperiod, slowperiod=slowperiod, signalperiod=signalperiod))
    DIF = result[0]
    DEA = result[1]
    MACD = result[2] * 2
    dict = {'DIF': DIF, 'DEA': DEA, 'MACD': MACD}
    return dict


def EMA(length, kline):
    """
    指数移动平均线
    :param length: 长度参数
    :param kline: 传入指定k线数据
    :return: 返回一个一维数组
    """
    records = kline
    kline_length = len(records)
    close_array = np.zeros(kline_length)
    t = 0
    for item in records:
        close_array[t] = item[4]
        t += 1
    result = talib.EMA(close_array, length)
    return result


def KAMA(length, kline):
    """
    适应性移动平均线
    :param length: 长度参数
    :param kline: 传入指定k线数据
    :return: 返回一个一维数组
    """
    records = kline
    kline_length = len(records)
    close_array = np.zeros(kline_length)
    t = 0
    for item in records:
        close_array[t] = item[4]
        t += 1
    result = talib.KAMA(close_array, length)
    return result


def KDJ(fastk_period, slowk_period, slowd_period, kline):
    """
    计算k值和d值
    :param fastk_period: 参数1
    :param slowk_period: 参数2
    :param slowd_period: 参数3
    :param kline: 传入指定k线数据
    :return: 返回一个字典，{'k': k值数组， 'd': d值数组}
    """
    records = kline
    kline_length = len(records)
    high_array = np.zeros(kline_length)
    low_array = np.zeros(kline_length)
    close_array = np.zeros(kline_length)
    t = 0
    for item in records:
        high_array[t] = item[2]
        low_array[t] = item[3]
        close_array[t] = item[4]
        t += 1
    result = (talib.STOCH(high_array, low_array, close_array, fastk_period=fastk_period,
                                                            slowk_period=slowk_period,
                                                            slowk_matype=0,
                                                            slowd_period=slowd_period,
                                                            slowd_matype=0))
    slowk = result[0]
    slowd = result[1]
    dict = {'k': slowk, 'd': slowd}
    return dict


def LOWEST(length, kline):
    """
    周期最低价
    :param length: 长度参数
    :param kline: 传入指定k线数据
    :return: 返回一个一维数组
    """
    records = kline
    kline_length = len(records)
    low_array = np.zeros(kline_length)
    t = 0
    for item in records:
        low_array[t] = item[3]
        t += 1
    result = (talib.MIN(low_array, length))
    return result


def OBV(kline):
    """
    OBV
    :param kline: 传入指定k线数据
    :return: 返回一个一维数组
    """
    records = kline
    kline_length = len(records)
    close_array = np.zeros(kline_length)
    t = 0
    for item in records:
        close_array[t] = item[4]
        t += 1
    result = (talib.OBV(close_array, VOLUME(kline)))
    return result


def RSI(length, kline):
    """
    RSI
    :param length: 长度参数
    :param kline: 传入指定k线数据
    :return:返回一个一维数组
    """
    records = kline
    kline_length = len(records)
    close_array = np.zeros(kline_length)
    t = 0
    for item in records:
        close_array[t] = item[4]
        t += 1
    result = (talib.RSI(close_array, timeperiod=length))
    return result


def ROC(length, kline):
    """
    变动率指标
    :param length:长度参数
    :param kline:传入指定k线数据
    :return:返回一个一维数组
    """
    records = kline
    kline_length = len(records)
    close_array = np.zeros(kline_length)
    t = 0
    for item in records:
        close_array[t] = item[4]
        t += 1
    result = (talib.ROC(close_array, timeperiod=length))
    return result


def STOCHRSI(timeperiod, fastk_period, fastd_period, kline):
    """
    计算STOCHRSI
    :param timeperiod: 参数1
    :param fastk_period:参数2
    :param fastd_period:参数3
    :param kline:传入指定k线数据
    :return: 返回一个字典  {'STOCHRSI': STOCHRSI数组, 'fastk': fastk数组}
    """
    records = kline
    kline_length = len(records)
    close_array = np.zeros(kline_length)
    t = 0
    for item in records:
        close_array[t] = item[4]
        t += 1
    result = (talib.STOCHRSI(close_array, timeperiod=timeperiod, fastk_period=fastk_period, fastd_period=fastd_period, fastd_matype=0))
    STOCHRSI = result[1]
    fastk = talib.MA(STOCHRSI, 3)
    dict = {'stochrsi': STOCHRSI, 'fastk': fastk}
    return dict


def SAR(kline):
    """
    抛物线指标
    :param kline:传入指定k线数据
    :return:返回一个一维数组
    """
    records = kline
    kline_length = len(records)
    high_array = np.zeros(kline_length)
    low_array = np.zeros(kline_length)
    t = 0
    for item in records:
        high_array[t] = item[2]
        low_array[t] = item[3]
        t += 1
    result = (talib.SAR(high_array, low_array, acceleration=0.02, maximum=0.2))
    return result


def STDDEV(length, kline, nbdev=None):
    """
    求标准差
    :param length:周期参数
    :param nbdev:求估计方差的类型，1 – 求总体方差，2 – 求样本方差
    :param kline:传入指定k线数据
    :return:返回一个一维数组
    """
    nbdev= 1 or nbdev
    records = kline
    kline_length = len(records)
    close_array = np.zeros(kline_length)
    t = 0
    for item in records:
        close_array[t] = item[4]
        t += 1
    result = (talib.STDDEV(close_array, timeperiod=length, nbdev=nbdev))
    return result


def TRIX(length, kline):
    """
    三重指数平滑平均线
    :param length:长度参数
    :param kline:传入指定k线数据
    :return:返回一个一维数组
    """
    records = kline
    kline_length = len(records)
    close_array = np.zeros(kline_length)
    t = 0
    for item in records:
        close_array[t] = item[4]
        t += 1
    result = (talib.TRIX(close_array, timeperiod=length))
    return result


def VOLUME(kline):
    """
    成交量
    :param kline: 传入指定k线数据
    :return: 返回一个一维数组
    """
    records = kline
    length = len(records)
    t = 0
    volume_array = np.zeros(length)
    for item in records:
        volume_array[t] = item[5]
        t += 1
    return volume_array