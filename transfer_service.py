import datetime
import uuid
import os
from reposit import get_manager

from email_service.emails import Email_Worker


class TransferService:
    def __init__(self, expeditaire, destinateur, montant):
        self.expeditaire = expeditaire
        self.destinateur = destinateur
        self.montant = montant
        self.date = datetime.datetime.now().strftime("%d/%m/%Y %H:%M ")
        self.transaction = str(uuid.uuid4())

    def transferer(self):
        self.expeditaire.transferer(self.expeditaire, self.destinateur, self.montant)

        # envoyer l'email
        message = f"Vous avez reussi un transfert de {self.expeditaire.nom}\n d'un montant de • {self.montant} •\n le {self.date}  " # le message
        ok = False
        while not ok:
            try:
                Email_Worker.envoi_email(self.destinateur.email, message=message)
                ok = True
            except:
                continue



        historique = (
            f"{self.expeditaire.nom}  {self.expeditaire.prenom}",
            f"{self.destinateur.nom}  {self.destinateur.prenom}",
            self.montant,
            self.date
        )
        
        
        base = get_manager()
        base.sauvegarde_transaction(historique)




