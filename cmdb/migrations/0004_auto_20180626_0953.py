# Generated by Django 2.0.5 on 2018-06-26 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb', '0003_auto_20180626_0947'),
    ]

    operations = [
        migrations.AlterField(
            model_name='disk',
            name='model',
            field=models.CharField(max_length=128, verbose_name='磁盘型号'),
        ),
    ]