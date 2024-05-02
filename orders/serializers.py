from rest_framework import serializers
from .models import PurchaseOrder, STATUS
from vendors.models import Vendor
from django.utils import timezone
from datetime import timedelta

class ItemSerializer(serializers.Serializer):
    item_name = serializers.CharField()
    sku = serializers.CharField()
    price = serializers.IntegerField()

class PurchaseOrderSerializer(serializers.ModelSerializer):
    poNumber = serializers.CharField(read_only=True) 
    status = serializers.CharField(read_only=True)
    orderStatus = serializers.CharField(read_only=True)
    orderDate = serializers.CharField(read_only=True)
    # deliveryDate = serializers.CharField(read_only=True)
    completedDate = serializers.CharField(read_only=True)
    qualityRating = serializers.CharField(read_only=True)
    issueDate = serializers.CharField(read_only=True)
    acknowledgmentDate = serializers.CharField(read_only=True) 
    items = ItemSerializer(many=False)

    class Meta:
        model = PurchaseOrder
        fields = "__all__"

    def create(self, validated_data):
        delivery_date = validated_data.get('deliveryDate')
        if delivery_date < (timezone.now() + timedelta(days=2)):
            raise serializers.ValidationError("Delivery date must be at least 2 days from today.")
        
        validated_data['orderStatus'] = 'pending'
        validated_data['poNumber'] = timezone.now()
        return super().create(validated_data)

class ManagePurchaseOrderSerializer(serializers.ModelSerializer):
    completedDate = serializers.CharField(read_only=True)
    class Meta:
        model = PurchaseOrder
        fields = ['orderStatus', 'qualityRating', 'completedDate'] 
