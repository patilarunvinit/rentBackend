from django.urls import path
from .views import AddressView,GetAddress
from . import views

urlpatterns = [
    path('addAddress', AddressView.as_view()),
    path('getaddress', GetAddress.as_view()),


]