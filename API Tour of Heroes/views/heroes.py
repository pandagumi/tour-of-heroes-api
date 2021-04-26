"""Heroes view"""
from flask_restful import Resource
from flask import request

from models.hero import Hero
from modules.hero import HeroModule


class HeroesHandler(Resource):
    """Heroes handler"""

    def get(self):
        """Get heroes"""
        try:
            # Fazendo a consulta no banco de dados
            heroes = Hero.get_heroes()

            # Montando a resposta, por enquanto iremos deixar o cursor vazio
            response = {
                'cursor': None,
                'heroes': []
            }
            # Vamos percorer os herois e transformar em json
            for hero in heroes:
                response['heroes'].append(hero.to_dict())

            return response

        except Exception as error:
            return {
                       'message': 'Error on get heroes',
                       'details': str(error)
                   }, 500

    def post(self):
        """Create a new hero"""
        try:
            if not request.is_json or 'hero' not in request.json:
                return {'message': 'Bad request'}, 400

            hero = HeroModule.create(request.json['hero'])
            return hero.to_dict()

        except Exception as error:
            return {
                       'message': 'Error on create a new hero',
                       'details': str(error)
                   }, 500
