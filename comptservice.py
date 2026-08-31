from reposit import  get_manager
from model import Compte
import bcrypt

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

    @staticmethod
    def make_obj(user):
        return ServieCompte(
            id=None,
            nom=user.nom,
            prenom=user.prenom,
            age=user.age,
            sexe=user.sexe,
            numero=user.numero,
            email=user.email,
            mdp=user._mdp,
            solde=user._solde

        )


    def save(self):
        base = get_manager()
        base.sauvegarde_user(self.to_dict())
        return True


    def remove_user(self):
        base = get_manager()
        base.supprime_par_id(self._id)
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

    def deposer(self, value: int):
        if super().deposer(value):
            base = get_manager()
            if base.rechercher_par_id(self._id) is not None or isinstance(self._id, (int, str)):
                new_id = int(self._id)
                base.update_solde(self._solde, new_id)
            return True
        return False

    def retirer(self, value:int):
        if super().retirer(value):
            base = get_manager()
            if base.rechercher_par_id(self._id) is not None or isinstance(self._id, (int, str)):
                new_id = int(self._id)
                base.update_solde(self._solde, new_id)
            return True
        return False

    def transacter(self, montant:int, action='depot'):
        if action == 'depot':
            ok = self.deposer(int(montant))
        elif action == 'retrait':
            ok = self.retirer(montant)
        else:
            return False
        if ok:

            return True
        return False

    def transferer(self, exp, dst, montant):
        if montant <= 0 or exp._solde <= 0 or montant >= exp._solde or not exp.nom.isalpha():
            raise ValueError('Solde insuffisant')
        exp._solde -= montant
        super().transferer(exp, dst, montant)
        base = get_manager()
        if base.rechercher_par_id(self._id) is not None or isinstance(self._id, (int, str)):
            new_id = int(self._id)
            base.update_solde(self._solde, new_id)
            return True
        return False



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
        base = get_manager()
        user = base.rechercher_par_id(user_id)
        OBJET = ServieCompte(
            id=user_id,
            nom=user[1],
            prenom=user[2],
            age=user[3],
            sexe=user[4],
            numero=user[5],
            email=user[6],
            mdp=user[7],
            solde=user[8]

        )
        return {"ID": user_id,
                "Nom": OBJET.nom,
                "Prenom": OBJET.prenom,
                "Age": OBJET.age,
                "Sexe": OBJET.sexe,
                "Numero": OBJET.numero,
                "Email": OBJET.email,
                "Solde": OBJET.solde,
                "Mdp": OBJET._mdp
                }


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

    user = ServieCompte(nom='qa', prenom='daa', age=19, email='dfk', mdp='123', solde=100, numero=900, sexe='m')
    print(ser.transferer(dst=ser, exp=user, montant=10))
    print(ser._solde)
    print(user._solde)








