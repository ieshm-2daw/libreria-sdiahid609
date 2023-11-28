from django.shortcuts import render
from django.urls import reverse_lazy
from .models import Libro
from django.views import View
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView


class Libro_list(View):
    def get(self, request):
        libros = Libro.objects.all()
        return render(request, 'biblioteca/lista.html', {'libros':libros})

class Book_create(CreateView):
    model = Libro
    template_name = "biblioteca/create.html"
    fields = ["titulo", "autor", "editorial", "fechaPublicacion", "genero", "isbn", "resumen", "disponibilidad"]
    success_url = reverse_lazy("lista")

class Book_details(DetailView):
    model = Libro
    template_name = "biblioteca/details.html"
    fields = ["resumen"]

class Book_edit(UpdateView):
    model = Libro
    template_name = "biblioteca/edit.html"
    fields = ["titulo", "autor", "editorial", "fechaPublicacion", "genero", "isbn", "resumen", "disponibilidad"]
    success_url = reverse_lazy("lista")

class Book_delete(DeleteView):
    model = Libro
    template_name = "biblioteca/delete.html"
    success_url = reverse_lazy("lista")

