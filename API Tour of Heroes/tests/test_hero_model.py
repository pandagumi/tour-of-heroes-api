"""Test hero model"""
import unittest
from mock import patch
from mockfirestore import MockFirestore
from modules.main import MainModule
from models.hero import Hero


class TestHeroModel(unittest.TestCase):
    """Test hero model"""

    @staticmethod
    def create_hero(hero_name, universe):
        hero = Hero()
        hero.name = hero_name
        hero.description = '{0} description'.format(hero_name)
        hero.universe = universe
        hero.save()
        return hero

    def setUp(self):
        """SetUp é chamado no inicio de cada teste"""
        self.mock_db = MockFirestore()
        self.patcher = patch(
            'modules.main.MainModule.get_firestore_db', return_value=self.mock_db)
        self.patcher.start()

    def tearDown(self):
        """O tearDown é chamado no final de cada teste"""
        self.patcher.stop()
        self.mock_db.reset()

    def test_save_and_get_hero(self):
        """Test save and get hero"""
        # Criando o novo heroi
        new_hero = Hero()
        new_hero.name = 'Superman'
        new_hero.description = 'Superman'
        new_hero.universe = 'dc'
        new_hero.save()

        # Obtendo o heroi pelo id
        hero = Hero.get_hero(new_hero.id)
        self.assertEqual(hero.name, 'Superman')
        self.assertEqual(hero.id, new_hero.id)

    def test_get_hero_not_found(self):
        """Test get hero with id not found"""
        hero = Hero.get_hero('ID_TEST')
        self.assertIsNone(hero)

    def test_get_heroes(self):
        """Test get heroes"""
        # Aqui vamos fazer um loop e criar 20 herois
        # E o nome vai ser hero + index do loop, ex: "Hero 1"
        for index in range(1, 21):
            self.create_hero('Hero {0}'.format(index), 'marvel')

        # Aqui vamos chamar o metodo para obter os herois
        heroes = Hero.get_heroes()
        # Percorrendo todos os herois e transformando eles em dict(json)
        heroes_dict = [hero.to_dict() for hero in heroes]
        # Consultando a quantidade de itens que retornou
        self.assertEqual(len(heroes_dict), 16)
        for hero in heroes_dict:
            self.assertTrue(hero['name'].startswith('Hero'))

    def test_delete_hero(self):
        """Test delete hero"""
        # Criando o heroi
        hero = self.create_hero('Joker', 'dc')
        # Excluindo o heroi
        Hero.delete(hero.id)

        # Consultando se o heroi foi mesmo excluido
        self.assertIsNone(Hero.get_hero(hero.id))
