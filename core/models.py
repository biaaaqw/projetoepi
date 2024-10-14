from django.db import models
from django import forms

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
    id_colaborador = models.ForeignKey (Colaborador, on_delete=models.CASCADE)
    id_equipamento = models.ForeignKey (Equipamento, on_delete=models.CASCADE)
    situacao_emprestimo = models.CharField (max_length=100)
    data_emprestimo = models.DateTimeField(auto_now = True)
    
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

