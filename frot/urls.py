from django.urls import path
# 导入当前视图函数，由于是app的子url所以用.来代表当面目录
from . import views
# 定义应用命名空间，可防止url命名重复的问题
# 应用命名空间的变量叫做app_name
app_name='frot'
urlpatterns=[
    path('',views.index,name='index'),
    path('login/',views.login,name='login'),
]