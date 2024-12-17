import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
import configparser
from config import CONFIG_FILE


def send_email_gmail(sender_name, sender_email, receiver_emails, subject, body, app_password):
    try:
        # 创建邮件对象
        message = MIMEMultipart()
        message['From'] = formataddr((sender_name, sender_email))  # 自定义发件人名称
        message["To"] = ', '.join(receiver_emails)
        message["Subject"] = subject

        # 添加正文内容
        message.attach(MIMEText(body, "plain"))

        # 连接 Gmail SMTP 服务器
        smtp_server = "smtp.gmail.com"
        port = 587  # TLS 端口

        server = smtplib.SMTP(smtp_server, port)
        server.starttls()  # 启用 TLS 加密
        server.login(sender_email, app_password)  # 使用应用专用密码登录

        # 发送邮件
        server.sendmail(sender_email, receiver_emails, message.as_string())
        print("邮件发送成功！")
    except Exception as e:
        print("邮件发送失败:", e)
    finally:
        server.quit()


def send_email(subject, body):
    # 邮件参数
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE, encoding="utf-8")
    smtp_config = config['SMTP_GMAIL']
    app_password = smtp_config['app_password']  # 16位应用专用密码
    sender_name = smtp_config['sender_name']  # 自定义发件人名称
    sender_email = smtp_config['sender_email']  # 发件人
    receiver_emails = smtp_config['receiver_emails'].split(',')  # 收件人
    print(sender_name)
    # 发送邮件
    send_email_gmail(sender_name, sender_email, receiver_emails, subject, body, app_password)


if __name__ == "__main__":
    subject = "测试邮件"
    body = "这是一封通过 Gmail SMTP 和应用专用密码发送的测试邮件。"
    send_email(subject, body)
