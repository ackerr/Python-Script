import os
import smtplib

from email.mime.text import MIMEText
from email.utils import formataddr
from typing import List

from celery import Celery

app = Celery(
    "main", backend="redis://localhost:6379/0", broker="redis://localhost:6379"
)

SMTP_HOST = os.environ.get("SMTP_HOST", "smtp.qq.com")
SMTP_PORT = os.environ.get("SMTP_PORT", 465)
SMTP_USER = os.environ.get("SMTP_USER")
# https://service.mail.qq.com/cgi-bin/help?subtype=1&&id=28&&no=331
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD")  # 邮箱授权码


class Email:

    client = None

    def __init__(self):
        if not self.client:
            self.client = smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT)
            self.client.login(SMTP_USER, SMTP_PASSWORD)

    def send(self, message: str, to_addrs: List[str]):
        try:
            self.client.sendmail(SMTP_USER, to_addrs, message)
        except smtplib.SMTPException:
            print("发送失败")
        return True

    @staticmethod
    def generate_message(subject: str, message: str, to_addrs: List[str]) -> MIMEText:
        """
        生成发送内容对象
        :param subject: 邮件标题
        :param message: 邮件内容
        :param to_addrs: 接受者
        :return: 内容对象
        """
        info = MIMEText(message, "plain", "utf8")
        info["Subject"] = subject
        info["From"] = formataddr(["FROM", SMTP_USER])
        info["To"] = formataddr(["TO", ",".join(to_addrs)])
        return info


@app.task
def async_send_email(subject: str, message: str, to_addrs: List[str]):
    info = Email.generate_message(subject, message, to_addrs)
    Email().send(info.as_string(), to_addrs)


if __name__ == "__main__":
    title = "this is email title"
    msg = "this is email message"
    receivers = ["xxx@xx.com"]

    async_send_email.delay(title, msg, receivers)
