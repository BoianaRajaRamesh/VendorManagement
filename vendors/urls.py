from django.urls import path
from .views import VendorDetail

urlpatterns = [
    path('api/vendors', VendorDetail.as_view(), name='vendor-detail'),
]