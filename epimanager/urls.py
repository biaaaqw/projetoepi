"""
URL configuration for epimanager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),
    path('login/', views.login_usuario),
    path('login/submit',views.submit_login),
    path('logout/',views.logout_usuario),
    path('colaborador/', views.colaborador),
    path('colaborador/cadastrar/', views.cadastrar_colaborador),
    path('colaborador/cadastrar/submit', views.submit_colaborador),
    path('colaborador/excluir/<int:id_colaborador>/', views.delete_colaborador),
    path('equipamento/', views.equipamento),
    path('equipamento/cadastrar/', views.cadastrar_equipamento),
    path('equipamento/cadastrar/submit', views.submit_equipamento),
    path('equipamento/excluir/<int:id_equipamento>/', views.delete_equipamento),
    path('emprestimo/', views.emprestimo),
    path('emprestimo/cadastrar/', views.cadastrar_emprestimo),
    path('emprestimo/cadastrar/submit', views.submit_emprestimo),
    path('emprestimo/excluir/<int:id_emprestimo>/', views.delete_emprestimo),
    path('usuario/', views.usuario),
    path('usuario/cadastrar/', views.cadastrar_usuario),
    path('usuario/cadastrar/submit', views.submit_usuario),
    path('usuario/excluir/<int:id_usuario>/', views.delete_usuario),
]
