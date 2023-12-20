# mydashboard/urls.py
from django.contrib import admin
from django.urls import include, path
from django.shortcuts import redirect
from dashboard.views import dashboard
from dashboard.views import home, sobre, contatos

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda request: redirect('home/'), name='index'),  # Adicione esta linha para redirecionar
    path('dashboard/', dashboard, name='dashboard'),
    path('home/', home, name='home'),
    path('sobre/', sobre, name='sobre'),
    path('contatos/', contatos, name='contatos'),
]
