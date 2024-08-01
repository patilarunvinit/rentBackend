from django.urls import path
from .views import leaseView
from . import views

urlpatterns = [
    path('addlease', leaseView.as_view()),
    # path('getaddress', GetAddress.as_view()),


]