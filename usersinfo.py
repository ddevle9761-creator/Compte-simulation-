import sys
from comptservice import ServieCompte
from PySide6 import QtWidgets, Qt, QtCore
from PySide6.QtWidgets import QVBoxLayout, QPushButton, QLabel


class UsersInfo(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.layout_2 = QtWidgets.QHBoxLayout()
        self.setWindowTitle('Recherche des utilluisateurs')
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowState(QtCore.Qt.WindowMaximized)
        self.setup_ui()
        self.setup_connections()
        self.recuperer_les_noms()



    def setup_ui(self):
        self.topLayout = QVBoxLayout(self)
        info_label = QLabel("<h1><b>Information</b></h1>")
        info_label.adjustSize()

        self.topLayout.addWidget(info_label)
        self.topLayout.setSpacing(5)
        self.topLayout.setContentsMargins(1, 1, 1, 1)

        self.layout_1 = QtWidgets.QHBoxLayout()


        self.topLayout.addLayout(self.layout_1)



        self.edit_line = QtWidgets.QLineEdit()

        self.edit_line.setPlaceholderText("Recherche...")
        self.edit_line.textChanged.connect(self.text_de_recherche)

        self.layout_1.addWidget(self.edit_line)

        self.topLayout.addLayout(self.layout_2)

        self.liste_user = QtWidgets.QListWidget()

        self.layout_2.addWidget(self.liste_user)

        self.layout_info = QtWidgets.QFormLayout()


        self.layout_info.setContentsMargins(20, 10, 20, 10)
        self.layout_2.addLayout(self.layout_info)

        self.bottom_layout = QtWidgets.QHBoxLayout()
        self.topLayout.addLayout(self.bottom_layout)



        self.Btn_affiche = QPushButton("Affiche")
        self.Btn_rafrechie = QPushButton("Rafrechie")

        self.Btn_affiche.setMaximumSize(QtCore.QSize(150, 200))
        self.Btn_rafrechie.setMaximumSize(QtCore.QSize(150, 200))

        self.bottom_layout.addWidget(self.Btn_affiche)


        self.bottom_layout.addWidget(self.Btn_rafrechie)



    def les_noms(self, items):
        user_click = items.data(QtCore.Qt.UserRole)
        if user_click is None or not isinstance(user_click, int):
            return
        user = ServieCompte.get_user_by_id(user_click)

        for i in reversed(range(self.layout_info.count())):
            item = self.layout_info.takeAt(i)
            if item.widget():
                item.widget().deleteLater()

        self.layout_info.addRow("<h1>ID : </h1>", QLabel(f"<h1><b>{user['ID']}</b></h1>"))
        self.layout_info.addRow("<h1>Nom : </h1>", QLabel(f"<h1><b>{user['Nom']}</b></h1>"))
        self.layout_info.addRow("<h1>Prénom :</h1>", QLabel(f"<h1><b>{user['Prenom']}</b></h1>"))
        self.layout_info.addRow("<h1>Áge :</h1>", QLabel(f"<h1><b>{user['Age']}</b></h1>"))
        self.layout_info.addRow("<h1>Sexe :</h1>", QLabel(f"<h1><b>{user['Sexe']}</b></h1>"))
        self.layout_info.addRow("<h1>Numéro :</h1>", QLabel(f"<h1><b>{user['Numero']}</b></h1>"))
        self.layout_info.addRow("<h1>Email :</h1>", QLabel(f"<h1><b>{user['Email']}</b></h1>"))
        self.layout_info.addRow("<h1>Solde :</h1>", QLabel(f"<h1><b>{user['Solde']}</b></h1>"))


    def setup_connections(self):
        self.liste_user.itemClicked.connect(self.les_noms)

        self.Btn_rafrechie.clicked.connect(lambda x :self.recherch)


    def users(self):
        donnees = ServieCompte.get_users()
        return donnees

    def recuperer_les_noms(self):
        use = self.users()
        for i in use:
            text = f"{i[0]} • {i[1].capitalize()} • {i[2].capitalize()} • {i[3]} "
            item = QtWidgets.QListWidgetItem(text)

            item.setData(QtCore.Qt.UserRole, i[0])
            self.liste_user.addItem(item)


    def recherch(self, filter_text: str = ''):
        users = ServieCompte.get_users()
        query = (filter_text or '').strip().lower()

        if not query:
            filtre = users[:6]
        else:
            filtre = [
                user
                for user in users
                if query in str(user[1]).lower()
                   or query in str(user[2]).lower()
                   or query in str(user[0]).lower()
            ]

        self.liste_user.clear()
        if not filtre:
            self.liste_user.addItem('Aucun utilisateur trouvé.')
            return

        for user in filtre:
            self.liste_user.addItem(f'{user[0]} • {user[1]} • {user[2]} • {user[3]}')


    def text_de_recherche(self, texte: str):
        self.recherch(filter_text=texte)




















if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = UsersInfo()
    with open('assets/styles.qss', 'r') as f:
        styles = f.read()
        app.setStyleSheet(styles)

    window.show()
    app.exec()




