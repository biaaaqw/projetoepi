from django.shortcuts import render, redirect
from core.models import Equipamento, Colaborador, Emprestimo

# Create your views here.
def index (request):
    return render(request, 'index.html')

def equipamento (request):
    equipamentos = Equipamento.objects.all()
    dados = {'equipamentos': equipamentos}
    return render(request, 'equipamento.html', dados)

def cadastrar_equipamento(request):
    id_equipamento=request.GET.get('id')
    dados={}
    if id_equipamento:
        dados['equipamento'] = Equipamento.objects.get(id=id_equipamento)
    return render(request,"cadastrar-equipamento.html",dados)

def delete_equipamento(request,id_equipamento):
    equipamento = Equipamento.objects.get(id=id_equipamento)
    equipamento.delete()
    return redirect('/equipamento/')

def submit_equipamento(request):
    if request.POST:
        id = request.POST.get('id')
        data_validade = request.POST.get('data_validade')
        situacao = request.POST.get('situacao')
        id_equipamento = request.POST.get('id_equipamento') 
        if id_equipamento:
            Equipamento.objects.filter(id = id_equipamento).update(id=id,
                              data_validade=data_validade,
                              situacao=situacao)
        else:        
            Equipamento.objects.create(id=id,
                              data_validade=data_validade,
                              situacao=situacao)
    return redirect('/equipamento/')

def colaborador (request):
    colaboradores = Colaborador.objects.all()
    dados = {'colaboradores': colaboradores}
    return render(request, 'colaborador.html', dados)

def cadastrar_colaborador(request):
    id_colaborador=request.GET.get('id')
    dados={}
    if id_colaborador:
        dados['colaborador'] = Colaborador.objects.get(id=id_colaborador)
    return render(request,"cadastrar-colaborador.html",dados)

def delete_colaborador(request,id_colaborador):
    colaborador = Colaborador.objects.get(id=id_colaborador)
    colaborador.delete()
    return redirect('/colaborador/')

def submit_colaborador(request):
    if request.POST:
        id = request.POST.get('id')
        data_nascimento = request.POST.get('data_nascimento')
        id_colaborador = request.POST.get('id_colaborador') 
        if id_colaborador:
            Colaborador.objects.filter(id = id_colaborador).update(id=id,
                              data_nascimento=data_nascimento)
        else:
            Colaborador.objects.create(id=id,
                              data_nascimento=data_nascimento)
    return redirect('/colaborador/')


def emprestimo (request):
    emprestimos = Emprestimo.objects.all()
    dados = {'emprestimos': emprestimos}
    return render(request, 'emprestimo.html', dados)

def cadastrar_emprestimo(request):
    colaboradores = Colaborador.objects.all()
    equipamentos = Equipamento.objects.all()
    id_emprestimo=request.GET.get('id')
    dados={}
    if id_emprestimo:
        dados['emprestimo'] = Emprestimo.objects.get(id=id_emprestimo)
    dados['colaboradores'] = colaboradores
    dados['equipamentos'] = equipamentos
    return render(request,"cadastrar-emprestimo.html",dados)

def delete_emprestimo(request,id_emprestimo):
    emprestimo = Emprestimo.objects.get(id=id_emprestimo)
    emprestimo.delete()
    return redirect('/emprestimo/')

def submit_emprestimo(request):
    if request.POST:
        id_colaborador = request.POST.get('id_colaborador')
        colaborador = Colaborador.objects.get(id = id_colaborador)
        id_equipamento = request.POST.get('id_equipamento')
        equipamento = Equipamento.objects.get(id = id_equipamento)        
        situacao_emprestimo = request.POST.get('situacao_emprestimo')
        id_emprestimo = request.POST.get('id_emprestimo') 
        if id_emprestimo:
            Emprestimo.objects.filter(id = id_emprestimo).update(id_colaborador=colaborador,
                                  id_equipamento=equipamento,
                                  situacao_emprestimo=situacao_emprestimo)
        else:        
            Emprestimo.objects.create(id_colaborador=colaborador,
                                  id_equipamento=equipamento,
                                  situacao_emprestimo=situacao_emprestimo)
    return redirect('/emprestimo/')



