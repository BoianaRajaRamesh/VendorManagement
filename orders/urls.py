from django.urls import path
from .views import  ManageOrders, Orders, Acknowledgement, QualityRating

urlpatterns = [
    path('api/purchase_orders/<int:order_id>', ManageOrders.as_view(), name='manage-order-detail'),
    path('api/purchase_orders', Orders.as_view(), name='manage-order-detail'),
    path('api/purchase_orders/<int:order_id>/acknowledge', Acknowledgement.as_view(), name='acknowledge-purchase-order'),
    path('api/purchase_orders/<int:order_id>/rating', QualityRating.as_view(), name='QualityRating-purchase-order'),
]