import sys
import os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout,
                             QPushButton, QLabel, QHBoxLayout, QComboBox, QMessageBox, QWidget)
from models.database import Database

class YoneticiPanelUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = Database()

    def setupUi(self, MainWindow, birim_id):
        self.birim_id = birim_id
        MainWindow.setWindowTitle("Yönetici Paneli - Harcama Onay Paneli")
        screen_geometry = MainWindow.screen().availableGeometry()
        x = (screen_geometry.width() - 1300) // 2
        y = (screen_geometry.height() - 800) // 2
        MainWindow.setGeometry(x, y, 1300, 800)  # (x, y, width, height)
        MainWindow.setStyleSheet("background-color: #E3E4E0;")

        self.central_widget = QWidget()
        MainWindow.setCentralWidget(self.central_widget)

        self.main_layout = QHBoxLayout(self.central_widget)

        self.init_sidebar()
        self.init_main_content()

        self.load_data()

    def init_sidebar(self):
        self.sidebar = QWidget()
        self.sidebar.setFixedWidth(130)
        self.sidebar.setStyleSheet("""
            background-color: #080121;
            QPushButton {
                color: white;
                background-color: transparent;
                text-align: left;
                padding: 15px;
                border-left: 4px solid transparent;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #5a2d5a;
                border-left: 4px solid #64748B;
            }
        """)
        self.sidebar_layout = QVBoxLayout(self.sidebar)
        self.sidebar_layout.setContentsMargins(0, 0, 0, 0)

        logo = QLabel()
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        startech_icon = os.path.join(BASE_DIR, "images", "startech.png")
        logo.setPixmap(QtGui.QPixmap(startech_icon))
        logo.setScaledContents(True)
        logo.setMaximumSize(120, 100)
        self.sidebar_layout.addWidget(logo, alignment=QtCore.Qt.AlignCenter)
        birim_adi = self.db.get_birim_adi(self.birim_id)
        birim_label = QLabel(birim_adi)
        birim_label.setStyleSheet("color: white; font-size: 14px; font-weight: bold; padding: 5px;")
        birim_label.setAlignment(QtCore.Qt.AlignCenter)
        self.sidebar_layout.addWidget(birim_label)


        # Harcamalar Button with Icon and Text
        bill_icon = os.path.join(BASE_DIR, "images", "bill.png")
        harcamalar_btn = QPushButton("  Harcamalar")
        harcamalar_btn.setIcon(QtGui.QIcon(bill_icon))
        harcamalar_btn.setIconSize(QtCore.QSize(20, 20))
        harcamalar_btn.setStyleSheet('''
            QPushButton {
                color: white;
                background-color: transparent;
                text-align: left;
                padding: 10px 5px;
                font-size: 14px;
                border-left: 4px solid transparent;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #5a2d5a;
                border-left: 4px solid #64748B;
            }
        ''')
        self.sidebar_layout.addWidget(harcamalar_btn)


        self.sidebar_layout.addStretch()

        self.btn_logout = QPushButton("Çıkış")
        

        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        logout_icon = os.path.join(BASE_DIR, "images", "logout.png")

        self.btn_logout.setIcon(QIcon(logout_icon))

        self.btn_logout.setIconSize(QtCore.QSize(24, 24))
        self.btn_logout.setStyleSheet('''
            QPushButton {
                background-color: transparent;
                border-radius: 0px;
                border-left: 4px solid transparent;
                text-align: left;
                padding: 15px;
                margin: 5px 0px;
            }
            QPushButton:hover {
                background-color: #5a2d5a;
                border-left: 4px solid #64748B;
            }
        ''')
        self.btn_logout.clicked.connect(self.logout)
        self.sidebar_layout.addWidget(self.btn_logout)

        self.main_layout.addWidget(self.sidebar)

    def init_main_content(self):
        self.content = QWidget()
        self.content_layout = QVBoxLayout(self.content)

        # Yönetici bilgileri (üstte gösterilir)
        self.user_info_layout = QHBoxLayout()

        yonetici = self.db.get_yonetici_by_birim_id(self.birim_id)
        birim_name = self.db.get_birim_adi(self.birim_id)
        
        if yonetici:
            welcome_label = QLabel(f"Yönetici Paneli\n\nHoş Geldiniz,\n{yonetici.get_full_name()} !\n")
        else:
            welcome_label = QLabel("Yönetici bilgisi bulunamadı.")

        welcome_label.setStyleSheet("font-size:25px; font-weight: bold; color: #333;")

        self.user_info_layout.addWidget(welcome_label)
        self.content_layout.addLayout(self.user_info_layout)


        # Dashboard özet kartları
        self.dashboard_layout = QHBoxLayout()
        self.card_beklemede = self.create_summary_card("Beklemede", "0", "#f39c12")
        self.card_onaylandi = self.create_summary_card("Onaylandı", "0", "#2ecc71")
        self.card_reddedildi = self.create_summary_card("Reddedildi", "0", "#e74c3c")
        self.dashboard_layout.addWidget(self.card_beklemede)
        self.dashboard_layout.addWidget(self.card_onaylandi)
        self.dashboard_layout.addWidget(self.card_reddedildi)

        self.content_layout.addLayout(self.dashboard_layout)

        self.header = QLabel("Harcama Talepleri")
        self.header.setStyleSheet("font-size: 20px; font-weight: bold; color: #333;")
        self.content_layout.addWidget(self.header)

        self.filter_combo = QComboBox()
        self.filter_combo.addItems(["Tümü", "Beklemede", "Onaylandi", "Reddedildi"])
        self.filter_combo.setFixedWidth(200)
        self.filter_combo.currentTextChanged.connect(self.load_data)
        self.content_layout.addWidget(self.filter_combo, alignment=QtCore.Qt.AlignLeft)

        self.table = QTableWidget()
        self.table.setColumnCount(12)
        self.table.setHorizontalHeaderLabels([
            "ID", "Ad Soyad", "Kalem", "Tutar", "Tazmin", "Açıklama", "Durum", "Tarih",
            "Limit Aşıldı mı", "Şuan Aşım Var mı", "Aşım Miktarı"
        ])
     
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)  # Stretch all columns by default
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)  # ID column
        header.setSectionResizeMode(10, QtWidgets.QHeaderView.ResizeToContents)  # ID column
        


        self.table.setAlternatingRowColors(True)
        self.table.setStyleSheet("QTableWidget { background: white; font-size: 14px; }")
        self.content_layout.addWidget(self.table)

        self.main_layout.addWidget(self.content)

    def create_summary_card(self, title, value, color):
        card = QWidget()
        layout = QVBoxLayout(card)
        layout.setContentsMargins(10, 10, 10, 10)

        title_label = QLabel(title)
        title_label.setStyleSheet(f"font-size: 14px; color: #666;")
        value_label = QLabel(value)
        value_label.setStyleSheet(f"font-size: 24px; font-weight: bold; color: {color};")
        value_label.setAlignment(QtCore.Qt.AlignCenter)

        layout.addWidget(title_label, alignment=QtCore.Qt.AlignCenter)
        layout.addWidget(value_label, alignment=QtCore.Qt.AlignCenter)

        card.setStyleSheet(f"background-color: white; border: 1px solid #ccc; border-radius: 8px;")
        card.setFixedHeight(80)
        card.setFixedWidth(150)
        card.value_label = value_label  # Store label to update later
        return card

    def load_data(self):
    # Update dashboard summary
        counts = self.db.get_status_counts(self.birim_id)
        self.card_beklemede.value_label.setText(str(counts.get("Beklemede", 0)))
        self.card_onaylandi.value_label.setText(str(counts.get("Onaylandi", 0)))
        self.card_reddedildi.value_label.setText(str(counts.get("Reddedildi", 0)))

        # Get table rows
        status_filter = self.filter_combo.currentText()
        rows = self.db.get_harcamalar_by_birim(self.birim_id, status_filter)

        self.table.setRowCount(len(rows))
        self.table.setColumnCount(12)
        self.table.setHorizontalHeaderLabels([
            "ID", "Ad Soyad", "Kalem", "Tutar", "Tazmin", "Açıklama", "Durum", "Tarih",
            "Limit Aşıldı mı", "Şuan Aşım Var mı", "Aşım Miktarı"
        ])

        for row_idx, row in enumerate(rows):
            for col_idx in range(11):  # First 11 columns are text
                item = QTableWidgetItem(str(row[col_idx]))
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                self.table.setItem(row_idx, col_idx, item)

            # İşlem hücresi
            action_cell = QWidget()
            action_layout = QHBoxLayout(action_cell)
            action_layout.setContentsMargins(0, 0, 0, 0)

            if row[6] == 'Beklemede':
                btn_onay = QPushButton("Onayla")
                btn_onay.setStyleSheet("background-color: #2ecc71; color: white; font-weight: bold;")
                btn_onay.clicked.connect(lambda _, id=row[0]: self.update_status(id, "Onaylandi"))

                btn_red = QPushButton("Reddet")
                btn_red.setStyleSheet("background-color: #e74c3c; color: white; font-weight: bold;")
                btn_red.clicked.connect(lambda _, id=row[0]: self.update_status(id, "Reddedildi"))

                action_layout.addWidget(btn_onay)
                action_layout.addWidget(btn_red)
            else:
                action_layout.addWidget(QLabel("-"))

            self.table.setCellWidget(row_idx, 11, action_cell)





    def update_status(self, harcama_id, new_status):
        reply = QMessageBox.question(self.central_widget, "Onay", f"Harcama {new_status} olarak güncellensin mi?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.db.update_harcama_status(harcama_id, new_status)
            self.load_data()

    def logout(self):
        from screens.loginUi import LoginUi
        self.login_window.show()  # show login again
        self.parent_window.close()  # close the current harcama window



    
