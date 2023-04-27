## AutoTestPlatform-自动化测试平台

### 任务列表
#####1. 定时任务
#####1.1 数据库使用aps自带的，写个定时任务管理页面
#####2. 创建项目、模块、集合
#####3. 用户权限控制
#####4. 发送用例执行结果邮件


++++++++++++++++++++++++++++++++++++++
<br>
sudo /usr/local/bin/redis-server
<br>
celery -A main_platform  worker --loglevel=error
<br>
python3 manage.py runserver 0.0.0.0:8000
<br>
++++++++++++++++++++++++++++++++++++++