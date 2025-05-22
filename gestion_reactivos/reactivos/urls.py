from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Página principal: inventario de lotes
    path('reactivos/', views.lista_codigos, name='lista_codigos'),  # Tabla base de códigos
    path('reactivos/nuevo/', views.nuevo_reactivo, name='nuevo_reactivo'),  # Alta de código base
    path('reactivos/eliminar/<int:pk>/', views.eliminar_reactivo, name='eliminar_reactivo'),  # Baja de código base
    path('codigos/editar/<int:pk>/', views.editar_reactivo, name='editar_reactivo'),

    # path('lotes/', views.lista_lotes, name='lista_lotes'),  # Listado de lotes (opcional si usas home)
    # path('caducidades/', views.lista_caducidades, name='lista_caducidades'),  # Lista de caducidades por categoría

    # RUTAS PARA EDITAR Y ELIMINAR LOTES
    path('lotes/editar/<int:pk>/', views.editar_lote, name='editar_lote'),
    path('lotes/eliminar/<int:pk>/', views.eliminar_lote, name='eliminar_lote'),
    path('lotes/nuevo/', views.nuevo_lote, name='nuevo_lote'),  # Nueva ruta para alta de lote

    # Nueva ruta para pedidos
    path('pedidos/', views.lista_pedidos, name='lista_pedidos'),
    path('pedidos/nuevo/', views.nuevo_pedido, name='nuevo_pedido'),
    path('pedidos/<int:pk>/editar/', views.editar_pedido, name='editar_pedido'),

    # Nuevas rutas para salidas
    path('salidas/', views.lista_salidas, name='lista_salidas'),
    path('salidas/nueva/', views.nueva_salida, name='nueva_salida'),
    path('salidas/editar/<int:pk>/', views.editar_salida, name='editar_salida'),
    path('salidas/eliminar/<int:pk>/', views.eliminar_salida, name='eliminar_salida'),

    # Nueva ruta para categorías
    path('categorias/', views.lista_categorias, name='lista_categorias'),
    path('categorias/nueva/', views.nueva_categoria, name='nueva_categoria'),
]






