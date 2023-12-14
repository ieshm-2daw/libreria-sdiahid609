from datetime import datetime
from typing import Any
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from .models import Libro, Prestamo, Autor
from django.views import View
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView, ListView


class Libro_list(ListView):
    model = Libro
    template_name="biblioteca/lista.html"
    #queryset=Libro.objects.filter(disponibilidad="disponible")
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['autores'] = Autor.objects.all()
        generosLibro = []
        for libro in Libro.objects.all() :
            if libro.genero not in generosLibro:
                generosLibro.append(libro.genero)
        context['generosLibro'] = generosLibro
        a = self.request.GET.get('autor')
        g = self.request.GET.get('genero')
        if  (a == "all" or a == None) and (g == "all" or g == None):
            context['libros_disponibles'] = Libro.objects.filter(disponibilidad="disponible")
            context['libros_prestados'] = Libro.objects.filter(disponibilidad="prestado")
        elif g == "all" or g == None:
            autor = Autor.objects.get(nombre=a)
            context['libros_disponibles'] = Libro.objects.filter(disponibilidad="disponible", autor = autor)
            context['libros_prestados'] = Libro.objects.filter(disponibilidad="prestado", autor=autor)
        elif a == "all" or a == None:
            context['libros_disponibles'] = Libro.objects.filter(disponibilidad="disponible", genero = g)
            context['libros_prestados'] = Libro.objects.filter(disponibilidad="prestado", genero=g)
        else:
            autor = Autor.objects.get(nombre=a)
            context['libros_disponibles'] = Libro.objects.filter(disponibilidad="disponible", autor = autor, genero=g)
            context['libros_prestados'] = Libro.objects.filter(disponibilidad="prestado", autor=autor, genero=g)
            
        return context

class Book_list_prestados(ListView):
    model = Prestamo
    template_name="biblioteca/lista_prestado.html"
    #queryset=Libro.objects.filter(disponibilidad="disponible")
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['usuario'] = self.request.user
        context['prestamos'] = Prestamo.objects.filter(estadoPrestamo="prestado")
        context['historialPrestamos'] = Prestamo.objects.filter(estadoPrestamo="disponible")
        return context

class Book_list_disponibles(ListView):
    model = Libro
    template_name="biblioteca/lista_disponible.html"
    #queryset=Libro.objects.filter(disponibilidad="disponible")
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['libros_disponibles'] = Libro.objects.filter(disponibilidad="disponible")
        return context
    
class Book_create(CreateView):
    model = Libro
    template_name = "biblioteca/create.html"
    fields = ["titulo", "autor", "editorial", "fechaPublicacion", "genero", "isbn", "resumen", "disponibilidad" , "portada"]
    success_url = reverse_lazy("lista")

class Book_details(DetailView):
    model = Libro
    template_name = "biblioteca/details.html"
    fields = ["resumen"]

class Book_edit(UpdateView):
    model = Libro
    template_name = "biblioteca/edit.html"
    fields = ["titulo", "autor", "editorial", "fechaPublicacion", "genero", "isbn", "resumen", "disponibilidad", "portada"]
    success_url = reverse_lazy("lista")

class Book_delete(DeleteView):
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

class Prestamo_edit(View):
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

class Disponible_edit(View):
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
