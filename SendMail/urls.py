from django.conf.urls import url
from SendMail import views



# app_name= "[UserAuthAndPermission]"
urlpatterns= [
    url(r'^email/', views.email),
    url(r'^get_result/', views.get_result),
]