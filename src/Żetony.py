import sys
import DataManager
from operator import add

from PySide6 import QtGui
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QTabWidget, QVBoxLayout, QHBoxLayout, QLabel, \
    QLineEdit, QTableWidget, QTableWidgetItem, QHeaderView, QFrame, QAbstractItemView, QPushButton, QComboBox, QSpinBox, QMessageBox

#tutaj wciskasz ilości żetonów z bazy danych
ilosci = DataManager.get_zetony_by_machine_id(1).zetony
transakcje = DataManager.get_historia()
nominaly = DataManager.nominaly


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("System Inwentaryzacji Żetonów") #nazwa okna
        self.resize(800, 600)
        self.setMinimumSize(QSize(800, 600))

        tabs = QTabWidget()
        tabs.setMovable(False)
        self.Automaty = Automaty()
        self.historia = Historia()

        tabs = QTabWidget()
        tabs.setMovable(False)
        tabs.addTab(self.Automaty, "Stan Automatów") #nazwa zakładki automatów
        tabs.addTab(self.historia, "Historia Transakcji") #nazwa zakładki historii

        self.setCentralWidget(tabs)




class Automaty(QWidget):
    def __init__(self):
        super().__init__()

        wiersz = QVBoxLayout(self)

        tytul = QLabel("Magazyn Lokalny") #nazwa automatu
        tytul_font = QtGui.QFont()
        tytul_font.setBold(True)
        tytul_font.setPointSize(25)
        tytul.setFont(tytul_font)
        tytul.setAlignment(Qt.AlignmentFlag.AlignCenter)
        wiersz.addWidget(tytul)


        kolumny = QHBoxLayout()

        kolumna1 = QLabel("Żeton")
        kolumna1_font = QtGui.QFont()
        kolumna1_font.setBold(True)
        kolumna1_font.setPointSize(18)
        kolumna1.setFont(kolumna1_font)
        kolumna1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        kolumny.addWidget(kolumna1, 1)

        kolumna2 = QLabel("Ilość")
        kolumna2.setFont(kolumna1_font)
        kolumna2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        kolumny.addWidget(kolumna2, 1)

        kolumna3 = QLabel("Transakcja")
        kolumna3.setFont(kolumna1_font)
        kolumna3.setAlignment(Qt.AlignmentFlag.AlignCenter)
        kolumny.addWidget(kolumna3, 1)

        wiersz.addLayout(kolumny)

        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        wiersz.addWidget(separator)

        self.spinboxy = {}
        self.d_ilosci = {}


        for n in nominaly:
            kolumny2 = QHBoxLayout()

            nominal = QLabel(str(n))
            nominal.setFont(QFont("Arial", 15))
            nominal.setAlignment(Qt.AlignmentFlag.AlignCenter)

            ilosc = QLabel()
            ilosc.setFrameShape(QFrame.Shape.Box)
            ilosc.setFixedSize(60, 30)
            ilosc.setAlignment(Qt.AlignmentFlag.AlignCenter)
            ilosc.setText(str(ilosci[n]))
            self.d_ilosci[n] = ilosc

            transakcja = QSpinBox()
            transakcja.setFixedSize(80, 30)
            self.spinboxy[n] = transakcja

            kolumny2.addWidget(nominal, 1)
            kolumny2.addWidget(ilosc, 1, Qt.AlignmentFlag.AlignCenter)
            kolumny2.addWidget(transakcja, 1, Qt.AlignmentFlag.AlignCenter)
            wiersz.addLayout(kolumny2)

        przyciski = QHBoxLayout()
        dodaj = QPushButton("Dodaj")
        dodaj.setFixedHeight(40)
        dodaj.clicked.connect(self.dodaj_w)


        self.usun = QPushButton("Usuń")
        self.usun.setFixedHeight(40)
        self.usun.clicked.connect(self.usun_w)

        przyciski.addWidget(dodaj)
        przyciski.addWidget(self.usun)
        wiersz.addLayout(przyciski)

        self.aktualizuj_ilosci()


    def aktualizuj_ilosci(self):
        noweWartosci = DataManager.get_zetony_by_machine_id(1)
        ilosci = noweWartosci.zetony
        for n in nominaly:
            self.d_ilosci[n].setText(str(ilosci[n]))
        transakcje = DataManager.get_historia()

    def dodaj_w(self):
        zawartosc_transakcji = {}
        for n in nominaly:
            zawartosc_transakcji[n] = self.spinboxy[n].value()
            self.spinboxy[n].setValue(0)
        lista_wartosci = DataManager.wartosci_dict_to_list(zawartosc_transakcji)
        zestaw = DataManager.ZestawZetonow(lista_wartosci)
        DataManager.add_zetony(zestaw, 1)
        transakcje = DataManager.get_historia()
        self.aktualizuj_ilosci()


    def usun_w(self):
        zawartosc_transakcji = {}
        for n in nominaly:
            zawartosc_transakcji[n] = self.spinboxy[n].value()
            if zawartosc_transakcji[n] > ilosci[n]:
                QMessageBox.warning(self, "Błąd", "Nie można usunąć więcej niż już jest")
                break
            self.spinboxy[n].setValue(0)
        print(zawartosc_transakcji,"\n",ilosci)
        lista_wartosci = DataManager.wartosci_dict_to_list(zawartosc_transakcji)
        zestaw = DataManager.ZestawZetonow(lista_wartosci)
        DataManager.remove_zetony(zestaw, 1)
        self.aktualizuj_ilosci()



class Historia(QWidget):
    def __init__(self):
        super().__init__()

        wiersz = QVBoxLayout(self)

        tytul = QLabel("Historia Transakcji")
        tytul_font = QtGui.QFont()
        tytul_font.setBold(True)
        tytul_font.setPointSize(25)
        tytul.setFont(tytul_font)
        tytul.setAlignment(Qt.AlignmentFlag.AlignCenter)
        wiersz.addWidget(tytul)

        tabelka = QTableWidget()
        tabelka.setColumnCount(8)
        tabelka.setHorizontalHeaderLabels(["Data", "Automat", "Wpłata?", "10", "20", "50", "100", "200"])
        tabelka.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        tabelka.setShowGrid(False)
        tabelka.verticalHeader().setVisible(False)
        tabelka.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        wiersz.addWidget(tabelka)

        #                     |
        # historia transakcji v
        G_tabelka = tabelka
        tabelka.setRowCount(len(transakcje))


        for wiersz, dane in enumerate(transakcje): #dodawajka historii do historii transakcji





            #Zrób tak, żeby się aktualizowało po każdej transakcji i będziesz złoty!





            for kolumna, wartosc in enumerate(dane.to_list()):
                element = QTableWidgetItem(wartosc)

                element.setTextAlignment(
                    Qt.AlignmentFlag.AlignCenter
                )

                tabelka.setItem(wiersz, kolumna, element)

DataManager.init_db()
app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())