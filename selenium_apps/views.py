from django.http import JsonResponse
from django.shortcuts import render
from django.core.paginator import Paginator
from selenium_apps.models import TestCaseForSEA,TestCaseSteps
from django.contrib.auth.decorators import login_required



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
    '''主页-测试用例列表'''
    if request.method== "GET":
        # 如果为get请求，直接返回所有用例
        cases= TestCaseForSEA.objects.filter(status= 0).order_by("-create_time") # 根据创建时间倒序
        data= {}
        data["pages"]= get_paginator(request, cases)
        return render(request, "sea/sea_test_case.html", data)

    elif request.method== "POST":
        # 查询时候在写
        pass


@login_required
def test_case_detail(request,caseid):
    '''测试用例-修改用例'''
    if request.method== "GET":
        detail= TestCaseForSEA.objects.get(id= caseid)
        steps= TestCaseSteps.objects.filter(testcaseid_id= detail.id)\
            .values_list("LocationPath","Method","Parameter","Action","Expected")
        # values_list可以将queryset转换成tuple，需要指定字段

        detail_steps= [] # 处理数据加上下标
        for i,line in enumerate([list(i) for i in steps]):
            inner_steps= []
            inner_steps.append(str(i+1))
            for j in line:
                inner_steps.append(j)
            detail_steps.append(inner_steps)

        data= {
            "test_case":detail,
            "test_case_steps":detail_steps
        }

        return render(request, "sea/sea_test_case_detail.html", data)
    else:
        pass


@login_required
def add_test_case(request):
    '''测试用例-新增用例页面'''
    if request.method== "GET":
        # 提交表单时获取不到数据，所以通过接口add_test_case_interface来新增
        return render(request, "sea/sea_add_test_case.html",{})


@login_required
def add_test_case_interface(request):
    '''测试用例-新增用例接口'''
    data= {
        "status": 2000,
        "msg": "test",
    }
    try:
        steps= request.GET.get("steps").replace("[[","").replace("]]","")
        case_name= request.GET.get("case_name")
        steps_list= []
        for step in steps.split("],["):
            inner_list= []
            for s in step.split(","):
                s= s.replace('"','')
                if s== "/" or "": # 处理前端为空时显示
                    s= None
                inner_list.append(s)
            steps_list.append(inner_list)

        tcfs= TestCaseForSEA() # 创建用例
        tcfs.case_name= case_name
        tcfs.status= 0
        tcfs.user= request.user
        tcfs.save()

        for sl in steps_list:
            tcs= TestCaseSteps() # 创建关联步骤
            tcs.testcaseid= tcfs
            tcs.LocationPath= sl[0]
            tcs.Method= sl[1]
            tcs.Parameter= sl[2]
            tcs.Action= sl[3]
            tcs.Expected= sl[4]
            tcs.save()

        data["status"]= 2000
        data["msg"]= "提交用例创建成功"
    except Exception as e:
        TestCaseForSEA.objects.filter(user= request.user).last().delete()
        # 如果创建错误，将当前用户最后一条删除
        data["status"]= 2001
        data["msg"]= "提交用例创建失败，请检查"
    return JsonResponse(data)


@login_required
def update_test_case(request,caseid):
    '''测试用例-修改用例'''
    if request.method== "GET":
        detail= TestCaseForSEA.objects.get(id= caseid)
        steps= TestCaseSteps.objects.filter(testcaseid_id= detail.id)\
            .values_list("LocationPath","Method","Parameter","Action","Expected")
        # values_list可以将queryset转换成tuple，需要指定字段

        detail_steps= [] # 处理数据加上下标
        for i,line in enumerate([list(i) for i in steps]):
            inner_steps= []
            inner_steps.append(str(i+1))
            for j in line:
                inner_steps.append(j)
            detail_steps.append(inner_steps)

        data= {
            "test_case":detail,
            "test_case_steps":detail_steps
        }

        return render(request, "sea/sea_update_test_case.html", data)
    else:
        pass


@login_required
def update_test_case_interface(request):
    '''测试用例-修改用例接口'''
    data= {
        "status": 2000,
        "msg": "test",
    }

    try:
        case_id= request.GET.get("case_id")
        steps= request.GET.get("steps").replace("[[", "").replace("]]", "")
        detail= TestCaseForSEA.objects.get(id= case_id)
        TestCaseSteps.objects.filter(testcaseid_id= detail.id).delete()
        # 物理删除级联步骤，防止数据表过大

        steps_list= []
        for step in steps.split("],["):
            inner_list= []
            for s in step.split(","):
                s= s.replace('"', '')
                if s== "/" or "":  # 处理前端为空时显示
                    s= None
                inner_list.append(s)
            steps_list.append(inner_list)

        for sl in steps_list:
            tcs= TestCaseSteps()  # 创建关联步骤
            tcs.testcaseid= detail
            tcs.LocationPath= sl[0]
            tcs.Method= sl[1]
            tcs.Parameter= sl[2]
            tcs.Action= sl[3]
            tcs.Expected= sl[4]
            tcs.save()

        data["status"]= 2000
        data["msg"]= "提交用例创建成功"
    except:
        data["status"]= 2001
        data["msg"]= "修改用例失败，请检查"
    return JsonResponse(data)


@login_required
def delete_test_case(request,caseid):
    '''测试用例-删除用例'''
    case= TestCaseForSEA.objects.get(id= caseid)
    case.status= 1
    case.save()

    cases= TestCaseForSEA.objects.filter(status=0).order_by("-create_time")  # 根据创建时间倒序
    data= {}
    data["pages"]= get_paginator(request, cases)
    return render(request, "sea/sea_test_case.html", data)



1.新增用例的详情，可以管理项目和模块