# Generated by Django 4.1 on 2024-05-02 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendors', '0003_alter_vendorperformance_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendor',
            name='vendorCode',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
