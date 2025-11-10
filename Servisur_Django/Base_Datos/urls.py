from django.urls import path
from . import views

urlpatterns = [
    #  Navegación principal
    path('', views.main_view, name='main'),
    path('logout/', views.logout_view, name='logout'),
    path('accounts/login/', views.login_view, name='login'),

    #  Registro y gestión de reparaciones
    path('registrar/', views.registrar_reparacion, name='registrar_reparacion'),
    path('estado/', views.estado_reparacion_view, name='estado_reparacion'),
    path('historial/', views.consultar_historial, name='consultar_historial'),

    #  Generación de documentos
    path('generar-documento/', views.generar_documento_view, name='generar_documento'),
    path('generar-excel/', views.generar_excel_view, name='generar_excel'),
    #  Carga dinámica
    path('obtener_modelos_por_marca/', views.obtener_modelos_por_marca, name='obtener_modelos_por_marca'),
    path("obtener_tipos_falla/", views.obtener_tipos_falla, name="obtener_tipos_falla"),

    #  Creación dinámica
    path('agregar_modelo_ajax/', views.agregar_modelo_ajax, name='agregar_modelo_ajax'),
    path('agregar_marca_ajax/', views.agregar_marca_ajax, name='agregar_marca_ajax'),
    path("agregar_falla_ajax/", views.agregar_falla_ajax, name="agregar_falla_ajax"),
]
