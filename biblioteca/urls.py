from django.urls import path
from .views import Libro_list, Book_create, Book_details, Book_edit, Book_delete, Prestamo_edit, Book_list_prestados, Book_list_disponibles, Disponible_edit


urlpatterns = [
    path('', Libro_list.as_view(), name='lista'),
    path('biblioteca/disponibles/', Book_list_disponibles.as_view(), name='lista_disponible'),
    path('biblioteca/prestados/', Book_list_prestados.as_view(), name='lista_prestado'),
    path('biblioteca/create/', Book_create.as_view(), name='book_create'),
    path('biblioteca/details/<int:pk>', Book_details.as_view(), name='book_details'),
    path('biblioteca/edit/<int:pk>', Book_edit.as_view(), name='book_edit'),
    path('biblioteca/delete/<int:pk>', Book_delete.as_view(), name='book_delete'),
    path('biblioteca/prestamo/<int:pk>', Prestamo_edit.as_view(), name='prestamo_edit'),
    path('biblioteca/disponible/<int:pk>', Disponible_edit.as_view(), name='disponible_edit'),
]