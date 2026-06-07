from django.urls import path
from .views import buscar_produto_openfoodfacts

urlpatterns = [
    path("api/openfoodfacts/", buscar_produto_openfoodfacts, name="buscar_produto_openfoodfacts"),
]