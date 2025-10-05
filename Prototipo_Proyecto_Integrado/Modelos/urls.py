from django.urls import path
from . import views

urlpatterns = [
    path('agregar/',views.crear_registro,name='crear_registro'),
    path('funciona/',views.funciona,name='registro_exitoso'),
    path('ver_pedidos/', views.ver_pedidos, name='ver_pedidos'),
    path('editar_pedido/<int:n_orden>/', views.editar_pedido, name='editar_pedido'),
    path('eliminar_pedido/<int:n_orden>/', views.eliminar_pedido, name='eliminar_pedido'),
    path('registrar_otros/', views.registrar_otros,name='registrar_otros'),
    path('registrar_cliente/', views.registrar_cliente, name='registrar_cliente'),
    path('registrar_dispositivo/', views.registrar_dispositivo, name='registrar_dispositivo'),
    path('registrar_modelo/', views.registrar_modelo, name='registrar_modelo'),
    path('registrar_marca/', views.registrar_marca, name='registrar_marca'),
    path('ver_otros/',views.ver_otros,name="ver_otros"),
    path('ver_clientes/', views.ver_clientes, name='ver_clientes'),
    path('ver_dispositivos/', views.ver_dispositivos, name='ver_dispositivos'),
    path('ver_modelos/', views.ver_modelos, name='ver_modelos'),
    path('ver_marcas/', views.ver_marcas, name='ver_marcas'),
    path('ver_clientes/', views.ver_clientes, name='ver_clientes'),
    path('ver_dispositivos/', views.ver_dispositivos, name='ver_dispositivos'),
    path('ver_modelos/', views.ver_modelos, name='ver_modelos'),
    path('ver_marcas/', views.ver_marcas, name='ver_marcas'),
    path('editar_cliente/<int:pk>/', views.editar_cliente, name='editar_cliente'),
    path('editar_dispositivo/<int:pk>/', views.editar_dispositivo, name='editar_dispositivo'),
    path('editar_modelo/<int:pk>/', views.editar_modelo, name='editar_modelo'),
    path('editar_marca/<int:pk>/', views.editar_marca, name='editar_marca'),
    path('eliminar_cliente/<int:pk>/', views.eliminar_cliente, name='eliminar_cliente'),
    path('eliminar_dispositivo/<int:pk>/', views.eliminar_dispositivo, name='eliminar_dispositivo'),
    path('eliminar_modelo/<int:pk>/',views.eliminar_modelo, name='eliminar_modelo'),
    path('eliminar_marca/<int:pk>/',views.eliminar_marca,name='eliminar_marca')
]