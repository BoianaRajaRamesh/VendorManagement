from django.urls import path
from .views import  ManageOrders, Orders, Acknowledgement

urlpatterns = [
    path('api/purchase_orders/<int:order_id>', ManageOrders.as_view(), name='manage-order-detail'),
    path('api/purchase_orders', Orders.as_view(), name='manage-order-detail'),
    path('api/purchase_orders/<int:order_id>/acknowledge', Acknowledgement.as_view(), name='acknowledge-purchase-order'),
]