# Generated by Django 2.2.4 on 2021-12-02 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contactApp', '0003_auto_20211129_2107'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resume',
            name='birth',
            field=models.DateField(default='2021-12-02', max_length=20, verbose_name='出生日期'),
        ),
    ]
