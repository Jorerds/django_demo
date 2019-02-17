from django.db import models

# Create your models here.

class Author(models.Model):
    '''作者模型'''
    name=models.CharField(max_length=100)
    age=models.IntegerField()
    email=models.EmailField()

    class Meta:
        db_table='book_author'


class Publisher(models.Model):
    '''出版社模型'''
    name=models.CharField(max_length=250)
    class Meta:
        db_table='publisher'

class Book(models.Model):
    '''图书模型'''
    name=models.CharField(max_length=300) #书名
    pages=models.IntegerField() #书页
    price=models.FloatField() #价格
    rating=models.FloatField() #评分
    author=models.ForeignKey(Author,on_delete=models.CASCADE) #作者
    publisher=models.ForeignKey(Publisher,on_delete=models.CASCADE) #出版社
    class Meta:
        db_table='book'

class BookOrder(models.Model):
    '''图书订单模型'''
    book=models.ForeignKey('Book',on_delete=models.CASCADE)
    price=models.FloatField()
    c_time=models.DateTimeField(auto_now_add=True,null=True)
    class Meta:
        db_table='book_order'