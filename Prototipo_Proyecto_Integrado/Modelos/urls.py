from django.urls import path
from . import views

urlpatterns = [
    path('agregar/',views.crear_registro,name='crear_registro'),
    path('funciona/',views.funciona,name='registro_exitoso')
]