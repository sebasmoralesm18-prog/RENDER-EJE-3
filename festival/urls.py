from django.urls import path
from . import views

urlpatterns = [
    path('inicio/', views.inicio, name='inicio'),
    path('', views.index, name='index'),
    path('registro/', views.registro, name='registro'),
    path('login/', views.login, name='login'),
    path('logout/',views.logout,name='logout'),

    path('categorias/',views.categorias_votacion,name='categorias_votacion'),
    path('votar/<int:categoria_id>/',views.votar,name='votar'),
    path('mis-votos/', views.mis_votos,name='mis_votos'),
    path('resultados/',views.resultados,name='resultados'),

    path('panel-administrativo/',views.panel_administrativo,name='panel_administrativo'),
    path('administrar-categorias/',views.administrar_categorias,name='administrar_categorias'),
    path('crear-categoria/',views.crear_categoria,name='crear_categoria'),
    path('editar-categoria/<int:id>/',views.editar_categoria,name='editar_categoria'),
    path('eliminar-categoria/<int:id>/',views.eliminar_categoria,name='eliminar_categoria'),
    path('cambiar-estado-categoria/<int:id>/',views.cambiar_estado_categoria,name='cambiar_estado_categoria'),

    path('administrar-ediciones/',views.administrar_ediciones,name='administrar_ediciones'),
    path('crear-edicion/',views.crear_edicion,name='crear_edicion'),
    path('editar-edicion/<int:id>/',views.editar_edicion,name='editar_edicion'),
    path('cambiar-estado-edicion/<int:id>/',views.cambiar_estado_edicion,name='cambiar_estado_edicion'),

    path('administrar-opciones/', views.administrar_opciones, name='administrar_opciones'),
    path('crear-opcion/', views.crear_opcion, name='crear_opcion'),
    path('editar-opcion/<int:id>/', views.editar_opcion, name='editar_opcion'),
    path('eliminar-opcion/<int:id>/', views.eliminar_opcion, name='eliminar_opcion'),

    path('resultados-administrativos/',views.resultados_administrativos,name='resultados_administrativos'),

    path('api/categorias/',views.api_categorias,name='api_categorias'),   
]

