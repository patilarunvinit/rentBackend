from django.urls import path
from .views import leaseView, getleaseforrent,getmonths, PaymentView,testview,getremiain,getremianhistory,RemainPayView,getremovedata,removeleaseView
from . import views

urlpatterns = [
    path('addpayment', PaymentView.as_view()),
    path('addremain', RemainPayView.as_view()),
    path('addlease', leaseView.as_view()),
    path('removelease', removeleaseView.as_view()),
    path('getlease', getleaseforrent.as_view()),
    path('getmonths', getmonths.as_view()),
    path('getremain', getremiain.as_view()),
    path('remianhistory', getremianhistory.as_view()),
    path('getremovedata', getremovedata.as_view()),
    path('test123', testview.as_view()),


]