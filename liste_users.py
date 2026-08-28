from collections import Counter
from PySide6 import QtCore, QtWidgets
from PySide6.QtGui import QPainter
from PySide6.QtCharts import (
    QChart,
    QChartView,
    QBarSeries,
    QBarSet,
    QBarCategoryAxis,
    QValueAxis,
    QLineSeries,
    QPieSeries,
    QScatterSeries,
)

import sys
from comptservice import ServieCompte


class Stactistique(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Liste de users')
        self.setMinimumSize(980, 620)
        self.mode_graphique = 'hist'
        self.setup_ui()
        self.connction()



    def connction(self):
        self.rafrechie_users()
        self.miss_a_jour_ui()
        self.rafresh_button.clicked.connect(self.on_refresh_clicked)

    def setup_ui(self):
        self.setStyleSheet(
            'background-color: #050B18; color: #E2E8F0; font-family: Segoe UI, sans-serif;'
        )

        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.setContentsMargins(18, 18, 18, 18)
        self.main_layout.setSpacing(16)

        titre = QtWidgets.QLabel("<h1 style='background-color: #0D1724; color:cyan;'>Aperçu des utilisateurs</h1>")
        titre.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        titre.setStyleSheet('font-size: 22px; font-weight: 700; padding-bottom: 8px;')
        self.main_layout.addWidget(titre)

        top_bar = QtWidgets.QHBoxLayout()
        top_bar.setSpacing(12)

        self.champ_recherche = QtWidgets.QLineEdit()
        self.champ_recherche.setPlaceholderText('Rechercher un utilisateur par nom, prénom ou ID')
        self.champ_recherche.textChanged.connect(self.text_de_recherche)
        self.champ_recherche.setStyleSheet(
            'padding: 12px 14px; border-radius: 14px; background-color: #0F1724;'
            ' border: 1px solid #334155; color: #F8FAFC;'
        )
        top_bar.addWidget(self.champ_recherche, 1)

        self.rafresh_button = QtWidgets.QPushButton('Actualiser')
        self.rafresh_button.setCursor(QtCore.Qt.PointingHandCursor)
        self.rafresh_button.setStyleSheet(
            'padding: 10px 18px; border-radius: 12px; background-color: #2563EB; color: #F8FAFC; border: 1px solid #CBD5E1;  margin: 0px; font-weight: 600; font-size: 14px;'
        )
        top_bar.addWidget(self.rafresh_button)

        self.main_layout.addLayout(top_bar)

        content_layout = QtWidgets.QHBoxLayout()
        content_layout.setSpacing(16)
        self.main_layout.addLayout(content_layout)

        gauche_panel = QtWidgets.QWidget()
        gauche_panel.setStyleSheet(
            'background-color: #111827; border: 1px solid #334155; border-radius: 20px;'
        )
        gauche_panel.setLayout(QtWidgets.QVBoxLayout())
        gauche_panel.layout().setContentsMargins(18, 18, 18, 18)
        gauche_panel.layout().setSpacing(12)

        list_title = QtWidgets.QLabel('Utilisateurs récents')
        list_title.setStyleSheet('font-size: 17px; font-weight: 600;')
        gauche_panel.layout().addWidget(list_title)

        self.liste_apercu = QtWidgets.QListWidget()
        self.liste_apercu.setStyleSheet(
            'background-color: transparent; border: none; color: #F8FAFC; font-size: 14px;'
        )
        self.liste_apercu.setSelectionMode(QtWidgets.QListWidget.NoSelection)
        gauche_panel.layout().addWidget(self.liste_apercu)

        content_layout.addWidget(gauche_panel, 1)

        droite_panel = QtWidgets.QWidget()
        droite_panel.setStyleSheet(
            'background-color: #111827; border: 1px solid #334155; border-radius: 20px;'
        )
        droite_panel.setLayout(QtWidgets.QVBoxLayout())
        droite_panel.layout().setContentsMargins(18, 18, 18, 18)
        droite_panel.layout().setSpacing(14)

        header_layout = QtWidgets.QHBoxLayout()
        header_layout.setSpacing(12)

        chart_label = QtWidgets.QLabel('Graphique ')
        chart_label.setStyleSheet('font-size: 17px; font-weight: 600; border-radius: 12px;')
        header_layout.addWidget(chart_label)
        header_layout.addStretch(1)

        self.chart_type = QtWidgets.QComboBox()
        self.chart_type.addItems(['Histogramme', 'Ligne', 'Secteur', 'Rélation'])
        self.chart_type.setCurrentText('Histogramme')
        self.chart_type.setStyleSheet(
            'padding: 8px 12px; border-radius: 12px; background-color: #0F1724; color: #F8FAFC;'
        )
        self.chart_type.currentTextChanged.connect(self.monde_graph)
        header_layout.addWidget(self.chart_type)

        droite_panel.layout().addLayout(header_layout)

        self.chart_view = QChartView()
        self.chart_view.setRenderHint(QPainter.Antialiasing)
        self.chart_view.setMinimumHeight(360)
        self.chart_view.setStyleSheet('border: none;')
        droite_panel.layout().addWidget(self.chart_view)

        content_layout.addWidget(droite_panel, 2)

    def text_de_recherche(self, texte: str):
        self.rafrechie_users(filter_text=texte)

    def on_refresh_clicked(self):
        self.champ_recherche.clear()
        self.rafrechie_users()
        self.miss_a_jour_ui()

    def rafrechie_users(self, filter_text: str = ''):
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

        self.liste_apercu.clear()
        if not filtre:
            self.liste_apercu.addItem('Aucun utilisateur trouvé.')
            return

        for user in filtre:
            self.liste_apercu.addItem(f'{user[0]} • {user[1]} {user[2]}')

    def monde_graph(self, selection: str):
        mapping = {
            'Histogramme': 'hist',
            'Ligne': 'line',
            'Secteur': 'pie',
            'Rélation': 'scatter',
        }
        self.mode_graphique = mapping.get(selection, 'hist')
        self.miss_a_jour_ui()

    def miss_a_jour_ui(self):
        users = ServieCompte.get_users()
        ages = [user[3] for user in users if isinstance(user[3], (int, float))]
        solde = [user[-1] for user in users if isinstance(user[-1], (int, float))]
        frequency = Counter(ages)

        chart = QChart()
        chart.setAnimationOptions(QChart.SeriesAnimations)
        chart.setTheme(QChart.ChartThemeDark)
        chart.setTitle('Âges des utilisateurs')

        chart.setTitleBrush(QtCore.Qt.white)
        chart.legend().hide()

        if not frequency:
            chart.setTitle('Aucune donnée disponible')
            self.chart_view.setChart(chart)
            return

        if self.mode_graphique == 'hist':
            categories = [str(age) for age in sorted(frequency)]
            bar_set = QBarSet('Utilisateurs')
            for age in sorted(frequency):
                bar_set.append(frequency[age])

            series = QBarSeries()
            series.append(bar_set)
            chart.addSeries(series)

            axis_x = QBarCategoryAxis()
            axis_x.append(categories)
            axis_x.setTitleText('Âge')
            chart.addAxis(axis_x, QtCore.Qt.AlignBottom)
            series.attachAxis(axis_x)

            axis_y = QValueAxis()
            axis_y.setTitleText('Nombre')
            axis_y.setRange(0, max(frequency.values()) + 1)
            chart.addAxis(axis_y, QtCore.Qt.AlignLeft)
            series.attachAxis(axis_y)

        elif self.mode_graphique == 'line':
            line_series = QLineSeries()
            for index, age in enumerate(sorted(frequency)):
                line_series.append(index, frequency[age])
            chart.addSeries(line_series)

            axis_x = QBarCategoryAxis()
            categories = [str(age) for age in sorted(frequency)]
            axis_x.append(categories)
            axis_x.setTitleText('Âge')
            chart.addAxis(axis_x, QtCore.Qt.AlignBottom)
            line_series.attachAxis(axis_x)

            axis_y = QValueAxis()
            axis_y.setTitleText('Nombre')
            axis_y.setRange(0, max(frequency.values()) + 1)
            chart.addAxis(axis_y, QtCore.Qt.AlignLeft)
            line_series.attachAxis(axis_y)

        elif self.mode_graphique == 'scatter':
            scatter_series = QScatterSeries()
            scatter_series.setName('Âge vs Solde')
            for age, balance in zip(ages, solde):
                scatter_series.append(age, balance)
            chart.addSeries(scatter_series)

            axis_x = QValueAxis()
            axis_x.setTitleText('Âge')
            if ages:
                axis_x.setRange(min(ages), max(ages))
            chart.addAxis(axis_x, QtCore.Qt.AlignBottom)
            scatter_series.attachAxis(axis_x)

            axis_y = QValueAxis()
            axis_y.setTitleText('Solde')
            if solde:
                axis_y.setRange(0, max(solde) + max(1000, int(max(solde) * 0.1)))
            chart.addAxis(axis_y, QtCore.Qt.AlignLeft)
            scatter_series.attachAxis(axis_y)

        else:
            pie_series = QPieSeries()
            for age, count in sorted(frequency.items()):
                pie_series.append(f'{age} ans', count)
            chart.addSeries(pie_series)
            pie_series.setLabelsVisible(True)
            chart.legend().setVisible(True)
            chart.legend().setAlignment(QtCore.Qt.AlignBottom)

        self.chart_view.setChart(chart)

if __name__ == '__main__':

    app = QtWidgets.QApplication(sys.argv)

    window = Stactistique()
    window.show()
    sys.exit(app.exec())