from django.urls import path
from .views import main_view
from django.urls import path
from .views import main_view, logout_view 
from . import views 

urlpatterns = [
    path('', main_view, name='main'),
    path('logout/', logout_view, name='logout'),
    path('accounts/login/', views.login_view, name='login'),
    path('historial/', views.consultar_historial, name='consultar_historial'),
]