from sauvegarde_json import get_manager
from model import Compte


js = get_manager()

class ServieCompte(Compte):
    def __init__(self, nom, prenom, age, sexe, email, mdp, solde, numero, id = None  ):
       
        super().__init__(
            nom,
            prenom,
            age,
            sexe,
            email,
            mdp,
            numero,
            solde,
            _id=id,
        )
      
        if id is not None:
            self._id = id

    def save(self):
        data = {'_id': self._id,
            "nom":self.nom,
            'prenom': self.prenom,
            'age': self.age,
            'sexe': self.sexe,
            'email': self.email,
            'numero': self.numero,
            '_mdp':self._mdp,
            '_solde': self.solde
            }

        jm = get_manager()
        users = jm.charger_json()
        users = [e for e in users if e.get('_id') != self._id]
        users.append(data)
        jm.save_user(users)
        return True

    def remove_user(self):
        jm = get_manager()
        users = jm.charger_json()
        users = [e for e in users if e.get("_id") != self._id]
        jm.save_user(users)
        return True




    def update_user(self, u):
        if self.check_user(u):
            self.update(u)
            return True
        return False


    @staticmethod
    def get_users():
        users_all = ServieCompte._get_users()
        result = []
        for u in users_all:
            result.append(ServieCompte(
                nom=u.get('nom'),
                prenom=u.get('prenom'),
                age=u.get('age'),
                sexe=u.get('sexe'),
                email=u.get('email'),
                mdp=u.get('_mdp'),
                solde=u.get('_solde'),
                numero=u.get('numero'),
                id=u.get('_id')
            ))
        return result

    @staticmethod
    def _get_users():
        jm = get_manager()
        return jm.charger_json()

    def show_user(self):
        return self.show_info()

    def deposer(self, value):
        return super().deposer(value)

    def retirer(self, value):
        return super().retirer(value)

    def transacter(self, montant, action='depot'):
        if action == 'depot':
            ok = self.deposer(montant)
        elif action == 'retrait':
            ok = self.retirer(montant)
        else:
            return False
        if ok:
            return self.save()
        return False

    def transferer(self, exp, dst, montant):
        if montant <= 0 or exp._solde <= 0 or montant >= exp._solde:
            raise ValueError('Solde insuffisant')
        exp._solde -= montant
        super().transferer(exp, dst, montant)


    @staticmethod
    def get_user_by_id(user_id):
        return next((u for u in ServieCompte.get_users() if u._id == user_id), None)



if __name__ == '__main__':
    manager = get_manager()


