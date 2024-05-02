from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import PurchaseOrder
from vendors.models import Vendor
from .serializers import PurchaseOrderSerializer, ManagePurchaseOrderSerializer
from django.http import Http404
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.utils import timezone
from utils import check_token

class Orders(APIView):
    @swagger_auto_schema(request_body=PurchaseOrderSerializer)
    def post(self, request):
        check_token(request)
        serializer = PurchaseOrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'success', 'message': 'Order created successfully', 'details': serializer.data},status=status.HTTP_201_CREATED)
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
    @swagger_auto_schema(manual_parameters=[
        openapi.Parameter('vendor_id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, required=False, description='Vendor ID (optional)'),
        openapi.Parameter('order_id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, required=False, description='Order ID (optional)')
    ])
    def get(self, request):
        check_token(request)
        vendor_id = request.query_params.get('vendor_id')
        order_id = request.query_params.get('order_id')
        if vendor_id is not None:
            try:
                vendor = Vendor.objects.filter(status = 1,id=vendor_id).get()
                pos = PurchaseOrder.objects.filter(vendor=vendor)
            except Vendor.DoesNotExist:
                raise Http404("Vendor details not found")
        elif order_id is not None:
            pos = PurchaseOrder.objects.filter(status = 1,id=order_id)
        else:
            pos = PurchaseOrder.objects.filter(status = 1).all()
        total_count = pos.count()
        serialized_pos = PurchaseOrderSerializer(pos, many=True)
        return Response({'status': 'success', 'message': 'Orders list', 'total_count': total_count, 'list': serialized_pos.data}, status=status.HTTP_200_OK)

class ManageOrders(APIView):
    
    def get_object(self, pk):
        try:
            return PurchaseOrder.objects.filter(status = 1, pk=pk).get()
        except PurchaseOrder.DoesNotExist:
            raise Http404("Order details not found")
        
    @swagger_auto_schema(request_body=ManagePurchaseOrderSerializer)
    def put(self, request, order_id):
        check_token(request)
        order = self.get_object(order_id)
        serializer = ManagePurchaseOrderSerializer(order, data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            if validated_data['orderStatus'] == 'completed':
                validated_data['completedDate'] = timezone.now()
            serializer.save()
            return Response({'status': 'success', 'message': 'Order details updated successfully', 'details': serializer.data}, status=status.HTTP_200_OK)
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema()
    def delete(self, request, order_id):
        check_token(request)
        po = self.get_object(order_id)
        po.status = 0
        po.save()
        # po.delete()
        return Response({'status': 'success', 'message': 'Order deleted successfully'},status=status.HTTP_200_OK)
    
class Acknowledgement(APIView):
    @swagger_auto_schema()
    def post(self, request, order_id):
        check_token(request)
        order = PurchaseOrder.objects.filter(status = 1,pk=order_id).get()
        if order:
            order.acknowledgmentDate = timezone.now()
            order.save()
            return Response({'status': 'success', 'message': 'Order acknowledged successfully'},status=status.HTTP_200_OK)
        return Response({'error': "Order not found"}, status=status.HTTP_400_BAD_REQUEST)
        

