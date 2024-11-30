from urllib import response
from django.test import TestCase, Client
from django.urls import reverse
from core.models import Equipamento, Colaborador, Emprestimo, UserProfile
from django.contrib.auth.models import User
from core.views import emprestimo


class CoreViewsTest(TestCase):
    """Testes unitários para as views do aplicativo Core"""

    def setUp(self):
        """Configuração inicial para os testes"""
        self.client = Client()
        self.superuser = User.objects.create_superuser(username='admin', password='adminpass')
        self.user = User.objects.create_user(username='user', password='userpass')
        self.equipamento = Equipamento.objects.create(nome='Equipamento Teste', data_validade='2025-12-31')
        self.colaborador = Colaborador.objects.create(nome='Colaborador Teste', data_nascimento='1990-01-01')

    # Testes de Views
    def test_index_view(self):
        """Testa se a view index carrega corretamente"""
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_equipamento_view(self):
        """Testa acesso à view de equipamentos"""
        # Acesso não autenticado
        response = self.client.get(reverse('equipamento'))
        self.assertEqual(response.status_code, 302)  # Redirecionado para login

        # Acesso autenticado
        self.client.login(username='user', password='userpass')
        response = self.client.get(reverse('equipamento'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'equipamento.html')
        self.assertContains(response, self.equipamento.nome)

    # Testes de Funcionalidade do cadastro de Equipamento
    def test_submit_equipamento_create(self):
        """Testa o cadastro de um novo equipamento"""
        self.client.login(username='user', password='userpass')
        response = self.client.post(reverse('submit_equipamento'), {
            'nome': 'Novo Equipamento',
            'data_validade': '2026-12-31'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Equipamento.objects.filter(nome='Novo Equipamento').exists())

    def test_submit_equipamento_update(self):
        """Testa a atualização de um equipamento existente"""
        self.client.login(username='user', password='userpass')
        response = self.client.post(reverse('submit_equipamento'), {
            'id_equipamento': self.equipamento.id,
            'nome': 'Equipamento Atualizado',
            'data_validade': '2027-12-31'
        })
        self.assertEqual(response.status_code, 302)
        equipamento = Equipamento.objects.get(id=self.equipamento.id)
        self.assertEqual(equipamento.nome, 'Equipamento Atualizado')

    def test_delete_equipamento(self):
        """Testa a exclusão de um equipamento"""
        self.client.login(username='user', password='userpass')
        response = self.client.get(reverse('delete_equipamento', args=[self.equipamento.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Equipamento.objects.filter(id=self.equipamento.id).exists())

    # Testes de Login e Logout
    def test_login_logout(self):
        """Testa o login e logout de um usuário"""
        # Login
        response = self.client.post(reverse('submit_login'), {
            'username': 'user',
            'password': 'userpass'
        })
        self.assertEqual(response.status_code, 302)  # Redirecionado após login
        self.assertTrue('_auth_user_id' in self.client.session)

        # Logout
        response = self.client.get(reverse('logout_usuario'))
        self.assertEqual(response.status_code, 302)  # Redirecionado após logout
        self.assertFalse('_auth_user_id' in self.client.session)
         
    # Testes de Login com senha invalida
    def test_login_false(self):
        """Testa o login e logout de um usuário"""
        # Login
        response = self.client.post(reverse('submit_login'), {
            'username': 'user',
            'password': 'nopass'
        })
        self.assertEqual(response.status_code, 302)  # Redirecionado após login
        self.assertTrue('_auth_user_id' not in self.client.session)
        
   # Testes de Filtro de Empréstimos
    def test_emprestimo_filter(self):
        """Testa a funcionalidade de filtro de empréstimos"""
        self.client.login(username='user', password='userpass')
        response = self.client.get(reverse('emprestimo'), {'colaborador': self.colaborador.nome})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'emprestimo.html')

    def test_crud_equipamento(self):
        """Testa o fluxo completo de Funcionalidade do cadastro de equipamentos"""
        # Cadastro de equipamento
        self.client.login(username='user', password='userpass')
        response = self.client.post(reverse('submit_equipamento'), {
            'nome': 'Novo Equipamento',
            'data_validade': '2026-12-31'
        })
       
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/equipamento/cadastrar/')
        self.assertTrue(Equipamento.objects.filter(nome="Novo Equipamento").exists())

        # Edição de equipamento
        equipamento = Equipamento.objects.get(nome="Novo Equipamento")
        self.client.login(username='user', password='userpass')
        response = self.client.post(reverse('submit_equipamento'), {
            'id': equipamento.id,
            'nome': 'Equipamento Editado',
            'data_validade': '2036-12-31'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Equipamento.objects.filter(nome="Equipamento Editado").exists())

        # Exclusão de equipamento
        equipamento = Equipamento.objects.get(nome="Equipamento Editado")
        self.client.login(username='user', password='userpass')
        response = self.client.get(reverse('delete_equipamento', args=[equipamento.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Equipamento.objects.filter(nome="Equipamento Editado").exists())

    def test_crud_emprestimo(self):
        """Testa o cadastro e exclusão de empréstimos"""
        # Cadastro de empréstimo
        self.client.login(username='user', password='userpass')
        response = self.client.post(reverse('submit_emprestimo'), {
            'id_colaborador': self.colaborador.id,
            'id_equipamento': self.equipamento.id,
            'situacao_emprestimo': 'emprestado'
        })
        #'data_prevista': '2026-12-31',
        #'data_devolucao': '2026-12-31',
        #'obs_emprestimo': 'Observação',
        #'condicao_emprestimo': 'Normal'
        
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Emprestimo.objects.filter(id_colaborador=self.colaborador.id, id_equipamento=self.equipamento.id).exists())

        # Exclusão de empréstimo
        emprestimo = Emprestimo.objects.get(id_colaborador=self.colaborador.id, id_equipamento=self.equipamento.id)
        self.client.login(username='user', password='userpass')
        response = self.client.get(reverse('delete_emprestimo', args=[emprestimo.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Emprestimo.objects.filter(id=emprestimo.id).exists())
        
    def test_integracao_emprestimo(self):
        """Testa a integração do cadastro de equipamento e seu empréstimo """
        # Cadastro de equipamento
        self.client.login(username='user', password='userpass')
        response = self.client.post(reverse('submit_equipamento'), {
            'nome': 'Novo Equipamento',
            'data_validade': '2026-12-31'
        })
       
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/equipamento/cadastrar/')
        self.assertTrue(Equipamento.objects.filter(nome="Novo Equipamento").exists())

        self.equipamento = Equipamento.objects.get(nome="Novo Equipamento")
        
        """Testa o cadastro e exclusão de empréstimos"""
        # Cadastro de empréstimo
        self.client.login(username='user', password='userpass')
        response = self.client.post(reverse('submit_emprestimo'), {
            'id_colaborador': self.colaborador.id,
            'id_equipamento': self.equipamento.id,
            'situacao_emprestimo': 'emprestado'
        })
        #'data_prevista': '2026-12-31',
        #'data_devolucao': '2026-12-31',
        #'obs_emprestimo': 'Observação',
        #'condicao_emprestimo': 'Normal'
        
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Emprestimo.objects.filter(id_colaborador=self.colaborador.id, id_equipamento=self.equipamento.id).exists())

        # Exclusão de empréstimo
        emprestimo = Emprestimo.objects.get(id_colaborador=self.colaborador.id, id_equipamento=self.equipamento.id)
        self.client.login(username='user', password='userpass')
        response = self.client.get(reverse('delete_emprestimo', args=[emprestimo.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Emprestimo.objects.filter(id=emprestimo.id).exists())
        
        # Exclusão de equipamento
        equipamento = Equipamento.objects.get(nome="Novo Equipamento")
        self.client.login(username='user', password='userpass')
        response = self.client.get(reverse('delete_equipamento', args=[equipamento.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Equipamento.objects.filter(nome="Novo Equipamento").exists())
