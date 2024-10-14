from django.contrib import admin
from core.models import Colaborador, Equipamento, Emprestimo
# Register your models here.
class ColaboradorAdmin(admin.ModelAdmin):
    list_display = ('id','nome','data_nascimento')

admin.site.register(Colaborador,ColaboradorAdmin)

class EquipamentoAdmin(admin.ModelAdmin):
    list_display = ('id','nome','data_validade','situacao')

admin.site.register(Equipamento,EquipamentoAdmin)

class EmprestimoAdmin(admin.ModelAdmin):
    list_display = ('id','id_colaborador','id_equipamento','situacao_emprestimo', 'data_emprestimo')

admin.site.register(Emprestimo,EmprestimoAdmin)