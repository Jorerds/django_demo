from django.shortcuts import render,redirect,reverse
from django.http import HttpResponse
from .models import User,User_info
# Create your views here.

def index(request):
    # user_info=User_info(user_job='项目经理',user_edtn='清华大学')
    # user_info.user_id=User.objects.get(id=2)
    # user_info.save()

    # 一对一外键查询方法
    # 这里是通过信息表外键查外键表
    user_info=User_info.objects.first()
    print(user_info.user_id)
    # 这里是通过关联外键查信息表
    user=User.objects.first()
    # 这个小写的user_info是被关联的表自动创建的一个属性名，默认是关联表的类名小写
    # 可用在OneToOneField添加属性related_name 来自定义的关联属性名
    print(user.user_info)

    return HttpResponse('成功')