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
            heroes = Hero.get_heroes(request.args.get('cursor'))

            # Montando a resposta, por enquanto iremos deixar o cursor vazio
            response = {
                'cursor': None,
                'heroes': []
            }
            # Vamos percorer os herois e transformar em json
            for hero in heroes:
                response['heroes'].append(hero.to_dict())

            # Adicionando o cursor no resultado da consulta
            if len(response['heroes']) == 16:
                response['cursor'] = response['heroes'][-1]['id']

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


class HeroHandler(Resource):
    """Hero handler"""

    def get(self, hero_id):
        """Get hero"""
        try:
            # Fazendo a consulta no banco
            hero = Hero.get_hero(hero_id)

            # Transformando em json
            return hero.to_dict()

        except Exception:
            return {
                       'message': 'Hero not found',

                   }, 404

    def post(self, hero_id):
        """Update a hero"""
        try:
            # Obtendo os valores no banco

            if not request.is_json or 'hero' not in request.json:
                return {'message': 'Bad request'}, 400

            hero_update = Hero.get_hero(hero_id)
            hero = HeroModule.update(hero_update, request.json['hero'])
            return hero

        except Exception as error:
            return {
                       'message': 'Error on update hero',
                       'details': str(error)
                   }, 500

    def delete(self, hero_id):
        """Delete hero"""
        try:
            Hero.delete(hero_id)
            return {'message': 'Hero deleted'}

        except Exception as error:
            return {
                       'message': 'Error on delete hero',
                       'details': str(error)
                   }, 500
