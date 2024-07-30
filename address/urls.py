from django.urls import path
from .views import AddressView
from . import views

urlpatterns = [
    path('addAddress', AddressView.as_view()),


]