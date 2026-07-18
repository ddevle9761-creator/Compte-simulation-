import sys
from collections import Counter


from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter
from PySide6.QtCharts import (
    QChart, QChartView, QBarSeries, QBarSet,
    QBarCategoryAxis, QValueAxis, QLineSeries, QPieSeries, QScatterSeries
)
from comptservice import ServieCompte
from page_user import Page_user
from expe_page import  Expe
from liste_users import Stactistique


from PySide6.QtWidgets import (
    QApplication, QWidget, QPushButton,
    QVBoxLayout, QHBoxLayout, QLabel,
    QStackedWidget, QListWidget, QLineEdit, QSpinBox,
    QMessageBox, QComboBox, QRadioButton, QButtonGroup
)



class App(QWidget):
    def __init__(self):
        super().__init__()
        self.page_trasfer = None
        self.setWindowTitle('Dashboard')
        self.resize(1000, 650)
        self.mode_graphique = 'hist'
        self.setup_ui()
        self.setup_connections()

    def setup_ui(self):
        # Barres de navigation — boutons en colonne
        self.btn_tableau = QPushButton("Tableau")
        self.btn_utilisateurs = QPushButton("Utilisateurs")
        self.btn_transaction = QPushButton("Transactions")
        self.btn_transfer = QPushButton("Transfert")
        self.btn_supprimer = QPushButton("Supprimer")
        self.btn_graph = QPushButton("Graphique")

        for b in (self.btn_tableau, self.btn_utilisateurs, self.btn_transaction, self.btn_transfer, self.btn_graph):
            b.setObjectName("btn-primary")

        sidebar = QVBoxLayout()
        sidebar.setContentsMargins(10, 10, 10, 10)
        sidebar.setSpacing(10)
        sidebar.addWidget(self.btn_tableau)
        sidebar.addWidget(self.btn_utilisateurs)
        sidebar.addWidget(self.btn_transaction)
        sidebar.addWidget(self.btn_transfer)
        sidebar.addWidget(self.btn_graph)
        sidebar.addStretch(1)
        sidebar.addWidget(self.btn_supprimer)

        # Contenu principal (pile de pages)
        self.stack = QStackedWidget()
        self.pile_pages = self.stack
        self.pile_pages.addWidget(self.create_dashboard_page())
        self.page_utilisateur = Page_user()
        self.page_trasfer = Expe()
        self.page_graph = Stactistique()
        self.pile_pages.addWidget(self.page_utilisateur)
        self.pile_pages.addWidget(self.creer_page_supprimer())
        self.pile_pages.addWidget(self.creer_page_transaction())
        self.pile_pages.addWidget(self.page_trasfer)
        self.pile_pages.addWidget(self.page_graph)

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(20)
        main_layout.addLayout(sidebar)
        main_layout.addWidget(self.stack)
        main_layout.setStretch(0, 0)
        main_layout.setStretch(1, 1)

    def create_dashboard_page(self):
        page = QWidget()
        page_layout = QVBoxLayout(page)
        page_layout.setSpacing(20)
        page_layout.setContentsMargins(16, 16, 16, 16)

        header = QLabel("Tableau de bord")
        header.setProperty("class", "header")
        subtitle = QLabel("Vue d'ensemble des utilisateurs et du solde disponible.")
        subtitle.setWordWrap(True)
        subtitle.setStyleSheet("color: #94A3B8; font-size: 13px; margin-bottom: 16px;")

        page_layout.addWidget(header)
        page_layout.addWidget(subtitle)

        cards_layout = QHBoxLayout()
        cards_layout.setSpacing(16)
        cards_layout.addWidget(self.create_stat_card("Utilisateurs", self.user_count(), "Total des comptes actifs"))
        cards_layout.addWidget(self.create_stat_card("Solde total", self.total_balance(), "Montant global disponible"))
        cards_layout.addWidget(self.create_stat_card("Âge moyen", self.average_age(), "Âge moyen des utilisateurs"))

        page_layout.addLayout(cards_layout)

        section_layout = QHBoxLayout()
        section_layout.setSpacing(16)
        section_layout.addWidget(self.create_user_preview())
        section_layout.addWidget(self.create_age_chart())
        section_layout.addWidget(self.create_actions_panel())
        page_layout.addLayout(section_layout)

        page_layout.addStretch(1)

        return page

    def create_stat_card(self, title, value, description):
        card = QWidget()
        card.setStyleSheet(
            "background-color: #151E32; border: 1px solid #334155; border-radius: 20px;"
        )
        layout = QVBoxLayout(card)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(10)

        title_label = QLabel(title)
        title_label.setStyleSheet("font-size: 14px; color: #94A3B8;")
        value_label = QLabel(str(value))
        value_label.setStyleSheet("font-size: 34px; font-weight: 700; color: #FFFFFF;")
        description_label = QLabel(description)
        description_label.setStyleSheet("font-size: 12px; color: #64748B;")
        description_label.setWordWrap(True)

        layout.addWidget(title_label)
        layout.addWidget(value_label)
        layout.addWidget(description_label)
        layout.addStretch(1)
        return card




    def create_age_chart(self):
        card = QWidget()
        card.setStyleSheet(
            "background-color: #151E32; border: 1px solid #334155; border-radius: 20px;"
        )
        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        title = QLabel("Répartition des âges")
        title.setProperty("class", "stats-title")
        layout.addWidget(title)
        
        self.chart_type = QComboBox()
        self.chart_type.addItems(["Histogramme", "Ligne", "Secteur", "Rélation"])
        mapping_current = {
            'hist': 'Histogramme',
            'line': 'Ligne',
            'pie': 'Secteur',
            'scatter': 'Rélation'
        }
        self.chart_type.setCurrentText(mapping_current.get(self.mode_graphique, 'Histogramme'))
        self.chart_type.setStyleSheet("padding:6px; border-radius:8px; background-color:#0F1724; color:#F1F5F9;")
        self.chart_type.currentTextChanged.connect(self.set_chart_mode)
        layout.addWidget(self.chart_type)

        users = ServieCompte.get_users()
        ages = [u[3] for u in users if isinstance(u[3], (int, float))]
        solde = [u[-1] for u in users if isinstance(u[-1], (int, float))]
        frequency = Counter(ages)

        if not frequency:
            message = QLabel("Aucune donnée disponible")
            message.setStyleSheet("color:#94A3B8; font-size:13px;")
            layout.addWidget(message)
            return card

        mode = getattr(self, 'mode_graphique', 'hist')
        chart = QChart()
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.setTheme(QChart.ChartThemeDark)
        chart.setTitle("Âges des utilisateurs")
        chart.setTitleBrush(Qt.white)
        chart.legend().hide()

        if mode == 'hist':
            categories = [str(age) for age in sorted(frequency)]
            bar_set = QBarSet("Utilisateurs")
            for age in sorted(frequency):
                bar_set.append(frequency[age])

            series = QBarSeries()
            series.append(bar_set)
            chart.addSeries(series)

            axis_x = QBarCategoryAxis()
            axis_x.append(categories)
            axis_x.setTitleText("Âge")
            chart.addAxis(axis_x, Qt.AlignBottom)
            series.attachAxis(axis_x)

            axis_y = QValueAxis()
            axis_y.setTitleText("Nombre")
            axis_y.setRange(0, max(frequency.values()) + 1)
            chart.addAxis(axis_y, Qt.AlignLeft)
            series.attachAxis(axis_y)
        elif mode == 'line':
            line_series = QLineSeries()
            for idx, age in enumerate(sorted(frequency)):
                line_series.append(idx, frequency[age])
            chart.addSeries(line_series)

            axis_x = QBarCategoryAxis()
            categories = [str(age) for age in sorted(frequency)]
            axis_x.append(categories)
            axis_x.setTitleText("Âge")
            chart.addAxis(axis_x, Qt.AlignBottom)
            line_series.attachAxis(axis_x)

            axis_y = QValueAxis()
            axis_y.setTitleText("Nombre")
            axis_y.setRange(0, max(frequency.values()) + 1)
            chart.addAxis(axis_y, Qt.AlignLeft)
            line_series.attachAxis(axis_y)

        elif mode == 'scatter':
            scatter = QScatterSeries()
            scatter.setName("Âge vs Solde")
            for a, s in zip(ages, solde):
                scatter.append(a, s)
            chart.addSeries(scatter)

            axis_x = QValueAxis()
            axis_x.setTitleText("Âge")
            if ages:
                axis_x.setRange(min(ages), max(ages))
            chart.addAxis(axis_x, Qt.AlignBottom)
            scatter.attachAxis(axis_x)

            axis_y = QValueAxis()
            axis_y.setTitleText("Solde")
            if solde:
                axis_y.setRange(0, max(solde) + max(1000, int(max(solde) * 0.1)))
            chart.addAxis(axis_y, Qt.AlignLeft)
            scatter.attachAxis(axis_y)

        else:
            pie_series = QPieSeries()
            for age, count in sorted(frequency.items()):
                slice_label = f"{age} ans"
                pie_series.append(slice_label, count)
            chart.addSeries(pie_series)
            pie_series.setLabelsVisible(True)
            chart.legend().setVisible(True)
            chart.legend().setAlignment(Qt.AlignBottom)

        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.Antialiasing)
        layout.addWidget(chart_view)




        return card

    def create_user_preview(self):
        card = QWidget()
        card.setStyleSheet(
            "background-color: #151E32; border: 1px solid #334155; border-radius: 20px;"
        )
        layout = QVBoxLayout(card)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(12)

        title = QLabel("Aperçu des utilisateurs")
        title.setProperty("class", "stats-title")
        layout.addWidget(title)

        self.champ_recherche = QLineEdit()
        self.champ_recherche.setPlaceholderText("Rechercher...")
        self.champ_recherche.textChanged.connect(self.filtrer_apercu)
        self.champ_recherche.setStyleSheet("padding:6px; border-radius:8px; background-color:#0F1724; color:#F1F5F9;")
        layout.addWidget(self.champ_recherche)

        self.liste_apercu = QListWidget()
        self.liste_apercu.setStyleSheet(
            "background-color: transparent; border: none; color: #F1F5F9;"
        )
        self.liste_apercu.setSelectionMode(QListWidget.NoSelection)
        self.refresh_user_preview()
        layout.addWidget(self.liste_apercu)
        return card


    def creer_page_supprimer(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        titre = QLabel("Supprimer des utilisateurs")
        titre.setProperty("class", "header")
        layout.addWidget(titre)

        liste = QListWidget()
        liste.setSelectionMode(QListWidget.MultiSelection)

        def refresh_list():
            liste.clear()
            for u in ServieCompte.get_users():
                liste.addItem(f"{u[0]} | {u[1]} | {u[2]} | {u[3]} {u[6]}")

        btn_sup = QPushButton("Supprimer sélection")

        def on_supprimer():
            sel = liste.selectedItems()
            if not sel:
                QMessageBox.information(page, 'Info', 'Aucune sélection')
                return
            for it in sel:
                try:
                    uid = int(it.text().split('|')[0].strip())
                except Exception:
                    continue
                
                users = ServieCompte.get_users()
                found = next((x for x in users if x[0] == uid), None)
                if found:
                    tmp = ServieCompte(nom=found[1], prenom=found[2], age=found[3], sexe=found[4], email=found.email ,  mdp=getattr(found,'_mdp',''), solde=getattr(found,'_solde',0), id=found._id, numero=found.numero)
                    tmp.remove_user()
            QMessageBox.information(page, 'Succès', 'Suppression effectuée')
            refresh_list()
            self.refresh_dashboard()

        btn_sup.clicked.connect(on_supprimer)
        layout.addWidget(liste)
        layout.addWidget(btn_sup)
        refresh_list()
        layout.addStretch(1)
        return page

    def creer_page_transaction(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        titre = QLabel("Transactions")
        titre.setProperty("class", "header")
        layout.addWidget(titre)

        self.transaction_compte = QComboBox()
        self.transaction_compte.setStyleSheet("padding:8px; border-radius:8px; background-color:#0F1724; color:#F1F5F9;")
        layout.addWidget(self.transaction_compte)

        montant_layout = QHBoxLayout()
        self.transaction_montant = QSpinBox()
        self.transaction_montant.setRange(1, 100000)
        self.transaction_montant.setPrefix("Montant : ")
        montant_layout.addWidget(self.transaction_montant)

        self.radio_depot = QRadioButton("Dépôt")
        self.radio_retrait = QRadioButton("Retrait")
        self.radio_depot.setChecked(True)
        radio_group = QButtonGroup(page)
        radio_group.addButton(self.radio_depot)
        radio_group.addButton(self.radio_retrait)

        montant_layout.addWidget(self.radio_depot)
        montant_layout.addWidget(self.radio_retrait)
        layout.addLayout(montant_layout)

        self.solde_actuel_label = QLabel("Solde actuel : 0")
        self.solde_actuel_label.setStyleSheet("color:#F1F5F9; font-size:13px;")
        layout.addWidget(self.solde_actuel_label)

        btn_trans = QPushButton("Valider transaction")
        btn_trans.setObjectName("btn-primary")
        btn_trans.clicked.connect(self.effectuer_transaction)
        layout.addWidget(btn_trans)

        layout.addStretch(1)

        self.transaction_compte.currentIndexChanged.connect(self.update_solde_actuel)
        self.refresh_transaction_list()
        return page

    def create_actions_panel(self):
        card = QWidget()
        card.setStyleSheet(
            "background-color: #151E32; border: 1px solid #334155; border-radius: 20px;"
        )
        layout = QVBoxLayout(card)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(12)

        title = QLabel("Actions rapides")
        title.setProperty("class", "stats-title")
        layout.addWidget(title)

        actions = ["Ouvrir la liste des utilisateurs", "Rafraîchir les données", "Basculer graphique"]
        for action in actions:
            btn = QPushButton(action)
            btn.setObjectName("btn-primary")
            if action == "Ouvrir la liste des utilisateurs":
                btn.clicked.connect(self.show_users)
            elif action == "Rafraîchir les données":
                btn.clicked.connect(self.refresh_dashboard)
            elif action == "Basculer graphique":
                btn.clicked.connect(self.basculer_mode_graphique)
            layout.addWidget(btn)


        layout.addStretch(1)
        return card

    def user_count(self):
        return len(ServieCompte.get_users())

    def total_balance(self):
        return ServieCompte.total_balance()

    def average_age(self):
        if ServieCompte.total_age():
            return ServieCompte.total_age()

    def refresh_user_preview(self):
        users = ServieCompte.get_users()
        self.liste_apercu.clear()
        for user in users:
            self.liste_apercu.addItem(f"{user[0]} • {user[1]} {user[2]}")


    def filtrer_apercu(self, texte: str):
        q = (texte or '').strip().lower()
        users = ServieCompte.get_users()
        filtres = []
        if not q:
            filtres = users[:6]
        else:
            for u in users:
                if q in str(u[1]).lower() or q in str(u[2]).lower() or q in str(u[0]):
                    filtres.append(u)
        self.liste_apercu.clear()
        for user in filtres[:6]:
            self.liste_apercu.addItem(f"{user[0]} • {user[1]} {user[2]}")

    def refresh_dashboard(self):
        self.pile_pages.removeWidget(self.pile_pages.widget(0))
        self.pile_pages.insertWidget(0, self.create_dashboard_page())
        self.pile_pages.setCurrentIndex(0)
        self.refresh_transaction_list()

    def refresh_transaction_list(self):
        if hasattr(self, 'transaction_compte'):
            self.transaction_compte.clear()
            for user in ServieCompte.get_users():
               
                self.transaction_compte.addItem(f"{user[0]} • {user[1]} {user[2]}", user[0])
            self.update_solde_actuel()

    def update_solde_actuel(self):
        uid = self.transaction_compte.currentData()
        if uid is None:
            self.solde_actuel_label.setText("Solde actuel : 0")
            return
        user = ServieCompte.get_user_by_id(uid)
        if user:
            self.solde_actuel_label.setText(f"Solde actuel : {user._solde} fcfa")
        else:
            self.solde_actuel_label.setText("Solde actuel : 0")

    def effectuer_transaction(self):
        uid = self.transaction_compte.currentData()
        if uid is None:
            QMessageBox.warning(self, 'Erreur', "Sélectionnez un utilisateur")
            return
        montant = self.transaction_montant.value()
        action = 'depot' if self.radio_depot.isChecked() else 'retrait'
        user = ServieCompte.get_user_by_id(uid)
        if user is None:
            QMessageBox.warning(self, 'Erreur', "Utilisateur introuvable")
            return
        if action == 'retrait' and int(montant) > user._solde:
            QMessageBox.warning(self, 'Erreur', "Solde insuffisant")
            return

        if not user.transacter(int(montant), action):
            QMessageBox.warning(self, 'Erreur', "Transaction impossible")
            return
        QMessageBox.information(self, 'Succès', 'Transaction enregistrée')
        self.refresh_dashboard()
        self.refresh_user_preview()

    def setup_connections(self):
        self.btn_tableau.clicked.connect(self.afficher_tableau)
        self.btn_utilisateurs.clicked.connect(self.afficher_utilisateurs)
        self.btn_transaction.clicked.connect(self.afficher_page_transaction)
        self.btn_supprimer.clicked.connect(self.afficher_page_supprimer)
        self.btn_transfer.clicked.connect(self.afficher_page_transfert)
        self.btn_graph.clicked.connect(self.afficher_page_graph)

    def show_dashboard(self):
        self.pile_pages.setCurrentIndex(0)

    def show_users(self):
        self.pile_pages.setCurrentIndex(1)

    def afficher_tableau(self):
        self.pile_pages.setCurrentIndex(0)

    def afficher_utilisateurs(self):
        self.pile_pages.setCurrentIndex(1)

    def afficher_page_supprimer(self):
        self.pile_pages.setCurrentIndex(2)

    def afficher_page_transaction(self):
        self.pile_pages.setCurrentIndex(3)

    def afficher_page_transfert(self):
        self.pile_pages.setCurrentIndex(4)

    def afficher_page_graph(self):
        self.pile_pages.setCurrentIndex(5)

    def basculer_mode_graphique(self):
        current = getattr(self, 'mode_graphique', 'hist')
        new_mode = 'line' if current == 'hist' else 'hist'
        self.mode_graphique = new_mode
        self.refresh_dashboard()

    def set_chart_mode(self, selection: str):
        mapping = {
            'Histogramme': 'hist',
            'Ligne': 'line',
            'Secteur': 'pie',
            'Rélation': 'scatter',

        }
        self.mode_graphique = mapping.get(selection, 'hist')
        self.refresh_dashboard()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    with open("assets/styles.qss") as f:
        app.setStyleSheet(f.read())
    window = App()
    window.show()
    sys.exit(app.exec())
