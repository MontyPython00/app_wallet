# Generated by Django 4.2.5 on 2023-09-07 12:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('coins', '0013_remove_coinholder_coins_coinholder_coin'),
    ]

    operations = [
        migrations.RenameField(
            model_name='buy',
            old_name='wallet',
            new_name='buy_wallet',
        ),
    ]
