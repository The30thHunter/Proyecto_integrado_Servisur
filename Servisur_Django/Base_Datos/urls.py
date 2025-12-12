from django.urls import path
from . import views
from .views import cambiar_grupo_view
from .views import toggle_usuario_view
from .views import cambiar_contrasena_view

urlpatterns = [
    #  Navegación principal
    path('', views.main_view, name='main'),
    path('accounts/login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

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
    
    path('reparacion/<int:orden_id>/editar/', views.editar_reparacion_view, name='editar_reparacion'),
    path('reparacion/<int:orden_id>/json/', views.pedido_json_view, name='pedido_json'),
    path('reparacion/<int:orden_id>/actualizar/', views.pedido_actualizar_view, name='pedido_actualizar'),
    # alias para AJAX que usan scripts antiguos o externos
    path('ajax/modelos/', views.obtener_modelos_por_marca, name='ajax_modelos'),
    path('ajax/tipos_falla/', views.obtener_tipos_falla, name='ajax_tipos_falla'),
    #ruta de impresion
    path('imprimir-ticket/', views.imprimir_ticket_view, name='imprimir_ticket'),

    path('gestionar_cuentas/', views.gestionar_cuentas_view, name='gestionar_cuentas'),
    path('activar_usuario/<int:user_id>/', views.activar_usuario_view, name='activar_usuario'),
    path('desactivar_usuario/<int:user_id>/', views.desactivar_usuario_view, name='desactivar_usuario'),
    path('crear_usuario/', views.crear_usuario_view, name='crear_usuario'),
    path('usuarios/<int:user_id>/cambiar-grupo/', cambiar_grupo_view, name='cambiar_grupo'),
    path('usuarios/<int:user_id>/toggle/', toggle_usuario_view, name='toggle_usuario'),
    path('cambiar_contrasena/<int:user_id>/', views.cambiar_contrasena_view, name='cambiar_contrasena'),

    path('boleta/pdf/<int:pk>/', views.generar_boleta_pdf, name='boleta_pdf'),
]
