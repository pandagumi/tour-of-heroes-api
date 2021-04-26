"""Test main"""
import unittest

from main import app


class TestMain(unittest.TestCase):
    """Test main"""

    # O setUp vai ser chamado antes de cada teste que criamos nessa classe
    def setUp(self):
        """Set up class"""
        # Aqui é iniciado a API no ambiente de teste
        self.app = app.test_client()

    def test_get_index_url(self):
        """Test get index url"""
        # Fazendo a requisição para a url / da API
        response = self.app.get('/')

        # Conferindo se voltou 200
        self.assertEqual(response.status_code, 200)

        # Conferindo a resposta da requisição
        self.assertEqual(response.get_json(), {'API': 'Heroes'})

    def test_get_not_found_url(self):
        """Test get not found url"""
        # Fazendo a requisição para a url /teste/teste/teste da API
        response = self.app.get('/teste/teste/teste')
        # Conferindo se voltou 404
        self.assertEqual(response.status_code, 404)
        # Conferindo a resposta da requisição
        self.assertEqual(response.get_data(), b'Sorry, Nothing at this URL.')


if __name__ == '__main__':
    unittest.main()
