# Generated by Django 4.2.5 on 2023-09-07 10:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('coins', '0012_remove_coinholder_coin_coinholder_coins_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coinholder',
            name='coins',
        ),
        migrations.AddField(
            model_name='coinholder',
            name='coin',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='coins.coin'),
        ),
    ]
