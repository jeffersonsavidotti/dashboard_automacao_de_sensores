# mydashboard/urls.py
from django.contrib import admin
from django.urls import include, path
from django.shortcuts import redirect
from dashboard.views import dashboard

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda request: redirect('dashboard/'), name='index'),  # Adicione esta linha para redirecionar
    path('dashboard/', dashboard, name='dashboard'),
]
