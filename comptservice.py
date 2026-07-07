from reposit import  get_manager
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

    def to_dict(self):
        return super().to_dict()

    def save(self):
        base = get_manager()
        base.sauvegarde_user(self.to_dict())
        return True

    def remove_user(self):
        user = manager.supprime_par_id(self._id)
        return True

    def update_user(self, u):
        if self.check_user(u):
            self.update(u)
            return True
        return False


    @staticmethod
    def get_users():
        return ServieCompte.__get_users__()

    @staticmethod
    def __get_users__():
        jm = get_manager()
        return jm.les_users()

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
        if montant <= 0 or exp._solde <= 0 or montant >= exp._solde or not exp.nom.isalpha():
            raise ValueError('Solde insuffisant')
        exp._solde -= montant
        super().transferer(exp, dst, montant)


    @staticmethod
    def check_email(email):
        find = '@gmail.com'
        if find in email :
            return True
        return False

    @staticmethod
    def check_number(number):
        if number.isdigit():
            return True
        return False


    @staticmethod
    def get_user_by_id(user_id):
        babe = get_manager()
        return babe.rechercher_par_id(user_id)

    @staticmethod
    def total_balance():
        montant = get_manager().total_balance()
        st = 0
        for i in range(len(montant)) :
            for row in montant :
                st += row[0]
        return st

    @staticmethod
    def total_age():
        us = get_manager().les_users()
        if len(us) != 0 :
            age = []
            for i in us:
                age.append(i[3])

            return round(sum(age) / len(us), 1)
        return 0







if __name__ == '__main__':
    manager = get_manager()
    ser = ServieCompte(nom='s', prenom='d', age=18, email='jd', mdp='123', solde=100, numero=900, sexe='m')

    print(manager.les_users())







