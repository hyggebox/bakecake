# Generated by Django 4.0.4 on 2022-04-30 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cakes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.EmailField(max_length=255, verbose_name='email'),
        ),
    ]
