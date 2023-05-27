from django.shortcuts import render
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from selenium_apps.models import TestCaseForSEA



def get_paginator(request,data):
    '''每个网页-获取指定页数'''
    paginator= Paginator(data,per_page= 10) # 每页10条
    page= request.GET.get("page")
    try:
        pp= paginator.page(page)
    except:
        pp= paginator.page(1) # 出现所有错误情况，都返回第1页
    return pp


@login_required
def test_case(request):
    '''主页-测试用例'''
    if request.method== "GET":
        # 如果为get请求，直接返回所有用例
        cases= TestCaseForSEA.objects.filter(status= 0).order_by("-create_time") # 根据创建时间倒序
        data= {}
        data["pages"]= get_paginator(request, cases)
        data["case_name"]= ""
        return render(request, "sea/sea_test_case.html", data)

    elif request.method== "POST":
        pass


# @login_required
# def add_test_case(request):
#     '''测试用例-手动创建用例'''
#     if request.method== "GET":
#         data= {}
#         belong_project= Project.objects.all().order_by("id")
#         belong_module= Module.objects.all().order_by("id")
#         user= User.objects.all()
#         data["request_method"]= vp.request_method
#         data["user"]= user
#         data["belong_project"]= belong_project
#         data["belong_module"]= belong_module
#         data["maintainer"]= str(request.user)
#         return render(request, "add_test_case.html",data)
#
#     elif request.method== "POST":
#         ts= TestCase()
#         ts.case_name= request.POST.get("case_name")
#         ts.request_data= request.POST.get("request_data")
#         ts.uri= request.POST.get("uri")
#         ts.maintainer= request.user
#         ts.request_method= request.POST.get("request_method")
#         u= request.POST.get("user")
#         ts.user= User.objects.get(username= u)
#         ts.status= 0
#
#         bp= request.POST.get("belong_project")
#         ts.belong_project= Project.objects.get(name= bp)
#         bm= request.POST.get("belong_module")
#         ts.belong_module= Module.objects.get(name= bm)
#         try:
#             related_case_id= int(request.POST.get("related_case_id"))
#         except:
#             related_case_id= None
#         ts.related_case_id= related_case_id
#         assert_key= request.POST.get("assert_key")
#         if assert_key== '':
#             assert_key= None
#         ts.assert_key= assert_key
#         extract_var= request.POST.get("extract_var")
#         if extract_var== '':
#             extract_var= None
#         ts.extract_var= extract_var
#         ts.save()
#
#         cases= TestCase.objects.filter(status= 0).order_by("-create_time") # 根据创建时间倒序
#         data= {}
#         data["pages"]= get_paginator(request, cases)
#         data["case_name"]= ""
#         return render(request, "test_case.html", data)