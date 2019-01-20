"""pyweb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
# 需要导入app的视图
from book import views

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('book/',views.book,name='book'),
    path('add_sever_book/',views.add_book,name='add_sever_book'),
    path('add_book/',views.add_book_ui,name='add_book'),
    path('ajax_data/',views.ajax_data,name='ajax_data'),
    # 在URL中添加了变量，必须要给视图函数添加变量
    path('book/detail=<book_id>',views.book_detail,name='book_detail'),
    # URL传参方式
    # 在django中传参不需要在url地址中加上? 只需要在视图函数中获取到变量就可以了
    path("book/author",views.author_detail),
    # 定义子url的规则，需要使用到include方法
    path('',include('frot.urls')),
    path('admin/',include('cms.urls')),
    path('disc/',include('disc.urls')),
    path('user/',include('user.urls')),

]
