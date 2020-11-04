# Generated by Django 3.1.1 on 2020-11-04 13:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0010_listing_created_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='watchlist',
            name='list_name',
        ),
        migrations.AlterField(
            model_name='watchlist',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='watchlist', to=settings.AUTH_USER_MODEL),
        ),
    ]