from celery.result import AsyncResult
from django.http import HttpResponse
from SendMail.tasks import send_emails
from main_platform import celery_app



def email(request):
    '''
    发送邮件
    :param request:
    :return:
    '''
    mail_address= request.GET.get("address")
    send_result= send_emails.delay(mail_address)
    return HttpResponse(send_result)


def get_result(request):
    '''
    根据id查询查询结果
    :param nid:
    :return:
    '''
    nid= request.GET.get("nid")
    print(nid)

    r= AsyncResult(nid,app= celery_app)
    return HttpResponse(r.status)