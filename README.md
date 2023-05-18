## AutoTestPlatform-自动化测试平台

### 任务列表
<br>
1. 定时任务(完成)
<br>
2. https/dubbo请求方式加入
<br>
3. 用户权限控制，那些个账户能看那些网页
<br>
4. 发送用例执行结果邮件
<br>
4.1将测试记录通过邮件发送，写个配置页面
<br>
++++++++++++++++++++++++++++++++++++++
<br>
sudo /usr/local/bin/redis-server
<br>
celery -A main_platform  worker --loglevel=error
<br>
python3 manage.py runserver 0.0.0.0:8000
<br>
++++++++++++++++++++++++++++++++++++++