# Generated by Django 2.1.3 on 2019-01-08 14:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_info',
            name='user_id',
            field=models.OneToOneField(db_column='user_id', on_delete=django.db.models.deletion.CASCADE, to='user.User'),
        ),
    ]
