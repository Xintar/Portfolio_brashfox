# Generated by Django 4.2.7 on 2023-12-09 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('brashfox_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='Imię')),
                ('email', models.EmailField(max_length=254, verbose_name='E-mail')),
                ('topic', models.CharField(max_length=64, verbose_name='Temat')),
                ('message', models.TextField(verbose_name='Wiadomość')),
            ],
        ),
    ]
