# Generated by Django 4.2.7 on 2023-12-15 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('brashfox_app', '0006_alter_fotodescription_edited'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fotodescription',
            name='image',
            field=models.ImageField(upload_to='./static/images/portfolio', verbose_name='Zdjęcie'),
        ),
    ]