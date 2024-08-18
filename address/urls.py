from django.urls import path
from .views import AddressView,GetAddress,Addressforleaseview,GetsingleAddress,Addressonleaseview,Addresscountview
from . import views

urlpatterns = [
    path('addAddress', AddressView.as_view()),
    path('getaddress', GetAddress.as_view()),
    path('getsingleaddress', GetsingleAddress.as_view()),
    path('addressforlease', Addressforleaseview.as_view()),
    path('addressonlease', Addressonleaseview.as_view()),
    path('addresscount', Addresscountview.as_view()),

]