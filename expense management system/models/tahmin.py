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

        # Tahmin etiketi
        self.tahminLabel = QtWidgets.QLabel("Gelecek Yıl Tahmini: -")
        self.tahminLabel.setStyleSheet("font-weight: bold; font-size: 14px; padding: 6px; color: #2c3e50;")
        self.layout().addWidget(self.tahminLabel)

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
        
        # Yıllık verileri hazırla
        df_yillik = df.resample("Y").sum()
        
        # Yıl bilgisi için indeksi string'e çevir
        df_yillik = df_yillik.reset_index()
        df_yillik['yil'] = df_yillik['tarih'].dt.year
        
        # Hareketli ortalama
        df_yillik["hareketli_ortalama"] = df_yillik["tutar"].rolling(window=n).mean()

        # Gelecek yıl tahmini
        tahmin = df_yillik["hareketli_ortalama"].iloc[-1]
        if pd.isna(tahmin):
            self.tahminLabel.setText("Gelecek Yıl Tahmini: Yetersiz veri")
        else:
            self.tahminLabel.setText(f"Gelecek Yıl Tahmini: {tahmin:.2f} TL")

        # Grafik çizimi
        # Önceki grafik varsa kaldır
        if self.canvas:
            self.layout().removeWidget(self.canvas)
            self.canvas.setParent(None)

        self.figure = Figure(figsize=(6, 4))
        self.canvas = FigureCanvas(self.figure)
        ax = self.figure.add_subplot(111)

        # x ekseni için yıl bilgilerini kullan
        ax.plot(df_yillik['yil'], df_yillik['tutar'], marker='o', label='Yıllık Harcama')
        ax.plot(df_yillik['yil'], df_yillik['hareketli_ortalama'], linestyle='--', 
                label=f'{n} Periyotluk Ortalama')

        ax.set_title("Yıllık Harcama Tahmini - Hareketli Ortalama Yöntemi")
        ax.set_xlabel("Yıl")
        ax.set_ylabel("Tutar (TL)")
        ax.legend()
        
        # X eksenindeki yıl etiketlerini ayarla
        ax.set_xticks(df_yillik['yil'])
        ax.set_xticklabels(df_yillik['yil'], rotation=45)

        self.figure.tight_layout()
        self.layout().addWidget(self.canvas)
        self.canvas.draw()