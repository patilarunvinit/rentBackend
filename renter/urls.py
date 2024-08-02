from django.urls import path
from .views import renterView, renterforleaseview,Getrenterifonlease
from . import views

urlpatterns = [
    path('addrenter', renterView.as_view()),
    # path('getaddress', GetAddress.as_view()),
    path('renterforlease', renterforleaseview.as_view()),
    path('Getrenterifonlease', Getrenterifonlease.as_view()),


]