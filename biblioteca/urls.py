from django.urls import path
from .views import Libro_list, Book_create, Book_details, Book_edit, Book_delete, Prestamo_edit


urlpatterns = [
    path('', Libro_list.as_view(), name='lista'),
    path('biblioteca/create/', Book_create.as_view(), name='book_create'),
    path('biblioteca/details/<int:pk>', Book_details.as_view(), name='book_details'),
    path('biblioteca/edit/<int:pk>', Book_edit.as_view(), name='book_edit'),
    path('biblioteca/delete/<int:pk>', Book_delete.as_view(), name='book_delete'),
    path('biblioteca/prestamo/<int:pk>', Prestamo_edit.as_view(), name='prestamo_edit')
]