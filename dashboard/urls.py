from django.urls import path
from .views import dashboard
from .views import save_temperature
from .views import get_temperature_history
from .views import home, sobre, contatos

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('home/', home, name='home'),
    path('sobre/', sobre, name='sobre'),
    path('contatos/', contatos, name='contatos'),
    path('save-temperature/', save_temperature, name='save_temperature'),
    path('get_temperature_history/', get_temperature_history, name='get_temperature_history'),
]