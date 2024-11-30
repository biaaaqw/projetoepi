from django.contrib import admin
from django.urls import path
from core import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),

    # Login & Logout
    path('', views.index, name='index'),
    path('login/', views.login_usuario, name='login'),
    path('login/submit', views.submit_login, name='submit_login'),
    path('logout/', views.logout_usuario, name='logout_usuario'),

    # Colaborador
    path('colaborador/', views.colaborador, name='colaborador'),
    path('colaborador/cadastrar/', views.cadastrar_colaborador, name='cadastrar_colaborador'),
    path('colaborador/cadastrar/submit', views.submit_colaborador, name='submit_colaborador'),
    path('colaborador/excluir/<int:id_colaborador>/', views.delete_colaborador, name='delete_colaborador'),

    # Equipamento
    path('equipamento/', views.equipamento, name='equipamento'),
    path('equipamento/cadastrar/', views.cadastrar_equipamento, name='cadastrar_equipamento'),
    path('equipamento/cadastrar/submit', views.submit_equipamento, name='submit_equipamento'),
    path('equipamento/excluir/<int:id_equipamento>/', views.delete_equipamento, name='delete_equipamento'),

    # Empréstimo
    path('emprestimo/', views.emprestimo, name='emprestimo'),
    path('emprestimo/cadastrar/', views.cadastrar_emprestimo, name='cadastrar_emprestimo'),
    path('emprestimo/cadastrar/submit', views.submit_emprestimo, name='submit_emprestimo'),
    path('emprestimo/excluir/<int:id_emprestimo>/', views.delete_emprestimo, name='delete_emprestimo'),

    # Usuário
    path('usuario/', views.usuario, name='usuario'),
    path('usuario/cadastrar/', views.cadastrar_usuario, name='cadastrar_usuario'),
    path('usuario/cadastrar/submit', views.submit_usuario, name='submit_usuario'),
    path('usuario/excluir/<int:id_usuario>/', views.delete_usuario, name='delete_usuario'),
    path('usuario/perfil/', views.perfil, name='perfil'),
    path('usuario/perfil/submit', views.submit_perfil, name='submit_perfil'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
