from django.shortcuts import render, redirect
from .models import Tareas
"""
Esto era para generar una respuesta http
from django.http import HttpResponse

def lista_pendientes(pedido):
    return HttpResponse('Lista de pendientes')"""

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin

class Logueo(LoginView):
    template_name = "base/login.html"
    field = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('pendientes')

class PaginaRegistro(FormView):
    template_name = 'base/registro.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('pendientes')

    def form_valid(self, form):
        usuario = form.save()
        if usuario is not None:
            login(self.request, usuario)
        return super(PaginaRegistro, self).form_valid(form)
    
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated: 
            return redirect('pendientes')
        return super(PaginaRegistro, self).get(*args,**kwargs)

class DesLogueo(LoginRequiredMixin,LogoutView):
    template_name = "base/logout.html"
    field = '__all__'
    next_page = reverse_lazy('login')

class ListaPendientes(LoginRequiredMixin,ListView):
    model = Tareas
    context_object_name = 'tareas'

    """
    Esto lo usé xq no habia cambiado object_list por tareas en tareas_html
    def get_queryset(self):
        return Tareas.objects.filter(usuario=self.request.user)"""

    def get_context_data(self, **kwarg):
        context = super().get_context_data(**kwarg)
        context['tareas'] = context['tareas'].filter(usuario=self.request.user)
        context['count'] = context['tareas'].filter(completo=False).count()

        valor_buscado = self.request.GET.get('area-buscar') or ''
        if valor_buscado:
            context['tareas'] = context['tareas'].filter(titulo__icontains = valor_buscado)
        
        context['valor_buscado'] = valor_buscado
        return context

class DetalleTarea(LoginRequiredMixin,DetailView):
    model = Tareas
    context_object_name = 'tarea'
    template_name = 'base/tarea_detalles.html'

class CrearTarea(LoginRequiredMixin,CreateView):
    model = Tareas
    fields =['titulo', 'descripcion', 'completo']
    # usuario lo saco de la lista porque lo asigno automaticamente con la funcion de mas abajo
    # podria haber puesto fields = '__all__' y crea el formulario para todos los campos de la clase Tareas
    # lo que sigue es para volver a una url sin que el ususario deba hacerlo manualmente
    success_url = reverse_lazy('pendientes')

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super(CrearTarea, self).form_valid(form)

class EditarTarea(LoginRequiredMixin,UpdateView):
    model = Tareas
    fields =['titulo', 'descripcion', 'completo']
    success_url = reverse_lazy('pendientes')

class EliminarTaea(LoginRequiredMixin,DeleteView):
    model = Tareas
    context_object_name = 'tarea'
    success_url = reverse_lazy('pendientes')