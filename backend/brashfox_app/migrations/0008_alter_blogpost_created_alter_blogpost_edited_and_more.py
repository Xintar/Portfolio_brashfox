# Generated by Django 4.2.7 on 2023-12-15 20:33

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('brashfox_app', '0007_alter_fotodescription_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogpost',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Data powstania wpisu'),
        ),
        migrations.AlterField(
            model_name='blogpost',
            name='edited',
            field=models.DateTimeField(auto_now=True, default=datetime.datetime.now, verbose_name='Data aktualizacji wpisu'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='fotodescription',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Data powstania opisu'),
        ),
        migrations.AlterField(
            model_name='fotodescription',
            name='edited',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='Data aktualizacji'),
        ),
        migrations.AlterField(
            model_name='message',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='postcomments',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Data powstania komnentarza'),
        ),
        migrations.AlterField(
            model_name='postcomments',
            name='edited',
            field=models.DateTimeField(auto_now=True, default=datetime.datetime.now, verbose_name='Data aktualizacji edycji'),
            preserve_default=False,
        ),
    ]
