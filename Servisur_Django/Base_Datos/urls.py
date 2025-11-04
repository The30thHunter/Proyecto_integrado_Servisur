from django.urls import path
from .views import main_view

from .views import main_view, logout_view 
from . import views 
from .views import registrar_reparacion_view, estado_reparacion_view, generar_documento_view, generar_excel_view


urlpatterns = [
    path('', main_view, name='main'),
    path('logout/', logout_view, name='logout'),
    path('accounts/login/', views.login_view, name='login'),
    path('historial/', views.consultar_historial, name='consultar_historial'),
    path('registrar/', registrar_reparacion_view, name='registrar_reparacion'),
    path('estado/', estado_reparacion_view, name='estado_reparacion'),
    path('generar-documento/', generar_documento_view, name='generar_documento'),
    path('generar-excel/', generar_excel_view, name='generar_excel'),

]