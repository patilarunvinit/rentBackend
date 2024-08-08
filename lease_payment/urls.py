from django.urls import path
from .views import leaseView, getleaseforrent
from . import views

urlpatterns = [
    path('addlease', leaseView.as_view()),
    path('getlease', getleaseforrent.as_view()),
    # path('getaddress', GetAddress.as_view()),


]