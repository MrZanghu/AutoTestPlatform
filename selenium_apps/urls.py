from django.urls import re_path,path
from selenium_apps import views



app_name= "[send_mails]"
urlpatterns= [
    path(r'test_case/', views.test_case,name= "test_case"),
]