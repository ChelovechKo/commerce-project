# Generated by Django 5.1.2 on 2024-11-06 13:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0012_alter_listing_price'),
    ]

    operations = [
        migrations.RenameField(
            model_name='listing',
            old_name='create_date',
            new_name='date_create',
        ),
        migrations.RemoveField(
            model_name='listing',
            name='current_bid',
        ),
        migrations.RemoveField(
            model_name='listing',
            name='starting_bid',
        ),
    ]