from django.shortcuts import render,redirect,reverse
import datetime
from django.http import  HttpResponse
from django.utils.timezone import now,localtime
# 如果要使用ORM模型来进行数据库的操作，必须要先导入数据库
from .models import dj_disc,Fenle,Tag
# Create your views here.

def disc_index(request):
    # 注意所以查询都是在objects进行，所以如果当你一个方法中对一个模型进行多次查询，都会以附带上主键条件
    # ORM模型查找 get方法是查找一条
    # pk是代表固定的根据表的主键条件进行查找
    # disc=dj_disc.objects.get(pk=1)
    # filter()方法是根据其他条件查找出符合条件的多条数据
    # 返回为一列表
    discs=dj_disc.objects.filter()

    # 数据库一对多关联操作
    # 如果要获取某一个分类下的所有文章
    # 1.先获取到要获取到查找的分类
    fenles=Fenle.objects.first()
    # 获取到了分类接下来用这个分类的一个属性来查找所引用了分类这个分类的文章
    # django模型被引用会默认添加一个由 引用模型名字小写+下划线+set 的属性
    # 可以给引用的模型的外键字段添加 related_name 属性，可以设置上面关联的属性名称 改为 这个属性的名称
    # 例如：如果我 related_name='fen'  那么 下面的语句应该改为 fenles.fen.all()
    fends=fenles.dj_disc_set.all()
    print(fends)


    # 多对多查询关系(一篇文章下所有的标签)
    disc1=dj_disc.objects.get(id=4)
    tag=disc1.tag.all()
    print('查询多对多(一篇文章下所有的标签)：%s'%tag)

    # 多对多查询关系(一个标签下的所有文章)
    tag1=Tag.objects.get(id=3)
    disc2=tag1.dj_disc_set.all()
    print('查询多对多(一个标签下的所有文章)：%s'%disc2)

    # 查询条件
    # exact 精确查找(这个条件可写可不写)
    disc3=dj_disc.objects.filter(id__exact=5)
    # 小细节：可用query对象来对查询模型进行查看orm模型转换成的sql语句
    # query不能用在get的这种返回ORM模型，只能用在QuerySet类型
    print(disc3.query)
    print('查询条件exact精确查找：%s'%disc3)

    # iexact 模糊查找
    # 在底层会被编译为sql中的LIKE条件
    disc4=dj_disc.objects.filter(title__iexact="测试内容字段")
    print(disc4.query)
    print('模糊查找iexact：%s'%disc4)

    # contains 匹配查找（大小写敏感）
    # icontains 匹配查找（大小写不敏感）
    disc5=dj_disc.objects.filter(title__contains='测试')
    print(disc5.query)
    print('匹配查找（区分大小写）：%s'%disc5)

    # in 和sql中的in用法一样判断是否在一个字符集中
    disc6=dj_disc.objects.filter(id__in=[1,2,5])
    print(disc6.query)
    print('in判断是否存在字符集中：%s'%disc6)
    # in 查询外键的数据的字符集查询（关联模型查找）
    # 解析：属性中是查找模型然后用双下划线接条件字段（可直接写模型的名字，这样的话默认是查id主键）
    fenles1=Fenle.objects.filter(dj_disc__id__in=[2,3])
    print(fenles1.query)
    print('查询当前文章分类外键的数据：%s'%fenles1)
    # 特别使用：在in中不仅仅条件不仅仅可以是一个列表还可以是一个元组和QuerySet对象
    # 例子：查找标题中含有测试的分类
    disc7=dj_disc.objects.filter(title__icontains='测试')
    fenles2=Fenle.objects.filter(dj_disc__id__in=disc7)
    print(fenles2.query)
    print(fenles2)

    # 范围查询
    # gt: 意思是大于条件
    # gte: 大于等于
    # lt: 小于
    # lte: 小于等于
    disc8=dj_disc.objects.filter(id__gt=2)
    print(disc8.query)
    print(disc8)

    # 区间查询
    # startswith: 查找某字段是否以某个值开头（大小写区分）
    # istartswith: 查找某字段是否以某个值开头（大小写不区分）
    # endswith: 查找以某字段是否以某个值结束（大小写区分）
    # iendswith: 查找以某字段是否以某个值结束（大小写不区分）
    disc9=dj_disc.objects.filter(title__istartswith='外键')
    print(disc9.query)
    print(disc9)






    return render(request,'disc_index.html',context={'discs':discs})

# ORM模型添加数据
def disc_add(request):
    # 外键数据的添加，如果外键没有数据的话在这里添加的需要先保存插入一下外键表的数据
    fenles=Fenle(fl_name='奇幻小说') # 外键创建数据
    fenles.save() #外键保存数据
    # ORM模型的方式添加数据
    # localtime方法转换时区
    c_time=localtime(now())
    disc=dj_disc(title='测试标题13',aid=2,content='测试内容字段35')
    disc.fenle= fenles
    # 运行插入数据
    disc=disc.save()

    # 上面那种外键保存的方式是在外键表没有数据的情况下才用的
    # 如果想要添加的外键在外键表已经存在的情况下思路是先查出这个外键数据，再给外键赋值给查找到的外键
    disc2=dj_disc(title='外键数据',aid=3,content='添加已存在外键数据的数据')
    # 查找出要添加外键表的数据
    fenles1=Fenle.objects.get(pk=2)
    # 然后给外键赋值查找出来的外键表的数据
    disc2.fenle=fenles1
    # 最后保存
    disc2.save()

    # 这是外键关联数据表的另外一种保存方式(这种方式不常用，推荐上面一种方式)
    # 直接用到了关联属性名称来设置
    # 查询关联外键
    fenles2=Fenle.objects.get(pk=1)
    disc3=dj_disc(title='外键数据添加2',aid=1,content='外键数据添加的另外一种方式')
    # 用模型外键关联名称对象，再用add这个方法来保存，而bulk这个属性是放置多个外键关联中防止出现某一外键不能为空的情况
    fenles2.dj_disc_set.add(disc3,bulk=False)


    return HttpResponse('添加成功')

# ORM模型删除操作
def disc_delete(request):
    disc=dj_disc.objects.get(id=6)
    quest=disc.delete()
    print(quest)
    if quest==1:
        return HttpResponse('删除成功')
    else:
        return HttpResponse('删除失败，请检查是否存在该数据')

# ORM模型修改操作
def disc_update(request):
    # disc=dj_disc.objects.get(id=5)
    # disc.title='测试标题5'
    # quest=disc.save()

    # 多对多关系（创建标签并给文章添加）
    # disc=dj_disc.objects.get(id=4)
    # tag=Tag(name='技术文章')
    # tag.save()
    # # 注意 dj_disc_set 这个属性是给引用的那一张表添加的属性
    # tag.dj_disc_set.add(disc)

    # 多对多（给文章添加标签）
    disc = dj_disc.objects.get(id=5)
    tag=Tag.objects.get(id=3)
    tag.dj_disc_set.add(disc)




    return HttpResponse('修改成功')