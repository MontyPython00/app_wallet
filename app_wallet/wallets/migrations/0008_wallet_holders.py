# Generated by Django 4.2.4 on 2023-08-31 17:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('coins', '0001_initial'),
        ('wallets', '0007_alter_wallet_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='wallet',
            name='holders',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='coins.coin'),
        ),
    ]
