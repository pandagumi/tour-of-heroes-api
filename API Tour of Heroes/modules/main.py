"""Main module"""
from firebase_admin import firestore


class MainModule(object):
    """Main module"""

    # Vamos criar esse metodo somente para ficar mais facil fazer o mock dele
    # nos testes
    @staticmethod
    def get_firestore_db():
        """Get firestore db instance"""
        return firestore.client()
