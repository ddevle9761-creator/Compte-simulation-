import sys

from PySide6 import QtWidgets, QtCore
from comptservice import ServieCompte
from PySide6.QtWidgets import QGraphicsOpacityEffect, QMessageBox
from PySide6.QtCore import QPropertyAnimation




class Page_user(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.main_layout = None
        self.setWindowTitle("Transfer Compte")
        self.setup_ui()
        self.setup_connexion()
        self.populate_user()



    def setup_ui(self):
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.setContentsMargins(16, 16, 16, 16)
        self.main_layout.setSpacing(16)
        # En-tête et barre d'actions
        titre = QtWidgets.QLabel("<i>Utilisateurs</i>")
        titre.setStyleSheet("font-size: 18px; font-weight: 700; color: #87CEEB;")
        sous_titre = QtWidgets.QLabel("Ajouter, sélectionner et afficher les comptes enregistrés.")
        sous_titre.setStyleSheet("color: #94A3B8; font-size: 13px;")
        sous_titre.setWordWrap(True)

        # créer les boutons d'action (ils seront placés en bas de la page)
        self.Btn_add_user = QtWidgets.QPushButton("Ajouter")
        self.Btn_add_user.setObjectName('btn-primary')
        self.Btn_remove_user = QtWidgets.QPushButton("Supprimer")
        self.Btn_remove_user.setObjectName('btn-logout')
        self.Btn_show_info = QtWidgets.QPushButton('Afficher')
        self.Btn_show_info.setObjectName('btn-primary')
        self.Btn_refresh = QtWidgets.QPushButton('Rafraîchir')
        self.Btn_refresh.setObjectName('btn-primary')

        # Ajustement UI taille des boutons
        for b in (self.Btn_add_user, self.Btn_remove_user, self.Btn_show_info, self.Btn_refresh):
            b.setFixedHeight(36)
            b.setCursor(QtCore.Qt.PointingHandCursor)

        self.main_layout.addWidget(titre)
        self.main_layout.addWidget(sous_titre)


        self.contenu_layout = QtWidgets.QHBoxLayout()
        self.contenu_layout.setSpacing(18)

       
        form_card = QtWidgets.QFrame()
        form_card.setObjectName("info_card")
        form_card.setFrameShape(QtWidgets.QFrame.StyledPanel)
        form_card_layout = QtWidgets.QFormLayout(form_card)
        form_card_layout.setContentsMargins(16, 16, 16, 16)
        form_card_layout.setSpacing(12)

        self.nom_input = QtWidgets.QLineEdit()
        self.prenom_input = QtWidgets.QLineEdit()
        self.age_input = QtWidgets.QSpinBox()
        self.age_input.setRange(1, 150)
        self.age_input.setValue(18)
        self.sexe_input = QtWidgets.QLineEdit()
        self.numero_input = QtWidgets.QLineEdit()
        self.email_input = QtWidgets.QLineEdit()
        self.mdp = QtWidgets.QLineEdit()
        self.mdp.setEchoMode(QtWidgets.QLineEdit.Password)
        self.solde = QtWidgets.QSpinBox()
        self.solde.setRange(0, 100000)

        self.nom_input.setPlaceholderText("Nom")
        self.prenom_input.setPlaceholderText("Prénom")
        self.sexe_input.setPlaceholderText("Sexe")
        self.numero_input.setPlaceholderText("Numéro")
        self.email_input.setPlaceholderText("Email")
        self.mdp.setPlaceholderText("Mot de passe")
        self.solde.setPrefix("FCFA ")

        form_card_layout.addRow("Nom", self.nom_input)
        form_card_layout.addRow("Prénom", self.prenom_input)
        form_card_layout.addRow("Âge", self.age_input)
        form_card_layout.addRow("Sexe", self.sexe_input)
        form_card_layout.addRow("Email", self.email_input)
        form_card_layout.addRow("Numéro", self.numero_input)
        form_card_layout.addRow("Mot de passe", self.mdp)
        form_card_layout.addRow("Solde de départ", self.solde)

        

        self.contenu_layout.addWidget(form_card, 3)

        
        right_card = QtWidgets.QFrame()
        right_card.setObjectName("info_card")
        right_layout = QtWidgets.QVBoxLayout(right_card)
        right_layout.setContentsMargins(16, 16, 16, 16)
        right_layout.setSpacing(12)

        self.list_user = QtWidgets.QListWidget()
        self.list_user.setSelectionMode(QtWidgets.QListWidget.ExtendedSelection)
        self.list_user.setObjectName('user_list')
        self.list_user.setMinimumWidth(300)

        try:
            self.list_user.setWordWrap(True)
        except Exception:
            pass

        btn_layout = QtWidgets.QHBoxLayout()
        btn_layout.addWidget(self.Btn_show_info)
        btn_layout.addWidget(self.Btn_refresh)

        self.info_user = QtWidgets.QFrame()
        self.info_user.setObjectName('info_card')
        self.info_layout = QtWidgets.QFormLayout(self.info_user)
        self.info_layout.setContentsMargins(12, 12, 12, 12)
        self.info_layout.setSpacing(10)

        right_layout.addWidget(QtWidgets.QLabel("Liste des utilisateurs"))
        right_layout.addWidget(self.list_user)
        right_layout.addLayout(btn_layout)
        right_layout.addWidget(QtWidgets.QLabel("Informations sélectionnées"))
        right_layout.addWidget(self.info_user)

        self.contenu_layout.addWidget(right_card, 4)
        self.main_layout.addLayout(self.contenu_layout)


        sep = QtWidgets.QFrame()
        sep.setFrameShape(QtWidgets.QFrame.HLine)
        sep.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.main_layout.addWidget(sep)

        bottom_bar = QtWidgets.QHBoxLayout()
        bottom_bar.setSpacing(12)
        bottom_bar.addStretch(1)
        bottom_bar.addWidget(self.Btn_add_user)
        bottom_bar.addWidget(self.Btn_remove_user)
        bottom_bar.addWidget(self.Btn_show_info)
        bottom_bar.addWidget(self.Btn_refresh)
        self.main_layout.addLayout(bottom_bar)

    def animation_info_user(self):
        self.effet = QGraphicsOpacityEffect()
        self.info_user.setGraphicsEffect(self.effet)

        self.anim = QPropertyAnimation(self.effet, b"opacity")
        self.anim.setDuration(1000)
        self.anim.setStartValue(0.0)
        self.anim.setEndValue(1.0)
        self.anim.start()


    def setup_connexion(self):
        self.Btn_add_user.clicked.connect(self.add_user)
        self.Btn_remove_user.clicked.connect(self.remove_user)
        self.Btn_show_info.clicked.connect(self.show_selected_user)
        self.Btn_refresh.clicked.connect(self.populate_user)
        self.list_user.itemClicked.connect(self.show_user)



    def populate_user(self):
        self.list_user.clear()
        users = ServieCompte.get_users()
        for i, user in enumerate(users):
            text = f"{i} • {user[1]} {user[2]}"
            item = QtWidgets.QListWidgetItem(text)
            item.setData(QtCore.Qt.UserRole, user)
            self.list_user.addItem(item)
        return



    def add_user(self):
        n = self.nom_input.text()
        p = self.prenom_input.text()
        a = self.age_input.value()
        s = self.sexe_input.text()
        e = self.email_input.text()
        m = self.mdp.text()
        so = self.solde.value()
        num = self.numero_input.text()

        ok_email = ServieCompte.check_email(email=e)
        ok_num = ServieCompte.check_number(number=num)

        if not n or len(n) <3 or not p or len(p) <3 or a < 18 or not s or len(m) < 8 or so <= 0 or not ok_email or not ok_num:

            QMessageBox.warning(self, 'Erreur', 'Veuillez remplir correctement les champs')
            return
        u = ServieCompte(nom=n, prenom=p, age=a, sexe=s, mdp=m, solde=so, email=e, numero=num, id=None)
        if not u.check_user(u):
            QMessageBox.warning(self, 'Erreur', 'Utilisateur invalide')
            return
        u.save()
        QMessageBox.information(self, 'Succès', 'Utilisateur ajouté')
        self.nom_input.setText("")
        self.prenom_input.setText("")
        self.sexe_input.setText("")
        self.mdp.setText("")
        self.numero_input.setText("")
        self.email_input.setText("")
        self.solde.setValue(0)
        self.age_input.setValue(19)
        
        return

    def remove_user(self):
        selected_items = self.list_user.selectedItems()
        if not selected_items:
            return False

        for list_item in selected_items:
            user = list_item.data(QtCore.Qt.UserRole)
            user.remove_user()
            self.list_user.takeItem(self.list_user.row(list_item))
        QtWidgets.QMessageBox(text='Supprimé avec succès', parent=self,).exec()
        return


    def show_user(self, item):
        user = item.data(QtCore.Qt.UserRole)
        if user is None :
            QtWidgets.QMessageBox(text='Impossible de charger les informations de l\'utilisateur.', parent=self).exec()
            return

        for i in reversed(range(self.info_layout.count())):
            item = self.info_layout.takeAt(i)
            if item.widget():
                item.widget().deleteLater()

        lbl_id = QtWidgets.QLabel(f'{user[0]}')
        lbl_nom = QtWidgets.QLabel(user[1])
        lbl_prenom = QtWidgets.QLabel(user[2])
        lbl_age = QtWidgets.QLabel(f"{user[3]} ans")
        lbl_sexe = QtWidgets.QLabel(user[4])
        lbl_email = QtWidgets.QLabel(user[6])
        lbl_numero = QtWidgets.QLabel(str(user[5]))
        lbl_solde = QtWidgets.QLabel(f"{user[8]} FCFA")

        for lbl in (lbl_id, lbl_nom, lbl_prenom, lbl_age, lbl_sexe, lbl_email, lbl_numero, lbl_solde):
            lbl.setWordWrap(True)

        self.info_layout.addRow("Id", lbl_id)
        self.info_layout.addRow("Nom", lbl_nom)
        self.info_layout.addRow("Prénom", lbl_prenom)
        self.info_layout.addRow("Âge", lbl_age)
        self.info_layout.addRow("Sexe", lbl_sexe)
        self.info_layout.addRow("Email", lbl_email)
        self.info_layout.addRow("Numéro", lbl_numero)
        self.info_layout.addRow("Solde", lbl_solde)

    def show_selected_user(self):
        item = self.list_user.currentItem()
        if item:
            self.show_user(item)






if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    with open("assets/styles.qss", "r") as f:
        app.setStyleSheet(f.read())
    win = Page_user()
    win.show()
    sys.exit(app.exec())