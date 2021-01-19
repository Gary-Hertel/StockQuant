from stockquant.config import config
import smtplib
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr


def sendmail(data):
    """
    推送邮件信息。
    :param data: 要推送的信息内容，字符串格式
    :return:
    """
    from_addr = config.SENDMAIL["from"]
    password = config.SENDMAIL["password"]
    to_addr = config.SENDMAIL["to"]
    smtp_server = config.SENDMAIL["server"]
    port = config.SENDMAIL["port"]

    msg = MIMEText(data, 'plain', 'utf-8')
    name, addr = parseaddr('Alert <%s>' % from_addr)
    msg['From'] = formataddr((Header(name, 'utf-8').encode(), addr))
    name, addr = parseaddr('交易者 <%s>' % to_addr)
    msg['To'] = formataddr((Header(name, 'utf-8').encode(), addr))
    msg['Subject'] = Header('交易提醒', 'utf-8').encode()

    server = smtplib.SMTP(smtp_server, port)
    server.login(from_addr, password)
    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()