from page_transfer import Transfer
import sys
from PySide6 import QtWidgets
from PySide6.QtWidgets import QMessageBox
from  comptservice import ServieCompte


class Expe(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Tranfert')
        self.setupUi()
        self.connexion()
        self.populate_user()


    def setupUi(self):
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.setContentsMargins(15, 15, 15, 15)
        self.main_layout.setSpacing(16)

        self.btn_verifie = QtWidgets.QPushButton('Verifie')
        self.btn_verifie.setFixedWidth(100)

        top_bar = QtWidgets.QHBoxLayout()
        top_bar.setSpacing(8)
        top_bar.addWidget(self.btn_verifie)
        top_bar.addStretch(1)
        self.main_layout.addLayout(top_bar)

        form_card = QtWidgets.QFrame()
        form_card.setObjectName("info_card")
        form_card.setFrameShape(QtWidgets.QFrame.StyledPanel)
        form_card_layout = QtWidgets.QFormLayout(form_card)
        form_card_layout.setContentsMargins(16, 16, 16, 16)
        form_card_layout.setSpacing(12)
        title_label = QtWidgets.QLabel("<h1 style= 'color:cyan; text-align: center; margin:top'>L'expediteur(e)</h1>")
        self.main_layout.addWidget(title_label)

        self.comb = QtWidgets.QComboBox()
        self.list_users = QtWidgets.QListWidget()



        contenu_layout = QtWidgets.QHBoxLayout()
        contenu_layout.setSpacing(10)

        self.edit_password = QtWidgets.QLineEdit()
        self.edit_password.setPlaceholderText("Entrez le mot de pass")
        self.edit_password.setEchoMode(QtWidgets.QLineEdit.Password)


        form_card_layout.addRow("Contacts", self.comb)
        form_card_layout.addWidget(self.list_users)
        form_card_layout.addRow('Mot de pass',self.edit_password)


        contenu_layout.addWidget(form_card, 1)
        contenu_layout.addWidget(self.btn_verifie, 0)
        self.main_layout.addLayout(contenu_layout, 2)


    def connexion(self):
        self.comb.currentTextChanged.connect(self.show_user)
        self.btn_verifie.clicked.connect(self.verification)


    def populate_user(self) :
        users = ServieCompte.get_users()
        for user in users :
            text = f"{user._id} | {user.nom} | {user.prenom} | {user.age} ans | {user.sexe}"
            self.comb.addItem(text, user)


    def show_user(self):
        user_selected = self.comb.currentData()
        text = f"{user_selected._id} | {user_selected.nom} | {user_selected.prenom} | {user_selected.age} ans | {user_selected.sexe}"
        if self.list_users.count() >= 1:
            self.list_users.clear()
        self.list_users.addItem(text)


    def verification(self):
        user = self.comb.currentData()
        self.page = Transfer(expediteur=user)
        edit_password = self.edit_password.text()
        if user._mdp == edit_password:
            self.edit_password.setText("")
            self.page.show()
        else:
            QMessageBox.information(self, "Log", "mot de passe Incorrect")




if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    with open('assets/styles.qss', 'r') as file:
        app.setStyleSheet(file.read())
    window = Expe()
    window.show()
    sys.exit(app.exec())









