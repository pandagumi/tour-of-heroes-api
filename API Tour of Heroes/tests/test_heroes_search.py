"""Heroes search test case"""
import unittest

from mock import patch
from mockfirestore import MockFirestore

from main import app
from models.hero import Hero


class HeroesSearchHandlerTestCase(unittest.TestCase):
    """Heroes search handler"""

    def setUp(self):
        """SetUp é chamado no inicio de cada teste"""
        self.mock_db = MockFirestore()
        self.patcher = patch(
            'modules.main.MainModule.get_firestore_db',
            return_value=self.mock_db)
        self.patcher.start()
        self.app = app.test_client()

    def tearDown(self):
        """O tearDown é chamado no final de cada teste"""
        self.patcher.stop()
        self.mock_db.reset()

    def test_search_hero(self):
        """Test search hero by name"""
        # Criando dois herois com nomes diferentes
        self.create_hero('Superman', 'dc')
        self.create_hero('Batman', 'dc')

        # Pesquisando o heroi Superman
        response = self.app.get(path='/search?name=' + 'Superman')

        # Conferindo o status da requisição
        self.assertEqual(response.status_code, 200)

        # Conferindo se voltou somente um heroi
        self.assertEqual(len(response.get_json()), 1)
        # Conferindo o nome do heroi que voltou
        self.assertEqual(response.get_json()[0]['name'], 'Superman')

    def test_search_hero_with_lowercase_param_name(self):
        """Test search hero by lowercase param name"""
        # Criando dois herois com nomes diferentes
        self.create_hero('Superman', 'dc')
        self.create_hero('Batman', 'dc')

        # Pesquisando o heroi Superman com a primeira letra minuscula
        # No metodo view vocês só precisam chamar o metodo title para deixar
        # a primeira letra maiuscula e o teste ira passar
        response = self.app.get(path='/search?name=' + 'superman')

        # Conferindo o status da requisição
        self.assertEqual(response.status_code, 200)

        # Conferindo se voltou somente um heroi
        self.assertEqual(len(response.get_json()), 1)
        # Conferindo o nome do heroi que voltou
        self.assertEqual(response.get_json()[0]['name'], 'Superman')

    def test_search_hero_max_returned_items(self):
        """Test search hero max items returned in query"""
        # Criando 15 herois com o mesmo nome para testar o limite da consulta
        for _ in range(15):
            self.create_hero('Superman', 'dc')

        # Pesquisando o heroi
        response = self.app.get(path='/search?name=' + 'Superman')

        # Conferindo o status da requisição
        self.assertEqual(response.status_code, 200)

        # Conferindo se voltou somente 10 herois que é o limite mencionado
        self.assertEqual(len(response.get_json()), 10)

    def test_search_hero_without_param_name(self):
        """Test search hero without param name"""

        # Pesquisando o heroi sem o parametro name, fazendo isso a requisição
        # deve retornar o status 400(Bad request) e retornar um json com
        # a mensagem de erro
        response = self.app.get(path='/search?name=')

        # Conferindo o status da requisição
        self.assertEqual(response.status_code, 400)

        # Conferindo a mensagem de erro que voltou
        self.assertDictEqual(
            response.get_json(),
            {'message': 'Bad request, param name is required'}
        )

    @staticmethod
    def create_hero(hero_name, universe):
        hero = Hero()
        hero.name = hero_name
        hero.description = '{0} description'.format(hero_name)
        hero.universe = universe
        hero.save()
        return hero


if __name__ == '__main__':
    unittest.main()