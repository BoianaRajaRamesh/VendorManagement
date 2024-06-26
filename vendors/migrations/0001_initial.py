# Generated by Django 4.1 on 2024-05-01 06:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('id', models.AutoField(db_column='id', db_index=True, primary_key=True, serialize=False)),
                ('vendorCode', models.CharField(max_length=20, unique=True)),
                ('name', models.CharField(db_column='name', max_length=1000, null=True)),
                ('contactDetails', models.TextField(blank=True, db_column='contact_details', null=True)),
                ('address', models.TextField(blank=True, db_column='address', null=True)),
                ('onTimeDeliveryRate', models.FloatField(db_column='on_time_delivery_rate', default=0)),
                ('qualityRatingAvg', models.FloatField(db_column='quality_rating_avg', default=0)),
                ('averageResponseTime', models.FloatField(db_column='average_response_time', default=0)),
                ('fulfillmentRate', models.FloatField(db_column='fulfillment_rate', default=0)),
            ],
        ),
        migrations.CreateModel(
            name='VendorPerformance',
            fields=[
                ('id', models.AutoField(db_column='id', db_index=True, primary_key=True, serialize=False)),
                ('date', models.DateTimeField(db_column='created_date')),
                ('onTimeDeliveryRate', models.FloatField(db_column='on_time_delivery_rate', default=0)),
                ('qualityRatingAvg', models.FloatField(db_column='quality_rating_avg', default=0)),
                ('averageResponseTime', models.FloatField(db_column='average_response_time', default=0)),
                ('fulfillmentRate', models.FloatField(db_column='fulfillment_rate', default=0)),
                ('vendor', models.ForeignKey(db_column='vendor_id', null=True, on_delete=django.db.models.deletion.SET_NULL, to='vendors.vendor')),
            ],
        ),
    ]
