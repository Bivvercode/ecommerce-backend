# Generated by Django 5.0.4 on 2024-05-23 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_alter_unit_name_alter_unit_symbol'),
    ]

    operations = [
        migrations.AlterField(
            model_name='unit',
            name='name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='unit',
            name='symbol',
            field=models.CharField(max_length=9),
        ),
    ]