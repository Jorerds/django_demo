from django.shortcuts import render,redirect,reverse
from django.http import HttpResponse
from django.db import connection
from .models import Author,Publisher,Book,BookOrder
# 引入聚合函数
from django.db.models import Avg,Count,Max,Min,Sum,F,Q,Prefetch
# 导入可以查看模型转换成sql语句的方法，该方法能够看查找出来是字典类型
from django.db import connections

# Create your views here.
# 把数据库油标写进方法里
def get_corsor():
    return connection.cursor()

def book(request):
    # 原生sql查找
    # 连接数据信息
    cursor=get_corsor()
    # 执行sql语句
    cursor.execute("select id,book_name,author from dj_books")
    data=cursor.fetchall()

    # 模型查找
    # 聚合函数查找法：
    # avg求平均值
    # aggregate() 返回使用聚合函数后的字段和值
    result=Book.objects.aggregate(Avg('price')) #aggregate()这种聚合函数查找出来是一个字典
    print('聚合：计算平均值'+'*' * 100)
    print(result)

    # 关联+聚合函数查找
    # 需要查找出每本书的平均销售价格
    # 思路：需要从订单表中获取每一本书对应的订单从而同本的订单进行一个分组，再求平均值
    # 这时候需要用到的方法是annotate()这个方法，这个方法是在原来的模型的基础上添加一个使用了聚合函数的字段并且会在当前模型进行分组
    # 注意annotate()查找出来返回的是一个queryset对象
    books=Book.objects.annotate(avg=Avg("bookorder__price"))
    print('查找每本的平均销售价格（关联+聚合）'+'*'*100)
    print(books)
    print(books.query)
    for book in books:
        print('%s平均销售价格：%s'%(book.name,book.avg))
    # Count 计算表中某一字段一共有多少条数据
    # 可传递distinct 属性去重，设置为True就可以吧当前计数的字段去重
    result1=Book.objects.aggregate(Count('id'))
    print('计算数据条数'+'*'*100)
    print(result1)
    result2=Author.objects.aggregate(Count('email',distinct=True))
    print('计数去重'+'*'*100)
    print(result2)
    books1=Book.objects.annotate(book_sum=Count('bookorder'))
    print('计算每本书的销售量'+'*'*100)
    print(books1)
    for book in books1:
        print('%s销售量：%s'%(book.name,book.book_sum))
    # Max与Min 最大与最小
    result3=Author.objects.aggregate(Max('age'),Min('age'))
    print('求最大年龄与最小年龄'+'*'*100)
    print(result3)
    books2=Book.objects.annotate(price_max=Max('bookorder__price'),price_min=Min('bookorder__price'))
    print('求每本书的最大销售价格与最小销售价格'+'*'*100)
    print(books2)
    for book in books2:
        print('%s：最大销售价格%s 最小销售价格%s'%(book.name,book.price_max,book.price_min))
    # Sum 求指定字段的总和
    book_order=BookOrder.objects.aggregate(sum=Sum('price'))
    print('求所以图书的销售总和'+'*'*100)
    print(book_order)
    books3=Book.objects.annotate(book_sum=Sum('bookorder__price'))
    print('求每一本书的销售总和'+'*'*100)
    print(books3.query)
    for book in books3:
        print('%s：销售总和为%s'%(book.name,book.book_sum))
    # 求出2018年度销售总和
    # 思路：先查询出来2018的数据，再进行聚合函数求和
    # 这种叫链式调用，而能够使用这种链式调用必须是前面返回的是一个queryset对象
    book_order1=BookOrder.objects.filter(c_time__year=2018).aggregate(sum=Sum('price'))
    print('求出2018年度图书销售总和'+'*'*100)
    print(book_order1)
    # F表达式
    # 可动态的获取到sql里面的值
    # 例子：如果查询出邮箱和名字相同，不用F表达式的话，首先查出所有的作者，再进行邮箱比较比较麻烦
    # 但如果有了F表达式就可以直接在sql上面筛选
    authors1=Author.objects.filter(name=F('email'))
    print('查询邮箱和名字相同的用户'+'*'*100)
    print(authors1.query)
    print(authors1)
    # Q表达式
    # 当filter中传递两个条件的时候转换为sql语句是满足两种条件，既and的，与的意思，但如果需要实现or或条件就需要用到Q表达式
    books4=Book.objects.filter(Q(price__lte=200)|Q(rating__lte=4.7))
    print('查询图书价格小于200或评分小于4.8的书'+'*'*100)
    print(books4.query)
    print(books4)
    # Q表达式还可以取反操作，~Q意思是条件中的相反。
    books5=Book.objects.filter(~Q(id=1))
    print(books5)

    # queryset包涵的方法：
    # all : 提取模型所有数据
    # filter : 将满足条件的数据提取出来，返回一个新的queryset
    # objects.filter(条件)
    # exclude : 排除掉满足条件的数据，返回一个新的queryset，可理解为条件的相反
    # objects.exclude(条件)
    # annotate : 给queryset中每个对象都添加一个使用查询表达式（聚合函数、F表达式、Q表达式、Func表达式等等）的字段
    # objects.annotate(聚合函数条件)
    # order_by : 给指定查询的结果根据某个字段进行排序默认是正序从小到大 如果要实现反序可在指定字段前面加上负号表示反序
    # 反序：objects.order_by('-排序字段')
    books6=Book.objects.order_by('-rating')
    print('对查询的条件进行排序'+'*'*100)
    for book in books6:
        print("%s"%book.name)
    # values : 查询时指定查询的字段，返回queryset里面装的是字典
    # values('需要查询的字段') 可传递多个字段，可以使用聚合函数获取字段，如果没有传递参数，会获取模型上所有的字段
    # values_list : 和values是一样的，不过返回queryset里面装的是元组。可选参数flat=True拆开元组(不过只能在查询一个字段时候使用)
    books7=Book.objects.values('id','name','rating',author_name=F('author__name'))
    print('查询指定的字段'+'*'*100)
    for book in books7:
        print(book)
    # select_related : 能过查询到当前模型的关联模型的数据，用此方法进行查询可减少查询的次数从而减少性能的损耗
    # 可选参数，可传递多个模型参数作为查找关联数据，如果为空就默认查找出所有关联的模型
    # 但不能用在一对多的关系，例如每本书的订单，这种一对多关系
    books8=Book.objects.select_related()
    print('另外一种优化的方法来查询关联模型数据'+'*'*100)
    print(books8.query)
    for book in books8:
        print('书名：%s 作者：%s'%(book.name,book.author.name))
    # prefetch_related : 和select_related一样，只不过可以取到一对多或者是多对多关系的模型数据
    books9=Book.objects.prefetch_related('bookorder_set')
    print('可获取到一对多或多对多关系的关联模型数据优化方法'+'*'*100)
    for book in books9:
        orders=book.bookorder_set.all() #里面只能使用all()这个方法，不能使用其他的如果需要过滤可以用下面Prefetch的例子
        print('书名：%s'%book.name)
        for order in orders:
            print('订单id：%s 订单销售价格：%s'%(order.id,order.price))
    #  如果是想在使用prefetch_related的时候再对关联模型进行条件筛选的话可以使用Prefetch()这个方法
    prefetch=Prefetch('bookorder_set',queryset=BookOrder.objects.filter(price__gte=100))
    books10=Book.objects.prefetch_related(prefetch)
    print('对关联模型数据进行条件筛选，只显示订单大于100的订单'+'*'*100)
    for book in books10:
        print('书名：%s'%book.name)
        orders=book.bookorder_set.all()
        for orde in orders:
            print('订单id：%s 订单销售：%s'%(order.id,order.price))




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