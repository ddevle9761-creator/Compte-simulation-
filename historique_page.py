import sys
from comptservice import ServieCompte
from PySide6 import QtWidgets, Qt, QtCore
from PySide6.QtWidgets import QVBoxLayout, QPushButton, QLabel


class HistoriquePage(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Recherche des utilluisateurs')

        self.setMinimumSize(600, 501)
        self.setup_ui()
        self.setup_connections()

    def setup_ui(self):
        topLayout = QVBoxLayout(self)
        info_label = QLabel("<h1><b>Information</b></h1>")

        topLayout.addWidget(info_label)
        topLayout.setSpacing(4)
        topLayout.setContentsMargins(1, 1, 1, 1)

        layout_1 = QtWidgets.QHBoxLayout()

        topLayout.addLayout(layout_1)



        edit_line = QtWidgets.QLineEdit()

        edit_line.setPlaceholderText("Recherche...")

        layout_1.addWidget(edit_line)

        layout_2 = QtWidgets.QHBoxLayout()
        topLayout.addLayout(layout_2)

        liste_user = QtWidgets.QListWidget()


        layout_2.addWidget(liste_user)
        show_info_user = QtWidgets.QListWidget()

        layout_2.addWidget(show_info_user)

        use = ['pomme', 'apple','tomate', 'banana', 'kiwi']
        for i in use:
            liste_user.addItem(str(i))


        form_layout = QtWidgets.QFormLayout()


    def setup_connections(self):
        pass


    def users(self):
        donnees = ServieCompte.get_users()
        print(donnees)















app = QtWidgets.QApplication(sys.argv)
window = HistoriquePage()
with open('assets/styles.qss', 'r') as f:
    styles = f.read()
    app.setStyleSheet(styles)

window.show()
app.exec()




