from django.db import models

# Create your models here.

class User(models.Model):
    user_name=models.CharField(max_length=254,null=False)
    power=models.IntegerField(null=True)
    c_time=models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table='dj_user'

    def __str__(self):
        dicts={
            'user_name':self.user_name,
            'user_power':self.power,
            'c_time':self.c_time,
        }
        return str(dicts)

class User_info(models.Model):
    user_job=models.CharField(max_length=254,null=True)
    user_edtn=models.CharField(max_length=254,null=True)
    # 插入一对一关系的外键,可以理解为1个id在这个表中只有一条数据，不能多条
    # 深入理解，django利用数据中的唯一键来实现
    user_id=models.OneToOneField('User',on_delete=models.CASCADE,null=False,db_column='user_id')

    class Meta:
        db_table='dj_user_info'

    def __str__(self):
        dicts={
            'id':self.id,
            'user_job':self.user_job,
            'user_edth':self.user_edtn,
            'user_id':self.user_id,
        }
        return str(dicts)
