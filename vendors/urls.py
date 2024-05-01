from django.urls import path
from .views import AddVendor, ManageVendor

urlpatterns = [
    path('api/vendors', AddVendor.as_view(), name='vendor-detail-adding'),
    path('api/vendors/<int:vendor_id>', ManageVendor.as_view(), name='manage-vendor-detail'),
]