from rest_framework import serializers
from .models import Vendor
import time, base64

class VendorSerializer(serializers.ModelSerializer):
    vendorCode = serializers.CharField(read_only=True) 
    
    class Meta:
        model = Vendor
        fields = ['vendorCode', 'name', 'contactDetails', 'address'] 

    def create(self, validated_data):
        vendor_name = validated_data.get('name').replace(" ", "").lower()
        inserted_id = Vendor.objects.latest('id').id + 1 if Vendor.objects.exists() else 1
        timestamp = int(time.time())
        vendor_code = f"{vendor_name}#{inserted_id}#{timestamp}"
        vendor_code_base64 = base64.b64encode(vendor_code.encode()).decode() #unique code, can be decoded also
        validated_data['vendorCode'] = vendor_code_base64
        
        return super().create(validated_data)
