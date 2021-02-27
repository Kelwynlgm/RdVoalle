from django.urls import path

from .views import ClientesApiView, get_response

app_name = 'Clientes'
urlpatterns = [
    path('cron/get', get_response, name='get_response'),
    path('adiciona/clientes', ClientesApiView.as_view(), name='clientes'),
]