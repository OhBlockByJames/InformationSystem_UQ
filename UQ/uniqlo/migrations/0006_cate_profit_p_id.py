# Generated by Django 3.0.8 on 2020-12-27 14:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('uniqlo', '0005_auto_20201227_2137'),
    ]

    operations = [
        migrations.AddField(
            model_name='cate_profit',
            name='p_id',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='uniqlo.Product'),
            preserve_default=False,
        ),
    ]
