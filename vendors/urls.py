from django.urls import path
from .views import AddVendor, ManageVendor, Performance

urlpatterns = [
    path('api/vendors', AddVendor.as_view(), name='vendor-detail-adding'),
    path('api/vendors/<int:vendor_id>', ManageVendor.as_view(), name='manage-vendor-detail'),
    path('api/vendors/<int:vendor_id>/performance', Performance.as_view(), name='performance'),
]