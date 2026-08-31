import os
import tempfile
import unittest

from sauvegarde_json import JsonManager
from comptservice import ServieCompte



class TestCompteService(unittest.TestCase):
    def setUp(self):
        self.test_file = os.path.join(tempfile.gettempdir(), 'cine_test_user.json')

        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        
        import sauvegarde_json
        sauvegarde_json._DEFAULT_MANAGER = JsonManager(self.test_file)
        self.jm = sauvegarde_json._DEFAULT_MANAGER

    def test_premier_t(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        
    def test_deuxieme_t(self):
        # start empty
        self.jm.save_user([])
        user = ServieCompte(nom='t', prenom='t', age=30, sexe='M', mdp='p', email='t@example.com', solde=100, numero=10101)
        self.assertTrue(user.save())
        users = self.jm.charger_json()
        self.assertTrue(any(u.get('email') == 't@example.com' for u in users))

    def test_triosiem_t(self):
        self.jm.save_user([])
        user = ServieCompte(nom='d', prenom='d', age=25, sexe='F', mdp='p', email='d@example.com', solde=100, numero=101010)
        self.assertTrue(user.save())
        # deposit
        self.assertTrue(user.transacter(50, action='depot'))
        users = self.jm.charger_json()
        u = next((x for x in users if x.get('email') == 'd@example.com'), None)
        self.assertIsNotNone(u)
        self.assertEqual(u.get('_solde'), 150)

    def test_quatrien(self):
        self.jm.save_user([])
        user = ServieCompte(nom='r', prenom='r', age=40, sexe='M', mdp='p', email='r@example.com', solde=10, numero=101010)
        self.assertTrue(user.save())

        self.assertFalse(user.transacter(20, action='retrait'))
        users = self.jm.charger_json()
        u = next((x for x in users if x.get('email') == 'r@example.com'), None)
        self.assertIsNotNone(u)
        self.assertEqual(u.get('_solde'), 10)

    def test_dernier_test(self):
        self.jm.save_user([])
        user = ServieCompte(nom='x', prenom='x', age=22, sexe='F', mdp='p', email='x@example.com', solde=5, numero=1211)
        self.assertTrue(user.save())

        self.assertTrue(user.remove_user)
        users = self.jm.charger_json()
        self.assertFalse(any(u.get('email') == 'x@example.com' for u in users))

  


if __name__ == '__main__':
    unittest.main()
