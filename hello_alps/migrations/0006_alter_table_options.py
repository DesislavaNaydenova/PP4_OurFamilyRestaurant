# Generated by Django 4.2.14 on 2024-08-19 10:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hello_alps', '0005_table'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='table',
            options={'ordering': ['table_number']},
        ),
    ]
