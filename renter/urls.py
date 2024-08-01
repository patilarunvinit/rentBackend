from django.urls import path
from .views import renterView, renterforleaseview
from . import views

urlpatterns = [
    path('addrenter', renterView.as_view()),
    # path('getaddress', GetAddress.as_view()),
    path('renterforlease', renterforleaseview.as_view()),


]