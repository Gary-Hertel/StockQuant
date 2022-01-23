import easytrader
from stockquant.config import config
from stockquant.utils.tools import sleep
from stockquant.utils.logger import logger
from stockquant.utils.dingtalk import DingTalk
from easytrader.utils.stock import get_today_ipo_data
from easytrader import grid_strategies


class Trade:
    """ Trade Client

    Attributes:
        config_file: config_file.
        symbol: stock_code.
        path: tong hua shun xia_dan.exe file path.
        delay: start after several seconds.
    """

    def __init__(self, config_file, symbol=None, path=None, delay=None):
        """initialize Trade API client."""
        try:
            sleep(delay or 1)
            if symbol:
                self.code = str(symbol).replace("sh", "") if str(symbol).startswith("sh") else str(symbol).replace("sz", "")
            else:
                self.code = ""
            config.loads(config_file)
            self.user = easytrader.use('ths')
            if path:
                self.user.connect(path)
            else:
                self.user.connect(r'C:\东方同花顺独立下单\xiadan.exe')
            logger.info("initialize trade client success !")
        except Exception as e:
            logger.error("initialize trade client failed ! error message: {}".format(e))

    def buy(self, price, amount):
        """ Create an buy order.
        Args:
            price: Price of each stock.
            amount: The buying quantity.

        Returns:
            success: Success results, otherwise it's None.
            error: Error information, otherwise it's None.
        """
        try:
            result = self.user.buy(security=self.code, price=price, amount=amount)
            return result, None
        except Exception as e:
            return None, e

    def sell(self, price, amount):
        """ Create an sell order.
        Args:
            price: Price of each stock.
            amount: The selling quantity.

        Returns:
            success: Success results, otherwise it's None.
            error: Error information, otherwise it's None.
        """
        try:
            result = self.user.sell(self.code, price=price, amount=amount)
            return result, None
        except Exception as e:
            return None, e

    def revoke_order(self, order_id):
        """ revoke an order.

        Args:
            order_id: order_id.

        Returns:
            success: Success results, otherwise it's None.
            error: Error information, otherwise it's None.
        """
        try:
            self.user.grid_strategy = grid_strategies.Xls
            result = self.user.cancel_entrust('buy/sell {order_id}'.format(order_id=order_id))
            if result["message"] != '撤单申报成功':
                return None, result
            return result, None
        except Exception as e:
            return None, e

    def get_today_orders(self):
        """ Get Today orders.

        Returns:
            success: Success results, otherwise it's None.
            error: Error information, otherwise it's None.
        """
        try:
            self.user.grid_strategy = grid_strategies.Xls
            result = self.user.today_entrusts
            return result, None
        except Exception as e:
            return None, e

    def get_today_deals(self):
        """ Get Today deals.

        Returns:
            success: Success results, otherwise it's None.
            error: Error information, otherwise it's None.
        """
        try:
            self.user.grid_strategy = grid_strategies.Xls
            result = self.user.today_trades
            return result, None
        except Exception as e:
            return None, e

    def get_positions(self):
        """ Get Positions.

        Returns:
            success: Success results, otherwise it's None.
            error: Error information, otherwise it's None.
        """
        try:
            self.user.grid_strategy = grid_strategies.Xls
            result = self.user.position
            return result, None
        except Exception as e:
            return None, e

    def get_balance(self):
        """ Get Balance.

        Returns:
            success: Success results, otherwise it's None.
            error: Error information, otherwise it's None.
        """
        try:
            result = self.user.balance
            return result, None
        except Exception as e:
            return None, e

    def auto_ipo(self):
        """ Auto IPO.

        Returns:
            success: Success results, otherwise it's None.
            error: Error information, otherwise it's None.
        """
        try:
            result = self.user.auto_ipo()
            return result, None
        except Exception as e:
            return None, e

    @staticmethod
    def get_today_ipo_data():
        """ Get_today_ipo_data.

        Returns:
            success: Success results, otherwise it's None.
            error: Error information, otherwise it's None.
        """
        try:
            result = get_today_ipo_data()
            return result, None
        except Exception as e:
            return None, e


if __name__ == '__main__':

    t = Trade(config_file="config.json", symbol="sh600519", path=None, delay=5)
    # success, error = t.buy(2000, 100)
    # success, error = t.sell(2000, 100)
    success, error = t.get_balance()
    logger.info("success:", success)
    logger.info("error:", error)
    if error:
        DingTalk.text("交易程序运行错误提醒：{error}".format(error=error))