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
                'universe': 'DC',
                'imageUrl': 'https://super.abril.com.br/wp-content/uploads/2018/09/superman.png?w=1024'
            }
        }

        response = self.app.post(path='/heroes', json=hero_dict)

        # Conferindo se voltou 200
        self.assertEqual(response.status_code, 200)

        # Conferindo a resposta da requisição
        self.assertIsNotNone(response.get_json())
        self.assertIsNotNone(response.get_json()['id'])

    def test_create_hero_without_name(self):
        """Test create hero without name"""
        params = {
            'hero': {
                'name': '',
                'description': '',
                'universe': 'DC',
                'imageUrl': 'https://image.com.br/image.jpg'
            }
        }
        response = self.app.post(path='/heroes', json=params)
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.get_json()['details'],
                         'Bad request, name is required')

    def test_create_hero_with_name_formatted(self):
        """Test create hero with uppercase name and blank spaces"""
        params = {
            'hero': {
                'name': ' SUPERMAN ',
                'description': 'Hero description',
                'universe': 'DC',
                'imageUrl': 'https://image.com.br/image.jpg'
            }
        }
        response = self.app.post(path='/heroes', json=params)
        self.assertEqual(response.status_code, 200)

        # Obtendo o heroi no banco de dados para conferir o nome
        hero_updated = Hero.get_hero(response.get_json()['id'])
        self.assertEqual(hero_updated.name, 'Superman')

    def test_create_hero_with_invalid_universe(self):
        """Test create hero with invalid universe"""
        params = {
            'hero': {
                'name': ' SUPERMAN ',
                'description': 'Hero description',
                'universe': 'x-men',
                'imageUrl': 'https://image.com.br/image.jpg'
            }
        }
        response = self.app.post(path='/heroes', json=params)
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.get_json()['details'],
                         'Bad request, invalid universe')

    def test_create_hero_with_invalid_url(self):
        """Test create hero with invalid url"""
        params = {
            'hero': {
                'name': 'Superman',
                'description': 'Superman description',
                'universe': 'DC',
                'imageUrl': ''
            }
        }
        response = self.app.post(path='/heroes', json=params)
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.get_json()['details'],
                         'Bad request, invalid image url')

    def test_create_hero_with_formatted_description(self):
        params = {
            'hero': {
                'name': 'SUPERMAN',
                'description': '          hero description         ',
                'universe': 'DC',
                'imageUrl': 'https://image.com.br/image.jpg'
            }
        }
        response = self.app.post(path='/heroes', json=params)
        self.assertEqual(response.status_code, 200)

        # Obtendo o heroi no banco de dados para conferir a descrição
        hero_updated = Hero.get_hero(response.get_json()['id'])
        self.assertEqual(hero_updated.description, 'Hero description')

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
        # Fazendo a segunda consulta enviando o cursor retornado
        cursor = response.get_json()['cursor']

        response = self.app.get(path='/heroes?cursor=' + cursor)

        # Conferindo se voltou 200
        self.assertEqual(response.status_code, 200)

        # Conferindo a quantidade de herois que voltou no json
        # Na primeira requisiçao voltou 16 herois entao precisa retornar mais 4
        self.assertEqual(len(response.get_json()['heroes']), 4)

    @staticmethod
    def create_hero(hero_name, universe):
        hero = Hero()
        hero.name = hero_name
        hero.description = '{0} description'.format(hero_name)
        hero.universe = universe
        hero.save()
        return hero

    def test_get_hero(self):
        """Test get hero"""
        # Criando o heroi e salvando o id
        hero_id = self.create_hero('Hero', 'dc').id

        # Enviando a requisição para obter o heroi
        response = self.app.get('/hero/{0}'.format(hero_id))
        self.assertEqual(response.status_code, 200)

        # Pegando o json da resposta
        hero_dict = response.get_json()
        self.assertEqual(hero_dict['name'], 'Hero')
        self.assertEqual(hero_dict['id'], hero_id)

    def test_get_hero_not_found(self):
        """Test get hero not found"""
        # Enviando a requisição para obter o heroi
        response = self.app.get('/hero/id_aleatorio')

        # A requisição vai voltar 404 pois não existe nenhum heroi com esse id
        self.assertEqual(response.status_code, 404)

        # Json retornado
        self.assertDictEqual(
            response.get_json(),
            {'message': 'Hero not found'}
        )

    def test_update_hero(self):
        """Test update hero"""
        # Criando o heroi
        hero = self.create_hero('Hero', 'DC')
        # Enviando a requisição para obter o heroi
        params = {
            'hero': {
                'name': 'Hawkwoman',
                'description': hero.description,
                'universe': hero.universe,
                'imageUrl': 'https://exitoina.uol.com.br/media/_versions/mulher_gaviao_3_widexl.jpg'
            }
        }
        response = self.app.post(path='/hero/{0}'.format(hero.id), json=params)

        # Resposta da requisição
        self.assertEqual(response.status_code, 200)

        # Obtendo o heroi atualizado para conferir o novo nome
        hero_updated = Hero.get_hero(hero.id)
        self.assertEqual(hero_updated.name, 'Hawkwoman')

    def test_delete_hero(self):
        """Test delete hero"""
        # Criando o heroi
        hero = self.create_hero('Hero', 'DC')

        # Enviando a requisição para excluir o heroi
        response = self.app.delete(path='/hero/{0}'.format(hero.id))

        # Resposta da requisição
        self.assertEqual(response.status_code, 200)

        # Conferindo a mensagem que voltou
        self.assertEqual(response.get_json(), {'message': 'Hero deleted'})
        # Obtendo o heroi diretamente no banco de dados para conferir se foi
        # excluido mesmo
        self.assertIsNone(Hero.get_hero(hero.id))


if __name__ == '__main__':
    unittest.main()
