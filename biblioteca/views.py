from datetime import datetime
from typing import Any
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from .models import Libro, Prestamo, Autor, Editorial
from django.views import View
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin



class Libro_list(LoginRequiredMixin, ListView):
    model = Libro
    template_name="biblioteca/lista.html"
    #queryset=Libro.objects.filter(disponibilidad="disponible")
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['autores'] = Autor.objects.all()
        #Recojo todos los generos
        generosLibro = []
        for libro in Libro.objects.all() :
            if libro.genero not in generosLibro:
                generosLibro.append(libro.genero)
        context['generosLibro'] = generosLibro
        context['editoriales'] = Editorial.objects.all()
        #Recojo los filtros seleccionados por el usuario
        a = self.request.GET.get('autor')
        g = self.request.GET.get('genero')
        e = self.request.GET.get('editorial')

        #Filtramos por disponibles y prestados
        context['libros_disponibles'] = Libro.objects.filter(disponibilidad="disponible")
        context['libros_prestados'] = Libro.objects.filter(disponibilidad="prestado")

        #Cambios de context
        if a != "all" and a != None:
            autor = Autor.objects.get(nombre=a)
            context['libros_disponibles']= context['libros_disponibles'].filter(autor=autor)
            context['libros_prestados'] = context['libros_prestados'].filter(autor=autor)
        
        if g != "all" and g != None:
            context['libros_disponibles']= context['libros_disponibles'].filter(genero=g)
            context['libros_prestados']=context['libros_prestados'].filter(genero=g)

        if e != "all" and e != None:
            context['libros_disponibles']= context['libros_disponibles'].filter(editorial=e)
            context['libros_prestados']=context['libros_prestados'].filter(editorial=e)
            
        return context

class Book_list_prestados(LoginRequiredMixin, ListView):
    model = Prestamo
    template_name="biblioteca/lista_prestado.html"
    #queryset=Libro.objects.filter(disponibilidad="disponible")
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['usuario'] = self.request.user
        context['prestamos'] = Prestamo.objects.filter(estadoPrestamo="prestado")
        context['historialPrestamos'] = Prestamo.objects.filter(estadoPrestamo="disponible")
        return context

class Book_list_disponibles(LoginRequiredMixin, ListView):
    model = Libro
    template_name="biblioteca/lista_disponible.html"
    #queryset=Libro.objects.filter(disponibilidad="disponible")
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['libros_disponibles'] = Libro.objects.filter(disponibilidad="disponible")
        return context
    
class Book_create(LoginRequiredMixin, CreateView):
    model = Libro
    template_name = "biblioteca/create.html"
    fields = ["titulo", "autor", "editorial", "fechaPublicacion", "genero", "isbn", "resumen", "disponibilidad" , "portada"]
    success_url = reverse_lazy("lista")

class Book_details(LoginRequiredMixin, DetailView):
    model = Libro
    template_name = "biblioteca/details.html"
    fields = ["resumen"]

class Book_edit(LoginRequiredMixin, UpdateView):
    model = Libro
    template_name = "biblioteca/edit.html"
    fields = ["titulo", "autor", "editorial", "fechaPublicacion", "genero", "isbn", "resumen", "disponibilidad", "portada"]
    success_url = reverse_lazy("lista")

class Book_delete(LoginRequiredMixin, DeleteView):
    model = Libro
    template_name = "biblioteca/delete.html"
    success_url = reverse_lazy("lista")

'''
class Prestamo_edit(UpdateView):
    model = Libro
    template_name = "biblioteca/prestamoEdit.html"
    fields = ["disponibilidad"]
    success_url = reverse_lazy("lista")
'''

class Prestamo_edit(LoginRequiredMixin, View):
    def get(self, request, pk):
        return render(request, 'biblioteca/prestamoEdit.html')

    def post(self, request, pk):
        libro = get_object_or_404(Libro, pk=pk)
        prestamo = Prestamo.objects.create(
            libroPrestado = libro,
            fechaPrestamo = datetime.now(),
            fechaDevolucion = None,
            usuarioPrestado = request.user,
            estadoPrestamo = "prestado",
        )
        libro.disponibilidad = "prestado"
        libro.save()
        return redirect('lista')

class Disponible_edit(LoginRequiredMixin, View):
    def get(self, request, pk):
        return render(request, 'biblioteca/disponibleEdit.html')
    def post(self, request, pk):
        libro_p = get_object_or_404(Libro, pk=pk, disponibilidad="prestado")
        prestamo = Prestamo.objects.filter(libroPrestado = libro_p, usuarioPrestado = request.user, estadoPrestamo = "prestado").first()
        libro_p.disponibilidad="disponible"
        prestamo.estadoPrestamo= "disponible"
        libro_p.save()
        prestamo.fechaDevolucion = datetime.now()
        prestamo.save()
        return redirect('lista')
