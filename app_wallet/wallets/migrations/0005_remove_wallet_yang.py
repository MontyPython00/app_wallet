# Generated by Django 4.2.4 on 2023-08-31 14:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wallets', '0004_alter_wallet_wallet_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wallet',
            name='yang',
        ),
    ]
