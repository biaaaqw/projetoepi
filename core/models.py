from django.db import models
from django import forms
from django.contrib.auth.models import User

# Create your models here.
class Colaborador(models.Model):
    nome = models.CharField (max_length=100)
    data_nascimento = models.DateField(blank=True)

    def __str__(self) -> str:
        return self.nome
    
    class Meta: 
        db_table='colaborador'

    def get_data_nascimento(self):
        return self.data_nascimento.strftime('%Y-%m-%d')

class Equipamento(models.Model):
    nome = models.CharField (max_length=100)
    data_validade = models.DateField(blank=True)
    situacao = models.CharField (max_length=100)

    def __str__(self) -> str:
        return self.nome
    
    class Meta: 
        db_table='equipamento'

    def get_data_validade(self):
        return self.data_validade.strftime('%Y-%m-%d')        

class Emprestimo(models.Model):
    SITUACAO_CHOICES = [
        ('emprestado', 'Emprestado'),
        ('em_uso', 'Em uso'),
        ('fornecido', 'Fornecido'),
        ('devolvido', 'Devolvido'),
        ('danificado', 'Danificado'),
        ('perdido', 'Perdido'),
    ]

    id_colaborador = models.ForeignKey(Colaborador, on_delete=models.CASCADE)
    id_equipamento = models.ForeignKey(Equipamento, on_delete=models.CASCADE)
    data_emprestimo = models.DateTimeField(auto_now=True)
    situacao_emprestimo = models.CharField(
        max_length=10,
        choices=SITUACAO_CHOICES,
        default='emprestado',
    )
    data_prevista = models.DateTimeField(null=True,blank=True)
    data_devolucao = models.DateTimeField(null=True,blank=True)
    condicao_emprestimo = models.CharField(max_length=100,null=True,blank=True)
    obs_emprestimo = models.TextField(max_length=500,null=True,blank=True)

    def get_nome_colaborador(self):
        return self.id_colaborador
    
    def get_id_colaborador(self):
        return self.id_colaborador

    def get_nome_equipamento(self):
        return self.id_equipamento
    
    class Meta: 
        db_table='emprestimo' 

    def get_data_emprestimo(self):
        return self.data_emprestimo.strftime('%Y-%m-%d')
    
    def get_data_prevista(self):
        if self.data_prevista:
            return self.data_prevista.strftime('%Y-%m-%d')
        return ""
    
    def get_data_devolucao(self):
        if self.data_devolucao:
            return self.data_devolucao.strftime('%Y-%m-%d')
        return ""

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return self.user.username
