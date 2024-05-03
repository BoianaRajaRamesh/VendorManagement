from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Vendor
from .serializers import VendorSerializer
from django.http import Http404
from drf_yasg.utils import swagger_auto_schema
from utils import check_token

class AddVendor(APIView):
    @swagger_auto_schema(request_body=VendorSerializer, operation_description="This API endpoint allows you to add a new vendor to the system.")
    def post(self, request):
        check_token(request)
        serializer = VendorSerializer(data=request.data)
        if serializer.is_valid():
            vendor = serializer.save()
            # print(vendor.id)
            return Response({'status': 'success', 'message': 'Vendor added successfully', 'details': serializer.data},status=status.HTTP_201_CREATED)
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(operation_description="This API endpoint retrieves a list of active vendors. Upon successful retrieval, it returns a list of vendors along with the total count of active vendors.If there are no active vendors, an empty list is returned.")
    def get(self, request):
        check_token(request)
        vendors = Vendor.objects.filter(status=1).all()
        total_count = vendors.count()  
        serialized_vendors = VendorSerializer(vendors, many=True)
        return Response({'status': 'success', 'message': 'Vendors list', 'total_count':total_count, 'list':serialized_vendors.data}, status=status.HTTP_200_OK)


class ManageVendor(APIView):
    def get_object(self, pk):
        try:
            return Vendor.objects.filter(status=1, pk=pk).get()
        except Vendor.DoesNotExist:
            raise Http404("Vendor details not found")
        
    @swagger_auto_schema(operation_description="This API endpoint retrieves details of a specific vendor identified by vendor_id. It returns the details of the specified vendor along with a success message. If the specified vendor does not exist, an error message is returned.")
    def get(self, request, vendor_id):
        check_token(request)
        vendor = self.get_object(vendor_id)
        serializer = VendorSerializer(vendor)
        return Response({'status': 'success', 'message': 'Vendors details', 'details':serializer.data}, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=VendorSerializer, operation_description="This endpoint updates the details of a specific vendor identified by vendor_id. If there are validation errors in the request data, it returns an error message with details of the validation errors.<br> <b>Note:</b> Vendorcode is unique and it will not update")
    def put(self, request, vendor_id):
        check_token(request)
        vendor = self.get_object(vendor_id)
        serializer = VendorSerializer(vendor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'success', 'message': 'Vendor details updated successfully', 'details': serializer.data},status=status.HTTP_200_OK)
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(operation_description="This API endpoint deactivates the details of a specific vendor identified by vendor_id. Instead of deleting, it disables the vendor by updating its status field.")
    def delete(self, request, vendor_id):
        check_token(request)
        vendor = self.get_object(vendor_id)
        vendor.status = 0
        vendor.save()
        # vendor.delete()
        return Response({'status': 'success', 'message': 'Vendor details deleted successfully'},status=status.HTTP_200_OK)
    
class Performance(APIView):
    @swagger_auto_schema(operation_description="This API endpoint retrieves performance data for a specific vendor using vendor_id. <br><br /><b>On Time Delivery Rate:</b> Rate of on-time delivery for the vendor. <br><b>Quality Rating Avg:</b> Average quality rating of the vendor. <br><b>Average Response Time:</b> Average response time of the vendor. <br><b>Fulfillment Rate:</b> Rate of fulfillment for the vendor.<br> <br />If the vendor is not found, it returns an error message.")
    def get(self, request, vendor_id):
        check_token(request)
        vendor = Vendor.objects.filter(pk=vendor_id).get()
        if vendor:
            performance_data = {
                'onTimeDeliveryRate': vendor.onTimeDeliveryRate,
                'qualityRatingAvg': vendor.qualityRatingAvg,
                'averageResponseTime': vendor.averageResponseTime,
                'fulfillmentRate': vendor.fulfillmentRate
            }
            return Response({'status': 'success', 'message': 'Performance data', 'details':performance_data},status=status.HTTP_200_OK)
        return Response({'error': "Vendor not found"}, status=status.HTTP_400_BAD_REQUEST)