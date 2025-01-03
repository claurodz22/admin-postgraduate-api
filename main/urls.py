# lo cree yo

from django.urls import path
from .views import PagosListAPIView  # Importa tu vista para mostrar los productos

urlpatterns = [
    path('pagos/', PagosListAPIView.as_view(), name='pagos-list'),  # Ruta de la API
]
