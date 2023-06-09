import datetime
from django.http import JsonResponse
from django.shortcuts import render
from django.core.paginator import Paginator
from selenium_apps.models import TestCaseForSEA,TestCaseSteps
from main_platform.views import get_server_address
from main_platform.models import JobExecuted
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from selenium_apps.tasks import case_task



def get_paginator(request,data):
    '''每个网页-获取指定页数'''
    paginator= Paginator(data,per_page= 10) # 每页10条
    page= request.GET.get("page")
    try:
        pp= paginator.page(page)
    except:
        pp= paginator.page(1) # 出现所有错误情况，都返回第1页
    return pp


@csrf_exempt
def get_job_name(request):
    '''获取任务名称，判断是否重复'''
    ex_time= request.GET.get("ex_time")
    type= request.GET.get("type")
    if ex_time== "":
        ex_time= (datetime.datetime.now() + datetime.timedelta(minutes= 1)).strftime("%Y-%m-%dT%H:%M")
    job_name= "test_UI_job%s_%s"%(str(type),ex_time)
    try:
        jbe= JobExecuted.objects.get(job_id= job_name)
        return JsonResponse({"msg":"存在相同任务名%s"%jbe,"status":2001})
    except:
        return JsonResponse({"msg": "不存在相同任务名", "status": 2000})


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
        case_name= request.POST.get("case_name")
        ex_case= request.POST.get("ex_case") # 判断是否执行用例的关键字
        ex_time= request.POST.get("ex_time") # 判断执行时间的关键字

        if ex_time in ("",None):
            ex_time= (datetime.datetime.now()+datetime.timedelta(minutes=1)).strftime("%Y-%m-%dT%H:%M")
        year= ex_time[:4]
        month= ex_time[5:7]
        day= ex_time[8:10]
        hour= ex_time[11:13]
        minute= ex_time[14:]
        data= {}

        if not ex_case:
            # 如果不是进行执行操作
            if case_name in [None, ""]:
                case_name= ""
                cases= TestCaseForSEA.objects.filter(status= 0).order_by("-create_time")
            else:
                cases= TestCaseForSEA.objects.filter(case_name__contains= case_name,status= 0).order_by("-create_time")
            data["pages"]= get_paginator(request, cases)
            data["case_name"]= case_name
            return render(request, "sea/sea_test_case.html", data)

        else:
            env= request.POST.get("env")
            test_case_list= request.POST.getlist("testcases_list")

            if len(test_case_list)== 0:
                # 解决传空用例的问题
                cases= TestCaseForSEA.objects.filter(status=0).order_by("-create_time")  # 根据创建时间倒序
                data= {}
                data["pages"]= get_paginator(request, cases)
                data["case_name"]= ""
                return render(request, "sea/sea_test_case.html", data)
            else:
                if JobExecuted.objects.filter(job_id= "test_UI_job0_%s"%ex_time).first():
                    pass # 解决重复任务名的问题
                else:

                    test_case_list = [int(x) for x in test_case_list]
                    test_case_list.sort()  # 将id转化成int后排序

                    env= get_server_address(env)

                    case_task(test_case_list,env,request.user,id= '1231231231')
                    return render(request, "sea/sea_test_case.html", data)



        #             register_jobs(test_case_list,env,request.user.username,0,"test_job0_%s"%ex_time,
        #                           year,month,day,hour,minute)
        #             jbe= JobExecuted()  # 记录定时任务
        #             jbe.job_id= "test_job0_%s" % ex_time
        #             jbe.user= request.user.username
        #             jbe.status= 0
        #             jbe.save()
        #         return redirect(reverse("main_platform:test_execute",kwargs= {"jobid":"None"}))


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
    '''
    测试用例-新增用例页面，
    关联项目和模块，这个功能暂时不需要，后期再加
    '''
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