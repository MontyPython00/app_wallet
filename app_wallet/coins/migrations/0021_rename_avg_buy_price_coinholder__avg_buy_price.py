# Generated by Django 4.2.5 on 2023-09-08 15:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('coins', '0020_remove_coin_market_cap_remove_coin_stocks_left_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='coinholder',
            old_name='avg_buy_price',
            new_name='_avg_buy_price',
        ),
    ]