# Generated by Django 3.0.8 on 2020-12-27 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('uniqlo', '0013_material_m_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='o_quantity',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=8),
        ),
    ]
