# Generated by Django 3.1.1 on 2020-10-29 12:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_auto_20201029_0920'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='seller',
            field=models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.CASCADE, related_name='listings', to='auctions.user'),
            preserve_default=False,
        ),
    ]