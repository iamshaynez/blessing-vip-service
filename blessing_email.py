import os
import ssl
from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
from ConfigCenter import R2Config
load_dotenv()

config = R2Config()
aws_ses_json = config.read_json('aws_ses_blessing.json')
AWS_SMTP_SERVER = aws_ses_json['AWS_SMTP_SERVER']
AWS_SMTP_PORT = aws_ses_json['AWS_SMTP_PORT']
AWS_SMTP_USER = aws_ses_json['AWS_SMTP_USER']
AWS_SMTP_PASSWORD = aws_ses_json['AWS_SMTP_PASSWORD']

def send_email_with_ses(from_email, to_email, message) :

    # getting the credentials fron evironemnt
    host = AWS_SMTP_SERVER
    user = AWS_SMTP_USER
    password = AWS_SMTP_PASSWORD

    # setting up ssl context
    context = ssl.create_default_context()

    # creating an unsecure smtp connection
    with SMTP(host,AWS_SMTP_PORT) as server :

        # securing using tls
        server.starttls(context=context)

        # authenticating with the server to prove our identity
        server.login(user=user, password=password)

        # sending a plain text email
        server.sendmail(from_email, to_email, message.as_string())


def get_email(subject, from_email, to_email):
    with open('blessing_output.html', 'r') as f:
        HTML_BODY = f.read()
    # 创建邮件对象
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email  # 收件人邮箱

    # 设置 HTML 正文
    html_part = MIMEText(HTML_BODY, 'html', 'utf-8')
    msg.attach(html_part)
    return msg

if __name__ == "__main__" :
    from_email = "support@blessing.vip"
    to_email = "xiaowen.z@outlook.com"
    subject = "Blessing For You"

    message = get_email(subject, from_email, to_email)
    send_email_with_ses(from_email, to_email, message)