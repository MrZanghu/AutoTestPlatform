from django.db import models
from django.contrib.auth.models import User



class TestCaseForSEA(models.Model):
    '''用例模型'''
    id= models.AutoField(primary_key= True)
    case_name= models.CharField("用例名称", max_length= 256, blank= True, null=True)
    status= models.IntegerField(blank= True, null= True, help_text="0:表示有效，1:表示无效，用于软删除", default= 0)
    create_time= models.DateTimeField("创建时间", auto_now_add= True)
    user= models.CharField("创建人", max_length= 20, blank= True, null= True)

    # 打印对象时返回项目名称
    def __str__(self):
        return self.case_name

    class Meta:
        db_table= "sea_test_case"
        verbose_name= "测试用例表"
        verbose_name_plural= "测试用例表"


class TestCaseSteps(models.Model):
    '''用例模型-测试步骤'''
    id= models.AutoField(primary_key= True)
    testcaseid= models.ForeignKey(TestCaseForSEA,on_delete= models.CASCADE, verbose_name= "所属用例")
    LocationPath= models.CharField("定位路径", max_length= 256, blank= True, null=True)
    Method= models.CharField("方法|操作", max_length= 256, blank= True, null=True)
    Parameter= models.CharField("传入参数", max_length= 256, blank= True, null=True)
    Action= models.CharField("步骤动作", max_length= 256, blank= True, null=True)
    Expected= models.CharField("预期结果", max_length= 256, blank= True, null=True)
    status= models.IntegerField(blank= True, null= True, help_text="0:表示有效，1:表示无效，用于软删除", default= 0)
    create_time= models.DateTimeField("创建时间", auto_now_add= True)

    # 打印对象时返回项目名称
    def __str__(self):
        return self.testcaseid

    class Meta:
        db_table= "sea_test_case_steps"
        verbose_name= "用例步骤表"
        verbose_name_plural= "用例步骤表"
