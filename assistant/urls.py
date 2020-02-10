from django.urls import path
from . import views
urlpatterns=[
    path('',views.login,name='login'),
    path('index',views.index,name='index'),
    path('result',views.result,name='result'),
    path('more',views.more,name='more'),
    path('msg',views.msg,name='msg'),
]