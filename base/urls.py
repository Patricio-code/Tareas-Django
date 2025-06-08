from django.urls import path
#from . import views
from .views import ListaPendientes, DetalleTarea, CrearTarea, EditarTarea, EliminarTaea, Logueo, DesLogueo, PaginaRegistro
#from django.contrib.auth.views import LogoutView
urlpatterns = [path('',ListaPendientes.as_view(), name = 'pendientes'),
               path('login/',Logueo.as_view(), name='login'),
               path('logout/',DesLogueo.as_view(), name='logout'),
               path('registro/',PaginaRegistro.as_view(), name='registro'),
               path('tareas/<int:pk>',DetalleTarea.as_view(), name = 'tareas'),
               path('crear-tarea/',CrearTarea.as_view(), name = 'crear-tarea'),
               path('editar-tarea/<int:pk>',EditarTarea.as_view(), name = 'editar-tarea'),
               path('eliminar-tarea/<int:pk>',EliminarTaea.as_view(), name = 'eliminar-tarea')]

#.as_view() sirve para que se puedan mostrar clases