from django.urls import path
from .views import RegisterView,LoginView,UserView,LogoutView,AccessRefreshView
from . import views

urlpatterns = [
    path('register', RegisterView.as_view()),
    path('login', LoginView.as_view()),
    path('user', UserView.as_view()),
    path('refresh', AccessRefreshView.as_view()),
    path('logout', LogoutView.as_view()),
    path('test',views.testget),

]