from django.db import models

# Create your models here.
# 如果要把普通的类变成一个映射到数据库中的ORM模型
# 就必须将父类设置成为models.Model或者他的子类
class dj_disc(models.Model):
    # 常用设置字段类型
    # AutoField 为自动增长
    # BigAutoField 64位的整形也是自动增长
    # BooleanField 布尔类型True/False
    # CharField 为字符串类型varchar,但如果超过了254个字符就不使用这个
    # TextField 为字符串类型longtext
    # DateField 是数据库中的date类型，只能存储年月日
    # DateTimeField 是数据库中的datetime类型，可以存储年月日和时间
    # TimeField 是数据库中的time类型，只能存储时间
    # EmailField 类似CharField，在数据库也是varchar类型，最大长度是254个字符 如不定义默认长度，默认是254个字符
    # EmailField 在数据库层面是并不会验证接收的数据是否是邮箱格式，但这个类型是用于ModeForm表单提交时候会起验证作用
    # FileField 存储文件用的类型
    # FloatField 浮点类型
    # IntegerField 整形
    # BigIntegerField 大整形
    # PositiveIntegerField 正整形
    # PositiveSmallIntegerField 正小整形
    # SmallIntegerField 小整形
    # UUIDField uuid格式字符串，uuid是一个32位全球唯一的字符串，一般用来作为主键
    # URLField 类似CharField，只不过只能用来存储url格式的字符串。并且默认的max_length是200
    # ForeignKey 普通常用设置的外键类型
    # OneToOneField 一对一使用的外键类型（一张表对一张表）

    # 常用参数
    # null 设置是否为空。如果设置了null=True 的话如果插入数据没有传数据那么数据库表
    # 这个字段会为一个null值，如果设置null=False 的情况空数据插入时候django会自动插入空的字符串
    # blank 判断表单提交数据时候会验证是否为空,默认是False。
    # db_column 设置这个字段在数据库表中的名字，如果没有设置默认是使用模型中属性的名字
    # default 设置字段的默认值
    # primary_key 是否为主键，默认是False
    # unique 表示这个字段的值是否唯一，一般是设置手机号码/邮箱等


    id=models.AutoField(primary_key=True)
    title=models.CharField(max_length=255,null=False)
    aid=models.IntegerField(null=False)
    content=models.CharField(max_length=2000,null=False)
    # auto_now_add=True 在第一次添加数据的时候可以自动获取当前对象，一般来用于自动插入时间数据
    # auto_now=True  每次调用save方法的时候都会更新时间数据
    c_time=models.DateTimeField(auto_now_add=True)

    # ForeignKey 关联外键，联表查询
    # 第一个参数输出入关联的表
    # 第二个参数为啥外键操作方式：CASCADE 为级联操作，如果外键的表的数据被删除，关联本表的数据也将删除
    # PROTECT 受保护，只要数据引用了外键，那么就不能删除该引用外键表上的数据
    # SET_NULL 设置空，当外键表关联的数据被删除那么自身表的外键关联字段将设置为空，前提条件是这个字段可以为空
    # SET_DEFAULT 设置默认值，如果外键关联的数据被删除了那么将使用默认值
    # SET  指定值，当被关联数据被删除了那么需要指定个值
    # DO_NOTHING 不采取任何行为。一切全看数据库级别的约束

    # 如果要引入其他app的模型，需要第一个参数模型名字前面接上APP的名字，APP名.模型名字
    # related_name 是外键的一个属性，设置关联查找用的属性名称 例如：related_name='fen'
    fenle=models.ForeignKey("Fenle",on_delete=models.CASCADE,null=True)

    # 多对多关系
    # 一般多对多需要两张表之间还需要一张中间表，orm模型会自动为多对多关系创建中间表
    tag=models.ManyToManyField('Tag')


    # 固定的模型类，用于操作模型的参数
    # 类中的变量：
    # db_table  设置数据库中的这个模型的数据表的名称，如果不设置这个，django会默认读取名字格式：APP名字_整个模型类的名字
    # ordering 设置提取数据的排序方式
    class   Meta:
        db_table = 'dj_disc'
        # 注意排序的方法是一个列表，所以可以传递多个值（多个依次排序）
        # 排序字段参数前面加上 - 负号是降序（默认是升序）
        ordering = ['-c_time','id']

# 映射模型创建数据库需要在命令行中输入命令：
# 第一步进入项目目录输入命令
# 1. python manage.py makemigrations  生成迁移脚本文件
# 2. python manage.py migrate  将新生成的迁移脚本文件映射到数据库中

#   查询接收到的数据形式可在这个方法中定义
#     这里我改成了放回字典的形式
    def __str__(self):
        dic={
            'id':self.id,
            'title':self.title,
            'aid':self.aid,
            'content':self.content,
            'c_time':self.c_time,
        }
        return str(dic)



class Fenle(models.Model):
    fl_name=models.CharField(max_length=254,null=False)
    class Meta:
        db_table = 'dj_fenle'
    def __str__(self):
        dic={
            'id':self.id,
            'fl_name':self.fl_name,
        }
        return str(dic)


class Tag(models.Model):
    name=models.CharField(max_length=100,null=False)
    class Meta:
        db_table='dj_tag'
    def __str__(self):
        dic={
            'id':self.id,
            'name':self.name,
        }
        return str(dic)