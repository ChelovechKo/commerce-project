# Generated by Django 5.1.2 on 2024-11-01 07:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_remove_user_name_alter_user_username'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='fraction',
        ),
        migrations.AddField(
            model_name='user',
            name='faction',
            field=models.CharField(blank=True, choices=[('', '— No faction —'), ('College of Winterhold', 'College of Winterhold'), ('Dark Brotherhood', 'Dark Brotherhood'), ('Thieves Guild', 'Thieves Guild'), ('Companions', 'Companions'), ('Imperial Legion', 'Imperial Legion'), ('Stormcloaks', 'Stormcloaks')], max_length=100, null=True),
        ),
    ]