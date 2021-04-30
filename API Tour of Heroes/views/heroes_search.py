from flask import request
from flask_restful import Resource

from models.hero import Hero


class HeroesSearchHandler(Resource):
    """Heroes search handler"""
    def get(self):
        """Search heroes"""
        try:
            #Fazendo a consulta no banco de dados
            heroes = Hero.search(request.args.get('name'))
            response = {
                'heroes': []
            }

            #Percorrendo os heróis e transformando em json
            for hero in heroes:
                response['heroes'].append(hero.to_dict())
            #Retornando o resultado
            if heroes:
                return response['heroes']
            return {'message': 'Hero not found'}, 404

        except Exception as error:
            return {
                'message': 'Bad request, param name is required',
            }, 400
