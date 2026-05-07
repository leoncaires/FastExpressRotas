import unittest
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from web.app import app

class TesteIntegracao(unittest.TestCase):
    def setUp(self):
        self.cliente = app.test_client()
        app.config['TESTING'] = True

    def testar_pagina_inicial(self):
        """A página principal deve retornar status 200."""
        resposta = self.cliente.get('/')
        self.assertEqual(resposta.status_code, 200)

    def testar_api_rota(self):
        """A API de rota deve retornar caminho correto."""
        resposta = self.cliente.post('/api/rota',
                                     json={"start": 0, "target": 2},
                                     content_type='application/json')
        self.assertEqual(resposta.status_code, 200)
        dados = resposta.get_json()
        self.assertTrue(dados['has_path'])
        self.assertEqual(dados['distance'], 12)  # rota direta 0->2 (12 min)