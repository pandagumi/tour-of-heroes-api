"""Hero model"""
import uuid

from modules.main import MainModule


class Hero(object):
    """Hero"""

    # Nessa variável vamos colocar o nome da coleção para ser salvo no banco de dados
    _collection_name = 'Hero'

    # Ao instanciar a nossa classe hero o metodo __init__ sempre é chamado
    def __init__(self, **args):
        # Aqui vamos já deixar os campos
        self.id = args.get('id', uuid.uuid4().hex)
        self.name = args.get('name')
        self.description = args.get('description')
        self.universe = args.get('universe')
        self.imageUrl = args.get('imageUrl')

    def save(self):
        """Save hero"""
        MainModule.get_firestore_db().collection(
            self._collection_name).document(self.id).set(self.to_dict())

    def to_dict(self):
        """Transform hero in dict format"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'universe': self.universe,
            'imageUrl': self.imageUrl
        }

    @classmethod
    def get_hero(cls, hero_id):
        """Get hero"""
        hero = MainModule.get_firestore_db().collection(
            cls._collection_name).document(hero_id).get()
        if hero.exists:
            return Hero(**hero.to_dict())
        return None

    @classmethod
    def get_heroes(cls):
        """Get heroes"""
        return MainModule.get_firestore_db().collection(
            cls._collection_name).limit(16).stream()

    @classmethod
    def delete(cls, hero_id):
        """Delete a hero by id"""
        hero = MainModule.get_firestore_db().collection(
            cls._collection_name).document(hero_id).get()
        if hero.exists:
            MainModule.get_firestore_db().collection(
                cls._collection_name).document(hero_id).delete()
