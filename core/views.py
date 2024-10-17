from django.shortcuts import render, redirect, get_object_or_404
from core.models import Equipamento, Colaborador, Emprestimo, UserProfile
from django.contrib.auth.decorators import login_required,permission_required
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponseForbidden

# Create your views here.
def index (request):
    return render(request, 'index.html',{'show_logout': True})

@login_required(login_url='/login/')
def equipamento (request):
    equipamentos = Equipamento.objects.all()
    dados = {'equipamentos': equipamentos, 'show_logout': True}
    return render(request, 'equipamento.html', dados)

@login_required(login_url='/login/')
def cadastrar_equipamento(request):
    id_equipamento=request.GET.get('id')
    dados={}
    if id_equipamento:
        dados['equipamento'] = Equipamento.objects.get(id=id_equipamento)
    dados['show_logout']=True
    return render(request,"cadastrar-equipamento.html",dados)

@login_required(login_url='/login/')
def delete_equipamento(request,id_equipamento):
    equipamento = Equipamento.objects.get(id=id_equipamento)
    equipamento.delete()
    return redirect('/equipamento/')

@login_required(login_url='/login/')
def submit_equipamento(request):
    if request.POST:
        nome = request.POST.get('nome')
        data_validade = request.POST.get('data_validade')
        situacao = request.POST.get('situacao')
        id_equipamento = request.POST.get('id_equipamento') 
        if id_equipamento:
            equipamento = Equipamento.objects.get(id = id_equipamento)
            equipamento.nome=nome
            equipamento.data_validade=data_validade
            equipamento.situacao=situacao
            equipamento.save()
        else:        
            Equipamento.objects.create(nome=nome,
                              data_validade=data_validade,
                              situacao=situacao)
    return redirect('/equipamento/')

@login_required(login_url='/login/')
def colaborador (request):
    colaboradores = Colaborador.objects.all()
    dados = {'colaboradores': colaboradores, 'show_logout':True}
    return render(request, 'colaborador.html', dados)

@login_required(login_url='/login/')
def cadastrar_colaborador(request):
    id_colaborador=request.GET.get('id')
    dados={}
    if id_colaborador:
        dados['colaborador'] = Colaborador.objects.get(id=id_colaborador)
    dados['show_logout'] = True
    return render(request,"cadastrar-colaborador.html",dados)

@login_required(login_url='/login/')
def delete_colaborador(request,id_colaborador):
    colaborador = Colaborador.objects.get(id=id_colaborador)
    colaborador.delete()
    return redirect('/colaborador/')

@login_required(login_url='/login/')
def submit_colaborador(request):
    if request.POST:
        data_nascimento = request.POST.get('data_nascimento')
        id_colaborador = request.POST.get('id_colaborador') 
        nome = request.POST.get('nome') 
        if id_colaborador:
            colaborador = Colaborador.objects.get(id = id_colaborador)
            colaborador.nome=nome
            colaborador.data_nascimento=data_nascimento
            colaborador.save()
        else:
            Colaborador.objects.create(nome=nome,
                              data_nascimento=data_nascimento)
    return redirect('/colaborador/')

@login_required(login_url='/login/')
def emprestimo (request):
    emprestimos = Emprestimo.objects.all()
    dados = {'emprestimos': emprestimos, 'show_logout': True}
    return render(request, 'emprestimo.html', dados)

@login_required(login_url='/login/')
def cadastrar_emprestimo(request):
    colaboradores = Colaborador.objects.all()
    equipamentos = Equipamento.objects.all()
    id_emprestimo=request.GET.get('id')
    dados={}
    if id_emprestimo:
        dados['emprestimo'] = Emprestimo.objects.get(id=id_emprestimo)
    dados['colaboradores'] = colaboradores
    dados['equipamentos'] = equipamentos
    dados['show_logout'] = True
    return render(request,"cadastrar-emprestimo.html",dados)

@login_required(login_url='/login/')
def delete_emprestimo(request,id_emprestimo):
    emprestimo = Emprestimo.objects.get(id=id_emprestimo)
    emprestimo.delete()
    return redirect('/emprestimo/')

@login_required(login_url='/login/')
def submit_emprestimo(request):
    if request.POST:
        id_colaborador = request.POST.get('id_colaborador')
        colaborador = Colaborador.objects.get(id = id_colaborador)
        id_equipamento = request.POST.get('id_equipamento')
        equipamento = Equipamento.objects.get(id = id_equipamento)        
        situacao_emprestimo = request.POST.get('situacao_emprestimo')
        id_emprestimo = request.POST.get('id_emprestimo') 
        if id_emprestimo:
            Emprestimo.objects.get(id = id_emprestimo).update(id_colaborador=colaborador,
                                  id_equipamento=equipamento,
                                  situacao_emprestimo=situacao_emprestimo)
        else:        
            Emprestimo.objects.create(id_colaborador=colaborador,
                                  id_equipamento=equipamento,
                                  situacao_emprestimo=situacao_emprestimo)
    return redirect('/emprestimo/')

def login_usuario(request):
    url_next = request.GET.get('next', None)
    dados={}
    dados['show_logout']=False
    if url_next is not None:
        dados['url_next']=url_next
    return render(request,'login.html',dados)

def submit_login(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        url_next = request.POST.get('url_next', None)
        usuario = authenticate(username=username, password=password)
        if usuario is not None:
            login(request,usuario)
            if url_next is not None:
                return redirect(url_next)
            return redirect('/')
        else:
            messages.error(request,"Usuário ou senha inválido!")
            if url_next is not None:
                return redirect('/login/?next='+url_next)
        return redirect('/login/')
    else:
        if url_next is not None:
            return redirect('/login/?next='+url_next)
        return redirect('/login/')

def logout_usuario(request):
    logout(request)
    return redirect('/')

@permission_required('auth.add_user', raise_exception=True,login_url='/login/')
def usuario (request):
    usuarios = User.objects.all()
    dados = {'usuarios': usuarios   , 'show_logout':True}
    return render(request, 'usuario.html', dados)

@permission_required('auth.add_user', raise_exception=True,login_url='/login/')
def cadastrar_usuario(request):
    id_usuario=request.GET.get('id')
    dados={}
    if id_usuario:
        dados['usuario'] = User.objects.get(id=id_usuario)
    dados['show_logout'] = True
    return render(request,"cadastrar-usuario.html",dados)

@permission_required('auth.add_user', raise_exception=True,login_url='/login/')
def delete_usuario(request,id_usuario):
    usuario = get_object_or_404(User, id=id_usuario)
    usuario.delete()
    return redirect('/usuario/')

#a tela de alteração de cadastro de usuário deve ser diferente para o próprio usuário
@permission_required('auth.change_user', raise_exception=True, login_url='/login/')
def submit_usuario(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        id_usuario = request.POST.get('id_usuario')

        # Verifica se o superusuário está editando outro usuário
        if id_usuario:
            usuario = get_object_or_404(User, id=id_usuario)
            
            # Permite que apenas superusuários editem outros superusuários
            if not request.user.is_superuser:
                return HttpResponseForbidden("Você não tem permissão para alterar usuários.")

            usuario.username = username
            usuario.set_password(password)
            usuario.save()
            if usuario == request.user:
                usuario = authenticate(username=username, password=password)
                login(request,usuario)
        else:
            # Criação de novo usuário
            User.objects.create_user(username=username, password=password)

    return redirect('/usuario/')

@login_required(login_url='/login/')
def perfil(request):
    usuario = request.user
    dados={
        'usuario': usuario,
        'show_logout': True
    }
    return render(request,'perfil.html',dados)

#a tela de alteração de cadastro de usuário deve ser diferente para o próprio usuário
@login_required(login_url='/login/')
def submit_perfil(request):
    usuario = request.user
    user_profile, created = UserProfile.objects.get_or_create(user=usuario)
    if request.method == 'POST':
        id_usuario = request.POST.get('id_usuario')
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        #opicional
        password = request.POST.get('password',None)
        profile_picture = request.FILES.get('profile_picture')

        # Verifica se o usuário está editando outro usuário
        if int(id_usuario) == usuario.id:
            
            usuario.username=username
            usuario.first_name=first_name
            usuario.last_name=last_name
            usuario.email=email

            if profile_picture:
                user_profile.profile_picture = profile_picture
                user_profile.save()

            usuario.save()
        
            if password:
                usuario.set_password(password)
                usuario.save()

            usuario = authenticate(username=username, password=password)
            login(request,usuario)
        else:
            return HttpResponseForbidden("Você não tem permissão para alterar esse usuário.")
    return redirect('/usuario/perfil/')
