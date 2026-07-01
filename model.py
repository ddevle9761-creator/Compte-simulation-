
import os
import json



CUR_DIR = os.path.dirname(__file__)
DATA_FILE = os.path.join(CUR_DIR, "data", "user.json")
os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)



class Compte:
    id = 0
    def __init__(self, nom: str,prenom: str,age: int, sexe: str, email: str, _mdp: str,numero:int , _solde: int,  _id = None):
        if _id is None :
            self._id = Compte.id_user(Compte.id)
            Compte.id += 1
        self.nom = nom
        self.prenom = prenom
        self.age = age
        self.sexe = sexe
        self.email = email
        self._mdp = _mdp
        self._solde = _solde
        self.numero = numero

    # pour l'attribution des id
    @classmethod
    def id_user(cls, id):
        for cls in Compte.__subclasses__():
            if cls.id == id :
                Compte.id = cls.id
        return cls.id


    
    @classmethod
    def check_user(cls, u) :
        return isinstance(u, cls)

    def deposer(self, montant) -> bool :
        if montant <= 0 :
            return False
        self._solde += montant
        return True

    def retirer(self, montant) -> bool :
        if montant > self._solde :
            return False
        self._solde -= montant
        return True

    @property
    def solde(self) :
        return self._solde


    def to_dict(self) :
        return {
            "_id" : self._id,
            "nom" : self.nom,
            "prenom" : self.prenom,
            "age" : self.age,
            "sexe" : self.sexe,
            "email" : self.email,
            "_mdp" : self._mdp,
            'numero': self.numero,
            "_solde" : self.solde,
        }

    @classmethod
    def from_dict(cls, data) :
        return cls(
                   data['nom'],
                   data['prenom'],
                   data['age'],
                   data['sexe'],
                   data['email'],
                   data['_mdp'],
                   data['_solde'],
                   data['numero'],
                   data['_id']
                   )

    @staticmethod
    def _get_users():
        if not os.path.exists(DATA_FILE):
            return []
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                return []
            return data or []

    def update(self, us):
        self.nom = us.nom
        self.prenom = us.prenom
        self.age = us.age
        self.sexe = us.sexe
        self._mdp = us._mdp
        self.numero = us.numero
        self.email = us.email
        self._solde = us._solde
        return self


    def envoyer(self, dst, montant):
        ok = False
        if montant <= 0:
            raise ValueError('Montant invalide')
        if self._solde < montant :
            raise ValueError('Solde insuffisant')
        self._solde -= montant
        dst.recevoir(montant)
        ok = True
        return ok


    def recevoir(self, montant:int):
        if montant <= 0 :
            raise ValueError('Montant invalide')
        self._solde += montant
        return True


    def transferer(self, exp, dst, montant):
        if montant <= 0 or exp._solde <= 0 or montant >= exp._solde :
            raise ValueError('Montant invalide')
        else:
            exp._solde -= montant
            dst.recevoir(montant)



    def show_info(self):
        return f"Id : {self._id} • Nom : {self.nom} • Prénom : {self.prenom} • Âge : {self.age} • Sexe : {self.sexe} • Email : {self.email} • Mot de pass : {self._mdp} • Solde : {self._solde} fcfa"


    def __str__(self) :
            return f"•Id : {self._id} •Nom : {self.nom} •Prenom : {self.prenom} •Âge : {self.age} •Sexe {self.sexe} •Email {self.email}"

def get_manager(file_path=None):
    from sauvegarde_json import get_manager as _get_manager
    return _get_manager(file_path)


if __name__ == '__main__':
    manager = get_manager()



