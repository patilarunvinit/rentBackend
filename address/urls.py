from django.urls import path
from .views import AddressView,GetAddress,Addressforleaseview
from . import views

urlpatterns = [
    path('addAddress', AddressView.as_view()),
    path('getaddress', GetAddress.as_view()),
    path('addressforlease', Addressforleaseview.as_view()),


]