# Generated by Django 4.2.7 on 2023-11-13 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crud_api', '0002_user_created_at_and_updated_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='created_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='updated_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
