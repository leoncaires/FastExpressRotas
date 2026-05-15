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
        """A API de rota deve retornar caminho para vértices existentes no grafo."""
        # Obtém vértices reais do grafo via API
        resp_vertices = self.cliente.get('/api/vertices')
        self.assertEqual(resp_vertices.status_code, 200)
        vertices = resp_vertices.get_json()
        self.assertGreaterEqual(len(vertices), 2, "Grafo não possui vértices suficientes para o teste.")

        # Seleciona dois vértices diferentes (primeiro e último da lista)
        id_origem = vertices[0]['id']
        id_destino = vertices[-1]['id']

        resposta = self.cliente.post('/api/rota',
                                     json={"start": id_origem, "target": id_destino},
                                     content_type='application/json')
        self.assertEqual(resposta.status_code, 200)
        dados = resposta.get_json()
        self.assertTrue(dados['has_path'], f"Rota deveria existir entre {id_origem} e {id_destino}")