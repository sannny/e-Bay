# Generated by Django 3.1.5 on 2021-01-15 01:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_auto_20210114_1621'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='prod_image',
            field=models.CharField(blank=True, max_length=256),
        ),
        migrations.AddField(
            model_name='products',
            name='prod_name',
            field=models.CharField(default='', max_length=20),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='products',
            name='buyer_id',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='buyer_id', to=settings.AUTH_USER_MODEL),
        ),
    ]
