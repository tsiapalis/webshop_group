# Generated by Django 5.1.3 on 2024-12-03 07:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core_app', '0005_rename_list_of_items_order_item_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='total_cost',
        ),
    ]
