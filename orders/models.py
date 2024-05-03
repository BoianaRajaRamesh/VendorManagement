from django.db import models
from vendors.models import Vendor, VendorPerformance
from django.utils import timezone

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import F, Sum, Avg, ExpressionWrapper, DurationField
from django.db.models.functions import Coalesce
from datetime import date

STATUS = (
    ('pending', 'PENDING'),
    ('completed', 'COMPLETED'),
    ('canceled', 'CANCELED'),
)

class PurchaseOrder(models.Model):
    id = models.AutoField(primary_key=True, db_index=True, db_column='id')
    poNumber = models.CharField(max_length=100, db_column='po_number', unique=True)
    vendor = models.ForeignKey(Vendor, db_column='vendor_id', null=True, on_delete=models.SET_NULL)
    orderDate = models.DateTimeField(db_column='order_date', default=timezone.now)
    deliveryDate = models.DateTimeField(db_column='delivery_date', null=True)#Expected delivery date
    completedDate = models.DateTimeField(db_column='completed_date', null=True)#order completed date to calculate On-Time Delivery Rate:
    items = models.JSONField(db_column='items', null=True)
    quantity = models.IntegerField(db_column='quantity', null=False, default=0)
    orderStatus = models.CharField(max_length=20, choices=STATUS, db_column='order_status', default='pending')
    qualityRating = models.FloatField(db_column='quality_rating',null=True, blank=True)
    issueDate = models.DateTimeField(db_column='issue_date', null=True, default=timezone.now)
    acknowledgmentDate = models.DateTimeField(db_column='acknowledgment_date',null=True, blank=True)
    status = models.IntegerField(db_column='status', default=1)

    def __str__(self):
        return self.po_number


@receiver(post_save, sender=PurchaseOrder)
def update_vendor_data(sender, instance, created, **kwargs):    
    vendor = instance.vendor
    today = timezone.now().date()
    vendor_performance, _ = VendorPerformance.objects.get_or_create(vendor=vendor, date=today)
    # On-Time Delivery Rate
    completed_orders = PurchaseOrder.objects.filter(vendor=vendor, status = 1, orderStatus='completed')
    total_completed_orders = completed_orders.count()
    if total_completed_orders > 0:
        on_time_delivered_orders = completed_orders.filter(deliveryDate__gt=F('completedDate')).count()
        on_time_delivered_orders = on_time_delivered_orders if on_time_delivered_orders > 0 else 0
        onTimeDeliveryRate = round(on_time_delivered_orders / total_completed_orders ,2)
    else:
        onTimeDeliveryRate = 0
    vendor.onTimeDeliveryRate = onTimeDeliveryRate

    # Quality Rating Average
    total_quality_rating = completed_orders.filter(qualityRating__isnull=False).aggregate(total_quality_rating=Avg('qualityRating'))['total_quality_rating']
    if total_quality_rating is not None and total_quality_rating > 0:
        qualityRatingAvg = round(total_quality_rating , 2)
    else:
        qualityRatingAvg = 0
    vendor.qualityRatingAvg = qualityRatingAvg

    # Fulfillment Rate
    total_orders = PurchaseOrder.objects.filter(status = 1, vendor=vendor).count()
    if total_orders > 0:
        successful_orders = completed_orders.count()
        successful_orders = successful_orders if successful_orders > 0 else 0
        fulfillmentRate = round(successful_orders / total_orders ,2)
    else:
        fulfillmentRate = 0
    vendor.fulfillmentRate = fulfillmentRate

    average_time_difference = PurchaseOrder.objects.filter(status = 1, vendor=vendor).aggregate(
                    avg_time_difference=Avg(
                        ExpressionWrapper(
                            F('acknowledgmentDate') - F('issueDate'),
                            output_field=DurationField()
                        )
                    )
                )['avg_time_difference']
    if average_time_difference is not None:
        average_time_difference_seconds = average_time_difference.total_seconds()
        average_time_difference = round(average_time_difference_seconds, 2)
    else:
        average_time_difference = 0
    vendor.averageResponseTime = average_time_difference
    vendor.save()# Update Vendor changes
    
    vendor_performance.onTimeDeliveryRate = onTimeDeliveryRate
    vendor_performance.qualityRatingAvg = qualityRatingAvg
    vendor_performance.fulfillmentRate = fulfillmentRate
    vendor_performance.averageResponseTime = average_time_difference
    vendor_performance.save()
    
        