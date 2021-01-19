# -*- coding:utf-8 -*-

"""
智能渠道推送工具包
Author: Gary-Hertel
Date:   2021/01/19
"""
from stockquant.config import config
import json
import requests
from stockquant.utils.logger import logger


class DingTalk:

    @staticmethod
    def text(text):
        """
        推送文本类型信息至钉钉
        :param data: 要推送的数据内容，字符串格式
        :return:
        """
        json_text = {
            "msgtype": "text",
            "at": {
                "atMobiles": [
                    ""
                ],
                "isAtAll": False
            },
            "text": {
                "content": text
            }
        }

        headers = {'Content-Type': 'application/json;charset=utf-8'}
        api_url = config.dingtalk
        result = requests.post(api_url, json.dumps(json_text), headers=headers)    # 发送钉钉消息并返回发送结果
        logger.debug("dingtalk text result:{} message：{}".format(result, text))
        return result

    @staticmethod
    def markdown(content):
        """
        推送markdown类型信息至钉钉
        :param content:例如：
                            content = "### 订单更新推送\n\n"\
                                           "> **订单ID:** 1096989546123445\n\n"\
                                           "> **订单状态:** FILLED\n\n"\
                                           "> **时间戳:** 2021年1月2日"
        :return:推送结果，例如推送成功时的结果：{"errcode":0,"errmsg":"ok"}
        """
        url = config.dingtalk
        headers = {'Content-Type': 'application/json'}
        body = {
            "msgtype": "markdown",
            "markdown": {
                "title": "交易提醒",
                "text": content
            }
        }
        body = json.dumps(body)
        response = requests.post(url, data=body, headers=headers)
        logger.debug("dingtalk markdown result:", response)
        return response