# Generated by Django 4.2.5 on 2023-09-08 11:56

import django.contrib.postgres.fields
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coins', '0019_alter_coinholder_amount_of_coin_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coin',
            name='market_cap',
        ),
        migrations.RemoveField(
            model_name='coin',
            name='stocks_left',
        ),
        migrations.AddField(
            model_name='coin',
            name='_market_cap',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.DecimalField(decimal_places=3, max_digits=16, validators=[django.core.validators.MinValueValidator(0)]), blank=True, default=list, null=True, size=None),
        ),
        migrations.AddField(
            model_name='coin',
            name='_stocks_left',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.DecimalField(decimal_places=3, max_digits=16, validators=[django.core.validators.MinValueValidator(0)]), blank=True, default=list, null=True, size=None),
        ),
        migrations.AlterField(
            model_name='coinholder',
            name='amount_of_coin',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.DecimalField(decimal_places=5, max_digits=16, validators=[django.core.validators.MinValueValidator(0)]), default=list, size=None),
        ),
        migrations.AlterField(
            model_name='coinholder',
            name='avg_buy_price',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.DecimalField(decimal_places=5, max_digits=16, validators=[django.core.validators.MinValueValidator(0)]), default=list, size=None),
        ),
    ]