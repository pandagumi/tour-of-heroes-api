"""Heroes test case"""
import unittest
from main import app
from mock import patch
from mockfirestore import MockFirestore

from models.hero import Hero


class HeroesHandlerTestCase(unittest.TestCase):
    """Heroes handler"""

    def setUp(self):
        """SetUp é chamado no inicio de cada teste"""
        self.mock_db = MockFirestore()
        self.patcher = patch(
            'modules.main.MainModule.get_firestore_db', return_value=self.mock_db)
        self.patcher.start()
        self.app = app.test_client()

    def tearDown(self):
        """O tearDown é chamado no final de cada teste"""
        self.patcher.stop()
        self.mock_db.reset()

    def test_create_a_new_hero(self):
        """This test should create a new hero"""
        hero_dict = {
            'hero': {
                'name': 'Superman',
                'description': 'Superman description',
                'universe': 'dc',
                'imageUrl': 'https://super.abril.com.br/wp-content/uploads/2018/09/superman.png?w=1024'
            }
        }

        response = self.app.post(path='/heroes', json=hero_dict)

        # Conferindo se voltou 200
        self.assertEqual(response.status_code, 200)

        # Conferindo a resposta da requisição
        self.assertIsNotNone(response.get_json())
        self.assertIsNotNone(response.get_json()['id'])

    def test_get_heroes(self):
        """Test get this """
        # Aqui vamos fazer um loop e criar 20 herois
        # E o nome vai ser hero + index do loop, ex: "Hero 1"
        for index in range(1, 21):
            self.create_hero('Hero {0}'.format(index), 'marvel')

        response = self.app.get(path='/heroes')
        # Conferindo se voltou 200
        self.assertEqual(response.status_code, 200)
        # Conferindo se a chave do cursor esta retornando no json
        self.assertIn('cursor', response.get_json())
        # Conferindo a quantidade de herois que voltou no json
        self.assertEqual(len(response.get_json()['heroes']), 16)

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
