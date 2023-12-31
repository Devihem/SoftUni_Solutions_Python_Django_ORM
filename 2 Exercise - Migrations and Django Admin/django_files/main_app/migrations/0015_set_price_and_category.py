# Generated by Django 4.2.4 on 2023-10-30 18:44

from django.db import migrations
from main_app.models import Smartphone


def set_price(apps, schema_editor):
    smartphones_obj = apps.get_model('main_app', 'Smartphone')

    smartphones_all = smartphones_obj.objects.all()

    for smartphone_data in smartphones_all:
        new_price = len(smartphone_data.brand) * 120
        smartphone_data.price = new_price

    smartphones_obj.objects.bulk_update(smartphones_all, ['price'])


def reverse_price(apps, schema_editor):
    smartphones_obj = apps.get_model('main_app', 'Smartphone')

    smartphones_all = smartphones_obj.objects.all()

    for smartphone_data in smartphones_all:
        smartphone_data.price = 0

    smartphones_obj.objects.bulk_update(smartphones_all, ['price'])


def set_category(apps, schema_editor):
    smartphones_obj = apps.get_model('main_app', 'Smartphone')

    smartphones_all = smartphones_obj.objects.all()

    for smartphone_data in smartphones_all:
        if smartphone_data.price >= 750:
            smartphone_data.category = 'Expensive'
        else:
            smartphone_data.category = 'Cheap'

    smartphones_obj.objects.bulk_update(smartphones_all, ['category'])


def reverse_category(apps, schema_editor):
    smartphones_obj = apps.get_model('main_app', 'Smartphone')

    smartphones_all = smartphones_obj.objects.all()

    for smartphone_data in smartphones_all:
        smartphone_data.category = 'empty'

    smartphones_obj.objects.bulk_update(smartphones_all, ['category'])


class Migration(migrations.Migration):
    dependencies = [
        ('main_app', '0014_smartphone'),
    ]

    operations = [migrations.RunPython(set_price, reverse_price),
                  migrations.RunPython(set_category, reverse_category)
                  ]
