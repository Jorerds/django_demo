from django.shortcuts import render
from django.http import  HttpResponse
# 使用重定向的方式来实现检测跳转
# redirect：为重定向路由
# reverse：获取指定url命名的url
from django.shortcuts import  redirect,reverse
from datetime import datetime
from django.template.loader import render_to_string
# Create your views here.

class   Person(object):
    def __init__(self,user_name):
        self.user_name=user_name

def index(request):
    # 实现一个简单的检测登陆跳转功能
    user_id=request.GET.get('user_id')
    # 传递对象到模板
    user_name=Person('菲尔斯')
    # 传递参数到模板中
    context = {
        'user_id': user_id,
        'user_name':user_name,
        # 给模板传递一个字典中的字典
        'messg':{
            'sex':'男',
            'age':'16',
        },
        # 给模板传递列表
        'hobby':[
            '游戏',
            '电影',
            '运动',
        ],
        'projs':[
            {
                'pj_name':'腾讯',
                'pj_po':'架构工程师',
                'pj_num':'5年',
            },
            {
              'pj_name':'阿里巴巴',
                'pj_po':'开发工程师',
                'pj_num':'4年',
            },
            {
                'pj_name':'谷歌',
                'pj_po':'人工智能工程师',
                'pj_num':'3年',
            }
        ],
        'evts':[

        ],
        'greet':greet,
        'add_view1':[1,5,'1','50'],
        'add_view2':[15,'54','9'],
        'cut_view':'你好我这 里要过 滤掉空格字符',
        'date_view':datetime.now(),
    }

    if user_id:
        return render(request,'admin_index.html',context=context)
    else:
        # 反转url可使用命名空间，防止重复url命名混淆
        login_url=reverse('cms:login')
        return redirect(login_url)

def login(request):
    return render(request,'admin_login.html')

def greet(word):
    return '练习过滤器传递的参数：%s'%word