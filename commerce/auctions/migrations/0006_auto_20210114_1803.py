# Generated by Django 3.1.5 on 2021-01-15 02:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_auto_20210114_1744'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='prod_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]