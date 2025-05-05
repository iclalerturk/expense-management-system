from PyQt5 import QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import sqlite3
import pandas as pd
from datetime import datetime
import os

class TahminGrafikWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setLayout(QtWidgets.QVBoxLayout())

        # n değeri için kontrol
        kontrol_layout = QtWidgets.QHBoxLayout()
        self.spinBox = QtWidgets.QSpinBox()
        self.spinBox.setMinimum(1)
        self.spinBox.setValue(3)
        self.spinBox.setSuffix(" periyot")
        kontrol_layout.addWidget(QtWidgets.QLabel("Hareketli Ortalama Periyodu:"))
        kontrol_layout.addWidget(self.spinBox)

        self.button = QtWidgets.QPushButton("Grafiği Oluştur")
        self.button.setStyleSheet('''
           QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 10px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }                       
                                  
                                  ''')
        self.button.clicked.connect(self.grafik_olustur)
        kontrol_layout.addWidget(self.button)

        self.layout().addLayout(kontrol_layout)

        # Matplotlib çizimi için placeholder
        self.canvas = None
        self.figure = None

    def grafik_olustur(self):
        n = self.spinBox.value()

        # Veriyi oku
        db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gider.db')
        conn = sqlite3.connect(db_path)
        df = pd.read_sql_query("""
            SELECT tarih, tutar
            FROM harcama
            WHERE onayDurumu = 'Onaylandi'
            ORDER BY tarih ASC
        """, conn)
        conn.close()

        df["tarih"] = pd.to_datetime(df["tarih"])
        df.set_index("tarih", inplace=True)
        df.resample("M").sum()

        df["hareketli_ortalama"] = df["tutar"].rolling(window=n).mean()

        # Önceki grafik varsa kaldır
        if self.canvas:
            self.layout().removeWidget(self.canvas)
            self.canvas.setParent(None)

        # Yeni grafik
        self.figure = Figure(figsize=(6, 4))
        self.canvas = FigureCanvas(self.figure)
        ax = self.figure.add_subplot(111)

        df["tutar"].plot(ax=ax, label="Gerçek Harcama", marker="o")
        df["hareketli_ortalama"].plot(ax=ax, label=f"{n} Periyotluk Hareketli Ortalama", linestyle="--")

        ax.set_title("Harcama Tahmini - Hareketli Ortalama Yöntemi")
        ax.set_xlabel("Tarih")
        ax.set_ylabel("Tutar (TL)")
        ax.legend()
        self.figure.autofmt_xdate()

        self.layout().addWidget(self.canvas)
        self.canvas.draw()
