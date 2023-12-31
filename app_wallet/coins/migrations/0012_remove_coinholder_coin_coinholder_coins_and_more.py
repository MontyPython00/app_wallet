# Generated by Django 4.2.5 on 2023-09-07 10:08

import django.contrib.postgres.fields
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coins', '0011_buy_coin_coinholder_coin'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coinholder',
            name='coin',
        ),
        migrations.AddField(
            model_name='coinholder',
            name='coins',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.DecimalField(decimal_places=5, max_digits=16, validators=[django.core.validators.MinValueValidator(0)]), default=list, size=None),
        ),
        migrations.AlterField(
            model_name='coinholder',
            name='amount_of_coin',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.DecimalField(decimal_places=5, max_digits=16, validators=[django.core.validators.MinValueValidator(0)]), default=list, size=None),
        ),
    ]
