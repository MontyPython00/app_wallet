# Generated by Django 4.2.5 on 2023-09-08 15:27

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wallets', '0013_alter_wallet_main_wallet'),
        ('coins', '0023_rename_amount_of_coin_coinholder__amount_of_coin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buy',
            name='amount_of_coin',
            field=models.DecimalField(decimal_places=2, max_digits=16, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='buy',
            name='total_price',
            field=models.DecimalField(decimal_places=2, max_digits=16, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.CreateModel(
            name='Sell',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('amount_of_coin', models.DecimalField(decimal_places=2, max_digits=16, validators=[django.core.validators.MinValueValidator(0)])),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=16, validators=[django.core.validators.MinValueValidator(0)])),
                ('coin', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='coins.coin')),
                ('wallet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wallets.wallet')),
            ],
        ),
    ]
