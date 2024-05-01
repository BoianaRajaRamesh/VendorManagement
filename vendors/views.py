from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Vendor
from .serializers import VendorSerializer
from django.http import Http404
from drf_yasg.utils import swagger_auto_schema

class AddVendor(APIView):
    @swagger_auto_schema(request_body=VendorSerializer)
    def post(self, request):
        serializer = VendorSerializer(data=request.data)
        if serializer.is_valid():
            vendor = serializer.save()
            # print(vendor.id)
            return Response({'status': 'success', 'message': 'Vendor added successfully', 'details': serializer.data},status=status.HTTP_201_CREATED)
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema()
    def get(self, request):
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
        
    @swagger_auto_schema()
    def get(self, request, vendor_id):
        vendor = self.get_object(vendor_id)
        serializer = VendorSerializer(vendor)
        return Response({'status': 'success', 'message': 'Vendors details', 'details':serializer.data}, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=VendorSerializer)
    def put(self, request, vendor_id):
        vendor = self.get_object(vendor_id)
        serializer = VendorSerializer(vendor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'success', 'message': 'Vendor details updated successfully', 'details': serializer.data},status=status.HTTP_200_OK)
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, vendor_id):
        vendor = self.get_object(vendor_id)
        vendor.status = 0
        vendor.save()
        # vendor.delete()
        return Response({'status': 'success', 'message': 'Vendor details deleted successfully'},status=status.HTTP_200_OK)