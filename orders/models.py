from django.db import models
from vendors.models import Vendor

STATUS = (
    ('pending', 'PENDING'),
    ('completed', 'COMPLETED'),
    ('canceled', 'CANCELED'),
)

class PurchaseOrder(models.Model):
    id = models.AutoField(primary_key=True, db_index=True, db_column='id')
    poNumber = models.CharField(max_length=100, db_column='po_number', unique=True)
    vendor = models.ForeignKey(Vendor, db_column='vendor_id', null=True, on_delete=models.SET_NULL)
    orderDate = models.DateTimeField(db_column='order_date')
    deliveryDate = models.DateTimeField(db_column='delivery_date')
    items = models.JSONField(db_column='items')
    quantity = models.IntegerField(db_column='quantity', null=False, default=0)
    status = models.CharField(max_length=20, choices=STATUS, db_column='status', default='pending')
    qualityRating = models.FloatField(db_column='quality_rating',null=True, blank=True)
    issueDate = models.DateTimeField(db_column='issue_date')
    acknowledgmentDate = models.DateTimeField(db_column='acknowledgment_date',null=True, blank=True)

    def __str__(self):
        return self.po_number
