# Generated by Django 5.1.1 on 2024-09-09 22:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bankapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='fullname',
            field=models.CharField(default=1, max_length=1000),
            preserve_default=False,
        ),
    ]
