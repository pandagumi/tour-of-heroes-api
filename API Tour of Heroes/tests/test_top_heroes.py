"""Top Heroes test case"""
import unittest

from mock import patch
from mockfirestore import MockFirestore

from main import app
from models.hero import Hero


class TopHeroesHandlerTestCase(unittest.TestCase):
    """Top Heroes handler"""

    def setUp(self):
        """SetUp é chamado no inicio de cada teste"""
        self.mock_db = MockFirestore()
        self.patcher = patch(
            'modules.main.MainModule.get_firestore_db',
            return_value=self.mock_db)
        self.patcher.start()
        # Nessa linha vamos iniciar a API nos testes
        self.app = app.test_client()

    def tearDown(self):
        """O tearDown é chamado no final de cada teste"""
        self.patcher.stop()
        self.mock_db.reset()

    @staticmethod
    def create_hero(hero_name, universe):
        """Create a hero for tests"""
        hero = Hero()
        hero.name = hero_name
        hero.description = '{0} description'.format(hero_name)
        hero.universe = universe
        hero.save()
        return hero

    def test_get_top_heroes(self):
        """Test get top heroes"""
        # Aqui vamos fazer um loop e criar 20 herois
        # E o nome vai ser hero + index do loop, ex: "Hero 1"
        for index in range(1, 21):
            self.create_hero('Hero {0}'.format(index), 'marvel')

        # Fazendo a primeira consulta a url e conferindo a resposta
        response = self.app.get(path='/top-heroes')
        first_hero_list = response.get_json()['heroes']
        self.assertEqual(len(first_hero_list), 4)
        self.assertEqual(response.status_code, 200)

        # Fazendo a segunda consulta a url e conferindo a resposta
        response = self.app.get(path='/top-heroes')
        self.assertEqual(response.status_code, 200)
        second_hero_list = response.get_json()['heroes']
        self.assertEqual(len(second_hero_list), 4)

        # Comparando as duas listas para ver se são diferentes
        # Pois essa url precisa sempre retornar herois diferentes
        self.assertNotEqual(first_hero_list, second_hero_list)


if __name__ == '__main__':
    unittest.main()