# Generated by Django 5.1.2 on 2024-11-06 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0011_remove_listing_cnt_bid_remove_listing_user_bid_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='price',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
