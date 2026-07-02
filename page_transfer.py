import sys
from transfer_service import TransferService
from PySide6 import QtWidgets, QtCore
from comptservice import ServieCompte
import datetime



class Transfer(QtWidgets.QWidget):
    def __init__(self, expediteur=None):
        super().__init__()
        self.expediteur = expediteur
        self.setWindowTitle('Tranfert')
        self.setupUi()
        self.connexion()
        self.populate_user()

    def setupUi(self):
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.setContentsMargins(15, 15, 15, 15)
        self.main_layout.setSpacing(12)

        top_bar = QtWidgets.QHBoxLayout()
        top_bar.setSpacing(8)

        top_bar.addStretch(1)
        self.main_layout.addLayout(top_bar)


        form_card = QtWidgets.QFrame()
        form_card.setObjectName("info_card")
        form_card.setFrameShape(QtWidgets.QFrame.StyledPanel)
        form_card_layout = QtWidgets.QFormLayout(form_card)
        form_card_layout.setContentsMargins(16, 16, 16, 16)
        form_card_layout.setSpacing(12)

        title_label = QtWidgets.QLabel("<h1 style='text-align:center; color: #fdb15b'>Transfert</h1>")
        self.main_layout.addWidget(title_label)

        self.comb = QtWidgets.QComboBox()
        self.list_users = QtWidgets.QListWidget()


        contenu_layout = QtWidgets.QHBoxLayout()
        contenu_layout.setSpacing(18)


        self.nom_input = QtWidgets.QLineEdit()
        self.prenom_input = QtWidgets.QLineEdit()
        self.solde = QtWidgets.QSpinBox(self)
        self.numero_input = QtWidgets.QLineEdit()
        self.btn_transfer = QtWidgets.QPushButton("Envoie")
        self.email =QtWidgets.QLineEdit()
        self.nom_input.setEnabled(False)
        self.prenom_input.setEnabled(False)
        self.numero_input.setEnabled(False)
        self.email.setEnabled(False)


        self.solde.setMinimum(1)
        self.nom_input.setPlaceholderText("Nom")
        self.prenom_input.setPlaceholderText("Prénom")
        self.solde.setPrefix("FCFA ")
        self.email.setPlaceholderText("Email")
        self.numero_input.setPlaceholderText("Numéro")
        self.btn_transfer.setMaximumWidth(200)


        form_card_layout.addRow("Nom", self.nom_input)
        form_card_layout.addRow("Prénom", self.prenom_input)
        form_card_layout.addRow("Numéro", self.numero_input)
        form_card_layout.addRow("Email", self.email)
        form_card_layout.addRow("Montant", self.solde)
        form_card_layout.addRow("Envoyer", self.btn_transfer)
        form_card_layout.addRow("Contacts", self.comb)

        form_card_layout.addWidget(self.list_users)
        contenu_layout.addWidget(form_card, 5)
        self.main_layout.addLayout(contenu_layout, 2)


    def connexion(self):
        self.comb.currentTextChanged.connect(self.show_user)
        self.btn_transfer.clicked.connect(self.envoie)

    def populate_user(self) :
        users = ServieCompte.get_users()
        for user in users :
           
            if self.expediteur is not None and getattr(user, '_id', None) == getattr(self.expediteur, '_id', None):
                continue
            text = f"{user._id} | {user.nom} | {user.prenom} | {user.age} ans | {user.sexe}"
            list_item = QtWidgets.QListWidgetItem(text)
            list_item.setData(QtCore.Qt.UserRole, user)
            self.comb.addItem(text, userData=user)



    def show_user(self):
        user = self.comb.currentData()
        if not user:
            return
        self.nom_input.setText(user.nom)
        self.prenom_input.setText(user.prenom)
        self.email.setText(user.email)
        self.numero_input.setText(user.numero)


    def envoie(self):
        dst = self.comb.currentData()
        if not dst:
            QtWidgets.QMessageBox(text='Veuillez sélectionner un destinataire', parent=self).exec()
            return

        users = ServieCompte.get_users()

        
        if self.expediteur is not None:
            sender = self.expediteur
        else:
            sender = next((u for u in users if getattr(u, '_id', None) != getattr(dst, '_id', None)), None)

        if sender is None:
            QtWidgets.QMessageBox(text='Aucun expéditeur disponible', parent=self).exec()
            return

        transfert = TransferService(expeditaire=sender, destinateur=dst, montant=self.solde.value())
        try:
            transfert.transferer()
        except Exception as e:
            QtWidgets.QMessageBox(text=str(e), parent=self).exec()
            return
        QtWidgets.QMessageBox(text='reussie', parent=self).exec()
        self.list_users.clear()
        self.list_users.addItem(f"Transfert de {sender.nom} . {sender.prenom}\nA "
                                f"{dst.nom} | {dst.prenom}\n"
                                f"Le {datetime.datetime.now().strftime("%d/%m/%Y %H:%M ")}"
                               )


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    with open('assets/styles.qss', 'r') as f:
        app.setStyleSheet(f.read())
    window = Transfer()
    window.show()
    sys.exit(app.exec())



