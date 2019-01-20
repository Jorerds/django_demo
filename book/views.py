from django.shortcuts import render,redirect,reverse
from django.http import HttpResponse
from django.db import connection
# Create your views here.
# 把数据库油标写进方法里
def get_corsor():
    return connection.cursor()

def book(request):
    # 连接数据信息
    cursor=get_corsor()
    # 执行sql语句
    cursor.execute("select id,book_name,author from dj_books")
    data=cursor.fetchall()

    return render(request,'book_list.html',context={'data':data})

def book_detail(request,book_id):
    text="获取书本id：%s"%book_id
    return HttpResponse(text)

# url传参的方式视图参考
def author_detail(request):
    # 无需在创建函数中定义变量，只需要在方法中获取
    author_id=request.GET.get('id')
    text='作者id是：%s'%(author_id)
    return HttpResponse(text)

def add_book(request):
    if request.method == 'GET':
        return render(request, 'book_local.html')
    else:
        book_name = request.POST.get("book_name")
        author = request.POST.get('author')
        cursor = get_corsor()
        cursor.execute("insert into dj_books(book_name,author)values ('%s','%s')" % (book_name, author))
        return redirect(reverse('book'))

def add_book_ui(request):
    book_id=request.GET.get('book_id','')
    if book_id!='':
        cursor=get_corsor()
        cursor.execute("select id,book_name,author from dj_books where id=%s"%book_id)
        data=cursor.fetchone()
        return render(request,'book_local.html',context={'data':data})
    else:
        return render(request, 'book_local.html')

# 测试ajax
def ajax_data(request):
    name=request.POST.get('name')
    print(name)