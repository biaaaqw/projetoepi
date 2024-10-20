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
    id_equipamento = request.GET.get('id')
    dados = {}
    
    # Verifica se está editando um equipamento existente
    if id_equipamento:
        dados['equipamento'] = Equipamento.objects.get(id=id_equipamento)
    dados['show_logout'] = True
    return render(request, "cadastrar-equipamento.html", dados)

@login_required(login_url='/login/')
def delete_equipamento(request,id_equipamento):
    equipamento = Equipamento.objects.get(id=id_equipamento)
    equipamento.delete()
    return redirect('/equipamento/')

@login_required(login_url='/login/')
def submit_equipamento(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        data_validade = request.POST.get('data_validade')
        id_equipamento = request.POST.get('id_equipamento') 

        if id_equipamento:
            equipamento = Equipamento.objects.get(id = id_equipamento)
            equipamento.nome=nome
            equipamento.data_validade=data_validade
            try:
                equipamento.save()
                messages.success(request, 'Equipamento alterado com sucesso!')
                return redirect('/equipamento/cadastrar/?id='+id_equipamento)
            except:
                messages.error(request, 'Ocorreu um erro ao cadastrar o equipamento.')
        else:
            try:
                Equipamento.objects.create(nome=nome,
                                data_validade=data_validade)
                messages.success(request, 'Equipamento cadastrado com sucesso!')
            except:
                messages.error(request, 'Ocorreu um erro ao cadastrar o equipamento.')

        return redirect('/equipamento/cadastrar/')
    
    else:
        messages.error(request, 'Ocorreu um erro ao cadastrar o equipamento.')
    return redirect('/equipamento/cadastrar/')

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
            try:
                colaborador.save()
                messages.success(request, 'Colaborador alterado com sucesso!')
                return redirect('/colaborador/cadastrar/?id='+id_colaborador)
            except:
                messages.error(request, 'Ocorreu um erro ao alterar o colaborador.')
        else:
            try:
                Colaborador.objects.create(nome=nome,
                                data_nascimento=data_nascimento)
                messages.success(request, 'Colaborador cadastrado com sucesso!')
            except:
                messages.error(request, 'Ocorreu um erro ao cadastrar o colaborador.')
    return redirect('/colaborador/cadastrar/')

@login_required(login_url='/login/')
def emprestimo (request):
    SITUACAO_CHOICES = [
        ('', ''),   
        ('emprestado', 'Emprestado'),
        ('em_uso', 'Em uso'),
        ('fornecido', 'Fornecido'),
        ('devolvido', 'Devolvido'),
        ('danificado', 'Danificado'),
        ('perdido', 'Perdido'),
    ]

    colaborador=request.GET.get('colaborador')
    equipamento=request.GET.get('equipamento')
    situacao_emprestimo=request.GET.get('situacao_emprestimo')

    if (colaborador is None and equipamento is None and situacao_emprestimo is None):
        emprestimos={}
        show_table=False
    else:
        emprestimos = Emprestimo.objects.all()

        if colaborador:
            emprestimos = emprestimos.filter(id_colaborador__nome__icontains=colaborador)
        if equipamento:
            emprestimos = emprestimos.filter(id_equipamento__nome__icontains=equipamento)
        if situacao_emprestimo:
            emprestimos = emprestimos.filter(situacao_emprestimo=situacao_emprestimo)
        
        show_table=True


    dados = {'emprestimos': emprestimos,
            'show_logout': True,
            'situacao_choices': SITUACAO_CHOICES,
            'show_table':show_table
            }
    return render(request, 'emprestimo.html', dados)

@login_required(login_url='/login/')
def cadastrar_emprestimo(request):
    id_emprestimo = request.GET.get('id')
    if id_emprestimo:
        emprestimo = get_object_or_404(Emprestimo, id=id_emprestimo)
        SITUACAO_CHOICES = [
            ('emprestado', 'Emprestado'),
            ('em_uso', 'Em uso'),
            ('fornecido', 'Fornecido'),
            ('devolvido', 'Devolvido'),
            ('danificado', 'Danificado'),
            ('perdido', 'Perdido'),
        ]
    else:
        emprestimo = None
        SITUACAO_CHOICES = [
            ('emprestado', 'Emprestado'),
            ('em_uso', 'Em uso'),
            ('fornecido', 'Fornecido'),
        ]

    colaboradores = Colaborador.objects.all()
    equipamentos = Equipamento.objects.all()

    dados = {
        'emprestimo': emprestimo,
        'colaboradores': colaboradores,
        'equipamentos': equipamentos,
        'situacao_choices': SITUACAO_CHOICES,
        'show_logout': True,
    }

    return render(request, "cadastrar-emprestimo.html", dados)

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
        data_prevista = request.POST.get('data_prevista') 
        data_devolucao = request.POST.get('data_devolucao') 
        obs_emprestimo = request.POST.get('obs_emprestimo') 
        condicao_emprestimo = request.POST.get('condicao_emprestimo') 
        if id_emprestimo:
            emprestimo=Emprestimo.objects.get(id = id_emprestimo)
            emprestimo.id_colaborador=colaborador
            emprestimo.id_equipamento=equipamento
            emprestimo.situacao_emprestimo=situacao_emprestimo
            emprestimo.data_prevista=data_prevista
            emprestimo.data_devolucao=data_devolucao
            emprestimo.obs_emprestimo=obs_emprestimo
            emprestimo.condicao_emprestimo=condicao_emprestimo
            emprestimo.save()
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
