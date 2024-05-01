from django.db import models

class Vendor(models.Model):
    id = models.AutoField(primary_key=True, db_index=True, db_column='id')
    vendorCode = models.CharField(max_length=20, unique=True, null=False)
    name = models.CharField(db_column='name', max_length=1000, null=True)
    contactDetails = models.TextField(db_column='contact_details', null=True, blank=True)
    address = models.TextField(db_column='address', null=True, blank=True)
    onTimeDeliveryRate = models.FloatField(db_column='on_time_delivery_rate', default=0)
    qualityRatingAvg = models.FloatField(db_column='quality_rating_avg', default=0)
    averageResponseTime = models.FloatField(db_column='average_response_time', default=0)
    fulfillmentRate = models.FloatField(db_column='fulfillment_rate', default=0)

    def __str__(self):
        return self.name
    
class VendorPerformance(models.Model):
    id = models.AutoField(primary_key=True, db_index=True, db_column='id')
    vendor = models.ForeignKey(Vendor, db_column='vendor_id', null=True, on_delete=models.SET_NULL)
    date = models.DateTimeField(db_column='created_date')
    onTimeDeliveryRate = models.FloatField(db_column='on_time_delivery_rate', default=0)
    qualityRatingAvg = models.FloatField(db_column='quality_rating_avg', default=0)
    averageResponseTime = models.FloatField(db_column='average_response_time', default=0)
    fulfillmentRate = models.FloatField(db_column='fulfillment_rate', default=0)

    def __str__(self):
        return f"{self.vendor} - {self.date}"