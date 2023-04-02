from celery import Celery
from flask import current_app as curr_app
from jinja2 import Template

celery = Celery("Application Workers")

class ContextTask(celery.Task):
    def __call__(self, *args, **kwargs):
        with curr_app.app_context():
            return self.run(*args, **kwargs)

import mimetypes
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

SMPTP_SERVER_HOST = "localhost"
SMPTP_SERVER_PORT = "1025"
SENDER_ADDRESS = "aakarshitdhuria@gmail.com"
SENDER_PASSWORD = "aakarshit"


def sendEmail(toAddress, subject, tripTime, tripPrice, content="text"):
    msg = MIMEMultipart()
    msg["From"] = SENDER_ADDRESS
    msg["To"] = toAddress
    msg["Subject"] = subject

    attachment = './templates/Cab Booking.html'
    with open(attachment) as f:
        template = Template(f.read())
        message = template.render(tripTime=tripTime,tripPrice=tripPrice)

    msg.attach(MIMEText(message, "html"))

    s = smtplib.SMTP(host=SMPTP_SERVER_HOST, port=SMPTP_SERVER_PORT)
    s.login(SENDER_ADDRESS, SENDER_PASSWORD)
    s.send_message(msg)
    s.quit()

    return "Mail Sent"
