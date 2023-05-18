import time,logging
from main_platform.celery import ex_cases_app
from AutoTestPlatform.settings import EMAIL_HOST_USER
from django.core.mail import send_mail



logger= logging.getLogger("main_platform")


@ex_cases_app.task
def send_emails(recipient):
    '''
    异步任务，延迟30s发送
    :param recipient:
    :return:
    '''
    time.sleep(30)
    subject= "测试标题"
    message= "测试内容"
    from_email= EMAIL_HOST_USER
    recipient_list= [recipient,]
    send_mail(subject,message,from_email,recipient_list)