# Generated by Django 5.1.1 on 2024-09-10 22:19

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bankapp', '0002_customuser_fullname'),
    ]

    operations = [
        migrations.AddField(
            model_name='transactions',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]
