# 这是加载封装好的模板方法，这种方式无需手动把模板渲染成字符串在返回
from django.shortcuts import render
from django.http import  HttpResponse
# 渲染模板，这种方式需要把模版渲染成一个字符串
from django.template.loader import render_to_string
# django封装的时区方法，获取到的时间为aware类型的时间
from django.utils.timezone import now
from datetime import datetime
# 专门用来设置区时
import pytz
# Create your views here.

def index(request):
    # 加载模板渲染模板
    # 时区
    # timezone()方法可以转换时区
    # 但不能转换navie类型
    now=datetime.now() # 这个获取到的是navie类型
    utc_timezone=pytz.timezone("UTC")
    # 直接使用转换会报错，now.astimezone(utc_timezone)
    # 中国时区
    now=now.replace(tzinfo=pytz.timezone("Asia/Shanghai"))
    # 切换其他时区
    utc_now=now.astimezone(utc_timezone)
    print(utc_now)
    print(now)
    html=render_to_string("index.html")
    return HttpResponse(html)

def login(request):
    # 使用封装包渲染模板
    return render(request,'login.html')
