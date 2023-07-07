import time
import logging
import unittest
from . import models
from . import viewsParams as vp
from BeautifulReport import BeautifulReport
from main_platform.celery import ex_cases_app_sea
from main_platform.tasks import ParametrizedTestCase



from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC



logger= logging.getLogger("selenium_apps")


class BeginTest(ParametrizedTestCase):
    '''使用unittest进行UI测试'''
    def setUp(self):
        '''用例准备操作'''
        self.doc= "131312312313131"
        print(1231231313213123132)

    def testMethod(self):
        '''用例断言，判断用例是否通过'''
        logger.info("selenium_apps_testsssss")
        self.assertEqual(True, True)

    def tearDown(self):
        '''用例结束操作'''
        pass



@ex_cases_app_sea.task
def case_task(test_case_list:list, server_address, user,id):
    '''
    进行测试用例的执行操作
    :param test_case_list: 用例id列表
    :param server_address: 服务器信息
    :param user: 执行用户
    :return:
    '''
    time.sleep(3)
    list_open= []
    suite= unittest.TestSuite()
    for tcl in test_case_list:
        detail= models.TestCaseForSEA.objects.get(id= tcl)
        steps= models.TestCaseSteps.objects.filter(testcaseid_id= detail.id)\
            .values_list("LocationPath","Method","Parameter","Action","Expected")
        # values_list可以将queryset转换成tuple，需要指定字段

        steps= [list(i) for i in steps]
        list_open.append({str(tcl):steps})

    for i in list_open:
        suite.addTest(ParametrizedTestCase.parametrize(BeginTest, case=i,
                                                       server_address= server_address,
                                                       type="case"))

    result= BeautifulReport(suite)
    time_ = str(time.strftime("%Y_%m_%d_%H:%M:%S", time.localtime(time.time())))
    result.report(filename="UI测试报告" + time_,
                  description="自动化测试平台报告",
                  report_dir="report",
                  theme="theme_memories")



    # driver = webdriver.Chrome()
    # driver.get('http://www.baidu.com')
    # time.sleep(3)
    # driver.find_element('xpath', '//*[@id="kw"]').send_keys('test')
    # driver.find_element('id', 'su').click()
    # time.sleep(3)
    # driver.quit()