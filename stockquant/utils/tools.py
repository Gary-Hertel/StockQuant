# -*- coding:utf-8 -*-

"""
工具包
"""

import time
import decimal
import datetime
import pandas as pd


def sleep(seconds):
    time.sleep(seconds)


def get_cur_timestamp():
    """ 获取当前时间戳（秒）
    """
    ts = int(time.time())
    return ts


def ts_to_utc_str(ts=None, fmt='%Y-%m-%dT%H:%M:%S.000z'):
    """ 将时间戳转换为UTC时间格式，'2020-07-25T03:05:00.000z'
    @param ts 时间戳，默认None即为当前时间戳
    @param fmt 返回的UTC字符串格式
    """
    if not ts:
        ts = get_cur_timestamp()
    dt = datetime.datetime.utcfromtimestamp(int(ts))
    return dt.strftime(fmt)


def get_cur_timestamp_ms():
    """ 获取当前时间戳(毫秒)
    """
    ts = int(time.time() * 1000)
    return ts


def get_cur_datetime_m(fmt='%Y%m%d%H%M%S%f'):
    """ 获取当前日期时间字符串，包含 年 + 月 + 日 + 时 + 分 + 秒 + 微妙
    """
    today = datetime.datetime.today()
    str_m = today.strftime(fmt)
    return str_m


def get_datetime(fmt='%Y%m%d%H%M%S'):
    """ 获取日期时间字符串，包含 年 + 月 + 日 + 时 + 分 + 秒
    """
    today = datetime.datetime.today()
    str_dt = today.strftime(fmt)
    return str_dt


def get_date(fmt='%Y%m%d', delta_day=0):
    """ 获取日期字符串，包含 年 + 月 + 日
    @param fmt 返回的日期格式
    """
    day = datetime.datetime.today()
    if delta_day:
        day += datetime.timedelta(days=delta_day)
    str_d = day.strftime(fmt)
    return str_d


def date_str_to_dt(date_str=None, fmt='%Y%m%d', delta_day=0):
    """ 日期字符串转换到datetime对象
    @param date_str 日期字符串
    @param fmt 日期字符串格式
    @param delta_day 相对天数，<0减相对天数，>0加相对天数
    """
    if not date_str:
        dt = datetime.datetime.today()
    else:
        dt = datetime.datetime.strptime(date_str, fmt)
    if delta_day:
        dt += datetime.timedelta(days=delta_day)
    return dt


def dt_to_date_str(dt=None, fmt='%Y%m%d', delta_day=0):
    """ datetime对象转换到日期字符串
    @param dt datetime对象
    @param fmt 返回的日期字符串格式
    @param delta_day 相对天数，<0减相对天数，>0加相对天数
    """
    if not dt:
        dt = datetime.datetime.today()
    if delta_day:
        dt += datetime.timedelta(days=delta_day)
    str_d = dt.strftime(fmt)
    return str_d


def get_utc_time():
    """ 获取当前utc时间
    """
    utc_t = datetime.datetime.utcnow()
    return utc_t


def get_localtime():
    """ 获取本地时间"""
    localtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    return localtime


def ts_to_datetime_str(ts=None, fmt='%Y-%m-%d %H:%M:%S'):
    """ 将时间戳转换为日期时间格式，年-月-日 时:分:秒
    @param ts 时间戳，默认None即为当前时间戳
    @param fmt 返回的日期字符串格式
    """
    if not ts:
        ts = get_cur_timestamp()
    dt = datetime.datetime.fromtimestamp(int(ts))
    return dt.strftime(fmt)


def datetime_str_to_ts(dt_str, fmt='%Y-%m-%d %H:%M:%S'):
    """ 将日期时间格式字符串转换成时间戳
    @param dt_str 日期时间字符串
    @param fmt 日期时间字符串格式
    """
    ts = int(time.mktime(datetime.datetime.strptime(dt_str, fmt).timetuple()))
    return ts


def datetime_to_timestamp(dt=None, tzinfo=None):
    """ 将datetime对象转换成时间戳
    @param dt datetime对象，如果为None，默认使用当前UTC时间
    @param tzinfo 时区对象，如果为None，默认使用timezone.utc
    @return ts 时间戳(秒)
    """
    if not dt:
        dt = get_utc_time()
    if not tzinfo:
        tzinfo = datetime.timezone.utc
    ts = int(dt.replace(tzinfo=tzinfo).timestamp())
    return ts


def utctime_str_to_ts(utctime_str, fmt="%Y-%m-%dT%H:%M:%S.%fZ"):
    """ 将UTC日期时间格式字符串转换成时间戳
    @param utctime_str 日期时间字符串 eg: 2019-03-04T09:14:27.806Z
    @param fmt 日期时间字符串格式
    @return timestamp 时间戳(秒)
    """
    dt = datetime.datetime.strptime(utctime_str, fmt)
    timestamp = int(dt.replace(tzinfo=datetime.timezone.utc).astimezone(tz=None).timestamp())
    return timestamp


def utctime_str_to_mts(utctime_str, fmt="%Y-%m-%dT%H:%M:%S.%fZ"):
    """ 将UTC日期时间格式字符串转换成时间戳（毫秒）
    @param utctime_str 日期时间字符串 eg: 2019-03-04T09:14:27.806Z
    @param fmt 日期时间字符串格式
    @return timestamp 时间戳(毫秒)
    """
    dt = datetime.datetime.strptime(utctime_str, fmt)
    timestamp = int(dt.replace(tzinfo=datetime.timezone.utc).astimezone(tz=None).timestamp() * 1000)
    return timestamp


def float_to_str(f, p=20):
    """ 将给定的float转换为字符串，而无需借助科学计数法。
    @param f 浮点数参数
    @param p 精读
    """
    if type(f) == str:
        f = float(f)
    ctx = decimal.Context(p)
    d1 = ctx.create_decimal(repr(f))
    return format(d1, 'f')


def now():
    """获取当前的小时和分钟信息，返回字符串，例如："02:47"，可以用来在每日早上去查询一下今日是否开盘"""
    localtime = get_localtime()
    result = localtime.split(" ")[1]
    t = result[0: 5]
    return t


def not_open_time():
    """获取小时和分钟时间，返回例如“200”，表示当前为02：00，为了在非交易时间进行过滤"""
    t = now()
    result = int(t.replace(":", ""))
    if result < 900 or result > 1500:
        return True
    else:
        return False


def combine_kline(csv_file_path, interval):
    """
    将自定义csv数据源的1分钟k线数据合成为任意周期的 k线数据，返回列表类型的k线数据，并自动保存新合成的k线数据至csv文件
    :param csv_file_path: 文件路径
    :param interval: 要合成的k线周期，例如3分钟就传入3，1小时就传入60，一天就传入1440
    :return: 返回列表类型的新合成的k线数据
    """
    df = pd.read_csv(csv_file_path)  # 读取传入的原1分钟k线数据
    df = df.set_index(pd.DatetimeIndex(pd.to_datetime(df['timestamp'], format='%Y-%m-%dT%H:%M:%S.000z', infer_datetime_format=True)))   # 设置索引
    open = df['open'].resample("%dmin"%interval, label="left", closed="left").first()    # 将open一列合成，取第一个价格
    high = df['high'].resample("%dmin"%interval, label="left", closed="left").max()  # 合并high一列，取最大值，即最高价
    low = df["low"].resample("%dmin"%interval, label="left", closed="left").min()    # 合并low一列，取最小值，即最低价
    close = df["close"].resample("%dmin"%interval, label="left", closed="left").last()   # 合并close一列，取最后一个价格
    volume = df["volume"].resample("%dmin"%interval, label="left", closed="left").sum()  # 合并volume一列，取和
    try:
        currency_volume = df["currency_volume"].resample("%dmin" % interval, label="left", closed="left").sum()  # 尝试合并currency_volume一列，如果失败则说明数据并不包含此列
        kline = pd.DataFrame(
            {"open": open, "high": high, "low": low, "close": close, "volume": volume, "currency_volume": currency_volume})
    except:
        kline = pd.DataFrame({"open": open, "high": high, "low": low, "close": close, "volume": volume})
    kline.to_csv("{}min_{}".format(interval, csv_file_path))    # 保存新数据至csv文件
    records = pd.read_csv("{}min_{}".format(interval, csv_file_path)) # 读取新文件，因为旧数据经处理后并不包含时间戳
    data = records.values.tolist()  # 将新读取的数据转换为列表数据类型
    return data