# Generated by Django 4.2.4 on 2023-10-24 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0007_supplier'),
    ]

    operations = [
        migrations.AddField(
            model_name='supplier',
            name='address',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
