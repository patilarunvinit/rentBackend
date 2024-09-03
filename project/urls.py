from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('owner.urls')),
    path('', include('address.urls')),
    path('', include('renter.urls')),
    path('', include('lease_payment.urls')),
    path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),

]+ static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)

