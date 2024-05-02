# Generated by Django 4.1 on 2024-05-02 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_purchaseorder_completeddate'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchaseorder',
            name='orderStatus',
            field=models.CharField(choices=[('pending', 'PENDING'), ('completed', 'COMPLETED'), ('canceled', 'CANCELED')], db_column='order_status', default='pending', max_length=20),
        ),
        migrations.AlterField(
            model_name='purchaseorder',
            name='status',
            field=models.IntegerField(db_column='status', default=1),
        ),
    ]