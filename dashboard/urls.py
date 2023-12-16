from django.urls import path
from .views import dashboard
from .views import save_temperature

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('save-temperature/', save_temperature, name='save_temperature'),
]