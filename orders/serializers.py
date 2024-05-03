from rest_framework import serializers
from .models import PurchaseOrder, STATUS
from vendors.models import Vendor
from django.utils import timezone
from datetime import timedelta

class ItemSerializer(serializers.Serializer):
    item_name = serializers.CharField(required=True)
    price = serializers.IntegerField(required=True, min_value=1)

class SavePurchaseOrderSerializer(serializers.ModelSerializer):
    quantity = serializers.IntegerField(required=True, min_value=1)
    orderStatus = serializers.CharField(read_only=True)
    items = ItemSerializer(many=False)

    class Meta:
        model = PurchaseOrder
        fields = ['vendor', 'quantity', 'items', 'orderStatus']

    def create(self, validated_data):
        validated_data['orderStatus'] = 'pending'
        validated_data['poNumber'] = timezone.now()
        order = super().create(validated_data)
        return order.id
    
class PurchaseOrderSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=False)
    class Meta:
        model = PurchaseOrder
        fields = "__all__"

class PurchaseOrderDeliveryDateSerializer(serializers.ModelSerializer):
    deliveryDate = serializers.DateTimeField(required=True)
    class Meta:
        model = PurchaseOrder
        fields = ['deliveryDate']

    
class ManagePurchaseOrderSerializer(serializers.ModelSerializer):
    completedDate = serializers.DateTimeField(read_only=True)
    orderStatus = serializers.ChoiceField(required=True, choices=STATUS)
    qualityRating = serializers.FloatField(required=True, min_value=0.5, max_value=5.0)
    class Meta:
        model = PurchaseOrder
        fields = ['orderStatus', 'qualityRating', 'completedDate'] 
