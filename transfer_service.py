import datetime
import uuid
import os
from sauvegarde_json import get_manager



class TransferService:
    def __init__(self, expeditaire, destinateur, montant):
        self.expeditaire = expeditaire
        self.destinateur = destinateur
        self.montant = montant
        self.date = datetime.datetime.now().strftime("%d/%m/%Y %H:%M ")
        self.transaction = str(uuid.uuid4())

    def transferer(self):
        self.expeditaire.transferer(self.expeditaire, self.destinateur, self.montant)

        historique = {
            'transaction_id': self.transaction,
            'source': self.expeditaire.nom,
            'destination': self.destinateur.nom,
            'montant': self.montant,
            'date': self.date
        }
        
        
        jm = get_manager(file_path=os.path.join('data', 'transaction.json'))
        histo = jm.list_transactions()
        histo = [e for e in histo if e.get('transaction_id') != self.transaction]
        histo.append(historique)
        jm.save_transaction(histo)



