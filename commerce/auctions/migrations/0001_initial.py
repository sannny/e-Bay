# Generated by Django 3.1.5 on 2021-01-14 21:48

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('username', models.CharField(max_length=10, primary_key=True, serialize=False, unique=True)),
                ('first_name', models.CharField(max_length=64)),
                ('last_name', models.CharField(max_length=64)),
                ('email', models.CharField(max_length=64)),
                ('password', models.CharField(max_length=64)),
                ('dob', models.DateField()),
                ('address', models.CharField(max_length=64)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Bids',
            fields=[
                ('bid_id', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('bid_date', models.DateField()),
                ('bid_amt', models.IntegerField()),
                ('bidder_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bidder_id', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('prod_id', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('description', models.TextField()),
                ('amount', models.IntegerField()),
                ('post_date', models.DateField()),
                ('end_date', models.DateField()),
                ('buyer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='buyer_id', to=settings.AUTH_USER_MODEL)),
                ('seller_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sellers_id', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='listing',
            fields=[
                ('list_id', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('amt', models.ManyToManyField(related_name='list_amount', to='auctions.Products')),
                ('bid_end_date', models.ManyToManyField(related_name='bid_end_date', to='auctions.Products')),
                ('bid_id', models.ManyToManyField(related_name='bids_id', to='auctions.Bids')),
                ('cust_id', models.ManyToManyField(related_name='seller_id', to=settings.AUTH_USER_MODEL)),
                ('list_date', models.ManyToManyField(related_name='list_date', to='auctions.Products')),
                ('products_id', models.ManyToManyField(related_name='products_id', to='auctions.Products')),
            ],
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('comment_id', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('message', models.TextField()),
                ('date', models.DateField()),
                ('commenter_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='commenter_name', to=settings.AUTH_USER_MODEL)),
                ('lists_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lists_id', to='auctions.listing')),
            ],
        ),
        migrations.AddField(
            model_name='bids',
            name='min_amount',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='min_amt', to='auctions.products'),
        ),
        migrations.AddField(
            model_name='bids',
            name='product_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_id', to='auctions.products'),
        ),
    ]
