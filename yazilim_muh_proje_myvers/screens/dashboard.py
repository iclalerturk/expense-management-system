from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem
from models.database import Database
from collections import defaultdict
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from models.budget_manager import BudgetManager
import models.tahmin as tahmin
import re
class DashboardUI(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1100, 700)
        Form.setStyleSheet('''
            QWidget {
                font-family: 'Segoe UI', Arial;
                color: #333;
                background-color: #E3E4E0;
            }
            QPushButton {
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                background: #5a2d5a;
                color: white;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #755985;
            }
            QLineEdit {
                border: 1px solid #ddd;
                border-radius: 4px;
                padding: 8px;
                background: white;
            }
            QLineEdit:focus {
                border: 1px solid #755985;
            }
        ''')
        
        # Ana layout oluşturma
        self.main_layout = QtWidgets.QHBoxLayout(Form)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.stacked_widget = QtWidgets.QStackedWidget()
        self.stacked_widget.setObjectName("stacked_widget")
        self.stacked_widget.setStyleSheet('''
            background-color: #f8f9fa;
        ''')
        # ---- SOL MENÜ ----
        self.sidebar_widget = QtWidgets.QWidget()
        self.sidebar_widget.setObjectName("sidebar_widget")
        self.sidebar_widget.setMaximumWidth(130)
        self.sidebar_widget.setStyleSheet('''
            #sidebar_widget {
                background-color: #080121;
                border-right: 1px solid #34495e;
            }
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
            QPushButton:checked {
                background-color: #5a2d5a;
                border-left: 4px solid #64748B;
            }
        ''')
        
        # Sidebar layout
        self.sidebar_layout = QtWidgets.QVBoxLayout(self.sidebar_widget)
        self.sidebar_layout.setContentsMargins(0, 0, 0, 0)
        self.sidebar_layout.setSpacing(0)
        
        # Logo
        self.logo_label = QtWidgets.QLabel()
        self.logo_label.setMaximumSize(QtCore.QSize(120, 100))
        self.logo_label.setMinimumSize(QtCore.QSize(50, 50))
        self.logo_label.setPixmap(QtGui.QPixmap("images/startech.png"))
        self.logo_label.setScaledContents(True)
        self.logo_label.setStyleSheet("margin: 15px;")
        self.logo_container = QtWidgets.QWidget()
        self.logo_layout = QtWidgets.QHBoxLayout(self.logo_container)
        self.logo_layout.addWidget(self.logo_label, 0, QtCore.Qt.AlignCenter)
        self.sidebar_layout.addWidget(self.logo_container)
        
        # Menü butonları
        self.btn_home = self.create_menu_button("Ana Sayfa", "images/home.png")
        self.btn_employees = self.create_menu_button("Çalışanlar", "images/teamwork.png")
        self.btn_reports = self.create_menu_button("Raporlama", "images/growth.png")
        self.btn_tahmin = self.create_menu_button("Tahmin", "images/tahmin.png")####################
        # Butonları sidebar'a ekle
        self.sidebar_layout.addWidget(self.btn_home)
        self.sidebar_layout.addWidget(self.btn_employees)
        self.sidebar_layout.addWidget(self.btn_reports)
        self.sidebar_layout.addWidget(self.btn_tahmin)
        # Spacer ve çıkış butonu
        self.sidebar_layout.addItem(QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding))
        
        self.btn_logout = self.create_menu_button("Çıkış", "images/logout.png")
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
        self.sidebar_layout.addWidget(self.btn_logout)
        
        # ---- ANA İÇERİK ----
        self.content_widget = QtWidgets.QWidget()
        self.content_widget.setObjectName("content_widget")
        self.content_widget.setStyleSheet('''
            #content_widget {
                background-color: #f8f9fa;
            }
        ''')
        
        # Ana içerik layout
        self.content_layout = QtWidgets.QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(0)
        
        # Üst panel
        self.top_bar = QtWidgets.QWidget()
        self.top_bar.setObjectName("top_bar")
        self.top_bar.setStyleSheet('''
            #top_bar {
                background-color: white;
                border-bottom: 1px solid #ddd;
            }
            QPushButton {
                background-color: #080121;
                color: white;
                border-radius: 4px;
                padding: 8px 16px;
                margin: 0px 5px;
            }
            QPushButton:hover {
                background-color: #1b113d;
            }
            QLineEdit {
                border: 1px solid #ddd;
                border-radius: 20px;
                padding: 8px 15px;
                background: #f5f5f5;
                margin-right: 15px;
            }
        ''')
        self.top_bar.setMinimumHeight(70)
        self.top_bar.setMaximumHeight(70)
        
        # Top bar layout
        self.top_bar_layout = QtWidgets.QHBoxLayout(self.top_bar)
        self.top_bar_layout.setContentsMargins(20, 10, 20, 10)
        
        # Başlık
        self.title_label = QtWidgets.QLabel("Yönetici Paneli")
        self.title_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #333; background-color:white;")
        self.top_bar_layout.addWidget(self.title_label)
        
        # Spacer
        self.top_bar_layout.addItem(QtWidgets.QSpacerItem(100, 60, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))
        
        
        # kullanıcı profil butonu
        # self.btn_profile = QtWidgets.QPushButton()
        # self.btn_profile.setIcon(QtGui.QIcon("images/user.png"))
        # self.btn_profile.setIconSize(QtCore.QSize(30, 30))
        # self.btn_profile.setStyleSheet('''
        #     QPushButton {
        #         background-color: transparent;
        #         color: #333;
        #         border: none;
        #         padding: 5px;
        #     }
        #     QPushButton:hover {
        #         background-color: #f0f0f0;
        #     }
        # ''')
        # self.top_bar_layout.addWidget(self.btn_profile)
        
        # ana içerik sayfası
        self.content_page = QtWidgets.QWidget()
        self.content_page.setObjectName("content_page")
        self.content_page.setStyleSheet('''
            #content_page {
                background-color: #f8f9fa;
            }
        ''')
        
        # içerik sayfası layout
        self.page_layout = QtWidgets.QVBoxLayout(self.content_page)
        self.page_layout.setContentsMargins(30, 30, 30, 30)

        # İçerik kartları
        self.grid_layout = QtWidgets.QGridLayout()
        self.grid_layout.setContentsMargins(0, 0, 0, 0)
        self.grid_layout.setSpacing(20)
        
        # özet kart 1
        db = Database()
        total_calisan = db.get_total_employees()
        self.summary_card1 = self.create_summary_card("Toplam Çalışan", f"{total_calisan}", "images/teamwork.png", "#3498db")
        self.summary_card1.setFixedHeight(100)
        self.grid_layout.addWidget(self.summary_card1, 0, 0)
        
        # özet kart 2
        db = Database()
        total_butce = db.get_total_butce()
        self.summary_card2 = self.create_summary_card("Toplam Bütçe", str(total_butce), "images/calculate.png", "#2ecc71")
        self.summary_card2.setFixedHeight(100)
        self.grid_layout.addWidget(self.summary_card2, 0, 1)
        
        # özet kart 3
        db = Database()
        used_butce = db.get_used_butce()
        self.summary_card3 = self.create_summary_card("Kullanılan Bütçe",str(used_butce), "images/bill.png", "#e74c3c")
        self.summary_card3.setFixedHeight(100)
        self.grid_layout.addWidget(self.summary_card3, 0, 2)
        
        # Birim Bütçeleri Kartı
        self.budget_overview_card = QtWidgets.QWidget()
        self.budget_overview_card.setObjectName("budget_overview_card")
        self.budget_overview_card.setStyleSheet('''
            #budget_overview_card {
                background-color: white;
                border-radius: 10px;
                border: 1px solid #ddd;
            }
        ''')
        self.budget_overview_card.setMinimumHeight(400)

        self.budget_overview_layout = QtWidgets.QVBoxLayout(self.budget_overview_card)
        self.budget_overview_layout.setContentsMargins(20, 20, 20, 20)

        self.budget_overview_title = QtWidgets.QLabel("Birim - Kalem Bütçe Durumları")
        self.budget_overview_title.setStyleSheet("font-size: 16px; font-weight: bold; color: #333;background-color:white;")
        self.budget_overview_layout.addWidget(self.budget_overview_title)

        # Tablo
        self.budget_table = QtWidgets.QTableWidget()
        self.budget_table.setAlternatingRowColors(True)
        self.budget_table.setColumnCount(7)
        self.budget_table.setHorizontalHeaderLabels(["Birim Adı", "Kalem Adı", "Toplam Bütçe", "Kullanılan", "Kalan","Limit Bütçe","Aşım Oranı"])
        self.budget_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.budget_table.setEditTriggers(QtWidgets.QAbstractItemView.DoubleClicked | 
                                        QtWidgets.QAbstractItemView.EditKeyPressed)

        self.bd = BudgetManager(self.budget_table)
        # satır seçimi aktif
        self.budget_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        
        self.bd.populate_budget_table()

        # tablo düzenleme butonları:
        self.table_buttons_layout = QtWidgets.QHBoxLayout()
        self.table_buttons_layout.setContentsMargins(0, 10, 0, 0)
        self.table_buttons_layout.setSpacing(10)

        # Yeni ekle butonu
        self.btn_add_budget = QtWidgets.QPushButton("Yeni Ekle")
        self.btn_add_budget.setIcon(QtGui.QIcon("images/add.png"))  # Eğer varsa bir ikon ekleyebilirsiniz
        self.btn_add_budget.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_add_budget.setStyleSheet('''
            QPushButton {
                background-color: #2ecc71;
                color: white;
                border: none;
                padding: 10px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
        ''')
        self.btn_add_budget.clicked.connect(self.bd.add_budget_item)  # Sonra tanımlayacağız

        # Düzenle butonu
        self.btn_edit_budget = QtWidgets.QPushButton("Düzenle")
        self.btn_edit_budget.setIcon(QtGui.QIcon("images/edit.png"))  # Eğer varsa bir ikon ekleyebilirsiniz
        self.btn_edit_budget.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_edit_budget.setStyleSheet('''
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
        self.btn_edit_budget.clicked.connect(self.bd.edit_budget_item)

        # Sil butonu
        self.btn_delete_budget = QtWidgets.QPushButton("Sil")
        self.btn_delete_budget.setIcon(QtGui.QIcon("images/delete.png"))  # Eğer varsa bir ikon ekleyebilirsiniz
        self.btn_delete_budget.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.btn_delete_budget.setStyleSheet('''
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                padding: 10px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        ''')
        self.btn_delete_budget.clicked.connect(self.bd.delete_budget_item)

        self.table_buttons_layout.addWidget(self.btn_add_budget)
        self.table_buttons_layout.addWidget(self.btn_edit_budget)
        self.table_buttons_layout.addWidget(self.btn_delete_budget)

        self.budget_overview_layout.addLayout(self.table_buttons_layout)
        self.budget_overview_layout.addWidget(self.budget_table)
        self.grid_layout.addWidget(self.budget_overview_card, 1, 0, 1, 3)
        
        # 2. Bütçe Yönetimi Sayfası
        self.page_budgets = QtWidgets.QWidget()
        self.page_budgets.setObjectName("page_budgets")
        self.budgets_layout = QtWidgets.QVBoxLayout(self.page_budgets)
        self.budgets_layout.setContentsMargins(30, 30, 30, 30)
        self.budgets_layout.setSpacing(30)
        
        # içerikleri ana sayfa layouta ekle
        self.page_layout.addLayout(self.grid_layout)
        self.page_layout.addSpacing(20)
        
        self.stacked_widget.addWidget(self.content_page)
        
        # Yeni sayfa: Çalışanlar Sayfası
        self.employees_page = QtWidgets.QWidget()
        self.employees_page.setObjectName("employees_page")
        self.employees_layout = QtWidgets.QVBoxLayout(self.employees_page)
        self.employees_layout.setContentsMargins(30, 30, 30, 30)

        # Raporlama Sayfası - DÜZELTME
        self.raporlama_page = QtWidgets.QWidget()
        self.raporlama_page.setObjectName("raporlama_page")
        self.raporlama_layout = QtWidgets.QVBoxLayout(self.raporlama_page)
        self.raporlama_layout.setContentsMargins(30, 30, 30, 30)
        self.raporlama_layout.setSpacing(15)


        #Tahmin Sayfası
        self.tahmin_page = QtWidgets.QWidget()
        self.tahmin_page.setObjectName("tahmin_page")
        self.tahmin_layout = QtWidgets.QVBoxLayout(self.tahmin_page)
        self.tahmin_layout.setContentsMargins(30, 30, 30, 30)

        self.tahmin_widget = tahmin.TahminGrafikWidget()
        self.tahmin_layout.addWidget(self.tahmin_widget)
        # Buton Layoutu
        self.button_layout = QtWidgets.QHBoxLayout()
        self.button_layout.setSpacing(15)
        
        # Grafik Butonları
        self.button1 = QtWidgets.QPushButton("Birim Bazında Grafikler")
        self.button1.setStyleSheet('''
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
        
        self.button2 = QtWidgets.QPushButton("Kalem Bazında Grafikler")
        self.button2.setStyleSheet('''
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
        
        self.button3 = QtWidgets.QPushButton("Kişi Bazlında Grafikler")
        self.button3.setStyleSheet('''
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
        
        # Butonları ekle
        self.button_layout.addWidget(self.button1)
        self.button_layout.addWidget(self.button2)
        self.button_layout.addWidget(self.button3)
        
        # Önce butonları ekle
        self.raporlama_layout.addLayout(self.button_layout)
        
        # Scroll Area'yı hazırla
        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet('''
            QScrollArea {
                background-color: #f8f9fa;
                border: none;
            }
        ''')

        # Grafik alanını scroll içinde göster
        self.graphic_container = QtWidgets.QWidget()
        self.graphic_container.setMinimumHeight(1000)  # Daha uzun bir alan oluşturarak scroll etmeyi garantile
        self.graphic_layout = QtWidgets.QVBoxLayout(self.graphic_container)
        self.graphic_layout.setContentsMargins(15, 15, 15, 15)
        self.graphic_layout.setSpacing(40) 
        
        # Grafik için Filtre Bölümü
        self.filter_widget = QtWidgets.QWidget()
        self.filter_widget.setStyleSheet('''
            QWidget {
                background-color: white;
                border-radius: 8px;
                border: 1px solid #ddd;
            }
            QLabel {
                font-weight: bold;
                background-color: transparent;
            }
            QComboBox {
                border: 1px solid #ddd;
                border-radius: 4px;
                padding: 5px;
                background: white;
                min-height: 30px;
            }
        ''')
        self.filter_layout = QtWidgets.QVBoxLayout(self.filter_widget)
        self.filter_layout.setContentsMargins(15, 15, 15, 15)
        self.filter_layout.setSpacing(10)
        
        # Filtre Elemanları
        # Kişi Seçimi
        self.kisi_label = QtWidgets.QLabel("Kişi Seçiniz:")
        self.kisi_combo = QtWidgets.QComboBox()
        self.kisi_combo.setMinimumWidth(300)
        self.sec_buttonKisi = QtWidgets.QPushButton("Grafiği Göster")
        self.sec_buttonKisi.setStyleSheet('''
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
        
        # Birim Seçimi
        self.birim_label = QtWidgets.QLabel("Birim Seçiniz:")
        self.birim_combo = QtWidgets.QComboBox()
        self.birim_combo.setMinimumWidth(300)
        self.sec_buttonBirim = QtWidgets.QPushButton("Grafiği Göster")
        self.sec_buttonBirim.setStyleSheet('''
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
        
        # Kalem Seçimi
        self.kalem_label = QtWidgets.QLabel("Kalem Seçiniz:")
        self.kalem_combo = QtWidgets.QComboBox()
        self.kalem_combo.setMinimumWidth(300)
        self.sec_buttonKalem = QtWidgets.QPushButton("Grafiği Göster")
        self.sec_buttonKalem.setStyleSheet('''
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
        
        # Başlangıçta tüm filtreler gizli
        self.kisi_label.setVisible(False)
        self.kisi_combo.setVisible(False)
        self.sec_buttonKisi.setVisible(False)
        self.birim_label.setVisible(False)
        self.birim_combo.setVisible(False)
        self.sec_buttonBirim.setVisible(False)
        self.kalem_label.setVisible(False)
        self.kalem_combo.setVisible(False)
        self.sec_buttonKalem.setVisible(False)
        
        # Filtreler ekleniyor
        self.filter_layout.addWidget(self.kisi_label)
        self.filter_layout.addWidget(self.kisi_combo)
        self.filter_layout.addWidget(self.sec_buttonKisi)
        self.filter_layout.addWidget(self.birim_label)
        self.filter_layout.addWidget(self.birim_combo)
        self.filter_layout.addWidget(self.sec_buttonBirim)
        self.filter_layout.addWidget(self.kalem_label)
        self.filter_layout.addWidget(self.kalem_combo)
        self.filter_layout.addWidget(self.sec_buttonKalem)
        
        # Filtre Widget'ı Grafik Düzenine Ekleniyor
        self.graphic_layout.addWidget(self.filter_widget)
        
        # Grafik Canvas'ı ekle
        self.chart_widget = QtWidgets.QWidget()
        self.chart_widget.setStyleSheet('''
            background-color: white;
            border-radius: 8px;
            border: 1px solid #ddd;
            padding: 10px;
        ''')
        self.chart_layout = QtWidgets.QVBoxLayout(self.chart_widget)
        self.chart_layout.setContentsMargins(15, 15, 15, 15)
        
        self.canvas = FigureCanvas(Figure(figsize=(8, 6)))
        self.ax = self.canvas.figure.add_subplot(111)
        self.chart_layout.addWidget(self.canvas)
        
        # Grafik Widget'ı ekle
        self.graphic_layout.addWidget(self.chart_widget)
        
        self.chart_widget2 = QtWidgets.QWidget()
        self.chart_widget2.setStyleSheet('''
            background-color: white;
            border-radius: 8px;
            border: 1px solid #ddd;
            padding: 10px;
        ''')
        self.chart_layout2 = QtWidgets.QVBoxLayout(self.chart_widget2)
        self.chart_layout2.setContentsMargins(15, 15, 15, 15)

        # Başlık ekle
        self.pie_chart_title = QtWidgets.QLabel("Birim Harcama Dağılımı")
        self.pie_chart_title.setStyleSheet("font-size: 16px; font-weight: bold; color: #333; background-color: transparent;")
        self.chart_layout2.addWidget(self.pie_chart_title)

        # Pie chart için canvas oluştur
        self.canvas2 = FigureCanvas(Figure(figsize=(8, 6)))
        self.ax2 = self.canvas2.figure.add_subplot(111)
        self.chart_layout2.addWidget(self.canvas2)

        # İkinci grafik Widget'ı ekle
        self.graphic_layout.addWidget(self.chart_widget2)

        self.scroll_area.setWidget(self.graphic_container)        
        # Raporlama layout'a Scroll Area'yı ekle
        self.raporlama_layout.addWidget(self.scroll_area)
        
        # Örnek çalışanlar tablosu
        self.employees_table = QtWidgets.QTableWidget()
        self.employees_table.setColumnCount(5)
        self.employees_table.setHorizontalHeaderLabels(["Calışan Id","Ad", "Soyad", "Departman", "İletişim"])
        self.employees_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.populate_employee_table()  # Çalışanları veritabanından alıp tabloya ekleyecek bir metod
        self.employees_table.setStyleSheet('''
            QTableWidget {
                background-color: white;
                border-radius: 20px;
                border: 1px solid #ddd;
                padding: 5px;  /* İç boşluk ekleyerek içeriğin çerçeveye yapışmasını önle */
            }
            QTableWidget::item {
                padding: 10px;
            }
            QTableWidget QHeaderView::section {
                background-color: transparent;
            }
            QTableWidget::viewport {  /* İç içerik alanını yuvarlat */
                border-radius: 18px;  /* Ana çerçevenin radius'undan biraz küçük */
            }
        ''')
        self.employees_layout.addWidget(self.employees_table)

        # Sayfaları stacked_widget'e ekle
        self.stacked_widget.addWidget(self.employees_page)
        self.stacked_widget.addWidget(self.raporlama_page)
        self.stacked_widget.addWidget(self.tahmin_page)
        # içerikleri ana içerik layouta ekle
        self.content_layout.addWidget(self.top_bar)
        self.content_layout.addWidget(self.stacked_widget)
        
        # ana widgetları main layouta ekle
        self.main_layout.addWidget(self.sidebar_widget)
        self.main_layout.addWidget(self.content_widget)
        
        # Buton bağlantıları
        self.btn_home.setChecked(True)
        self.btn_home.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.content_page))
        self.btn_employees.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.employees_page))
        self.btn_reports.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.raporlama_page))
        self.btn_tahmin.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.tahmin_page))

        self.button1.clicked.connect(self.birim_grafik_baslat)
        self.button2.clicked.connect(self.kalem_grafik_baslat)
        self.button3.clicked.connect(self.kisi_grafik_baslat)
        self.sec_buttonKisi.clicked.connect(self.grafik_kisi_sec)
        self.sec_buttonKalem.clicked.connect(self.grafik_kalem_sec)
        self.sec_buttonBirim.clicked.connect(self.grafik_birim_sec)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    

    def grafik_kisi_sec(self):
        secim = self.kisi_combo.currentText()
        if not secim:
            return
        calisan_id = secim.split(" - ")[0]
        self.grafik_guncelle_filtreli("kisi", calisan_id)
        self.pie_chart_calisan_vs_digerleri(calisan_id)
        self.chart_widget2.setVisible(True)

    def grafik_kalem_sec(self):
        secim = self.kalem_combo.currentText()
        if not secim:
            return
        kalem_id = secim.split(" - ")[0]
        self.grafik_guncelle_kalem_birim(kalem_id)
        self.pie_chart_kalem_guncelle(secim)
        self.chart_widget2.setVisible(True)
    
    def grafik_birim_sec(self):
        secim_birim = self.birim_combo.currentText()
        if not secim_birim:
            return
        birim_id = int(secim_birim.split(" - ")[0])
        #self.grafik_guncelle_filtreli("birim", birim_id)
        self.grafik_guncelle_birim_kalem(birim_id)
        self.pie_chart_birim_guncelle(secim_birim)
        self.chart_widget2.setVisible(True)
    
    def pie_chart_birim_guncelle(self, secilen_birim):
        db = Database()

        birim_parcalari = secilen_birim.split(" - ")
        if len(birim_parcalari) >= 1:
            secilen_birim_id = birim_parcalari[0]  # "1 - Satış" -> "1"
            try:
                secilen_birim_id = int(secilen_birim_id)
            except ValueError:
                print(f"Birim ID'si bir sayı değil: {secilen_birim_id}")
                return
        else:
            print(f"Birim adı ayrıştırılamadı: {secilen_birim}")
            return
        
        print(f"Seçilen birim ID: {secilen_birim_id}")
        
        # Tüm birimlerin toplam harcamalarını al
        tum_birim_harcamalari = db.get_birim_harcamalari()  # birimId, toplam_tutar şeklinde dönüyor
        
        secilen_birim_harcama = 0
        diger_birimler_harcama = 0
        
        # Harcama tutarlarını topla
        for birim_id, harcama in tum_birim_harcamalari:
            if birim_id == secilen_birim_id:
                secilen_birim_harcama = harcama
            else:
                diger_birimler_harcama += harcama
        
        print(f"Seçilen birim ({secilen_birim}) harcaması: {secilen_birim_harcama}")
        print(f"Diğer birimler toplam harcaması: {diger_birimler_harcama}")
        
        # Pie chart'ı temizle ve yeniden çiz
        self.ax2.clear()
        
        # Birim adının sadece isim kısmını kullan (ID'yi çıkar)
        birim_adi = " - ".join(birim_parcalari[1:]) if len(birim_parcalari) > 1 else secilen_birim
        
        labels = [birim_adi, 'Diğer Birimler']
        sizes = [secilen_birim_harcama, diger_birimler_harcama]
        
        # Eğer herhangi bir harcama yoksa, varsayılan değerler kullan
        if secilen_birim_harcama == 0 and diger_birimler_harcama == 0:
            print("Hiç harcama verisi bulunamadı!")
            sizes = [1, 1]  # Görsel olarak eşit göstermek için
        
        colors = ['#c2a3fd', '#e13661']
        explode = (0.1, 0)  # Seçilen birimi vurgulamak için
        
        self.ax2.pie(sizes, explode=explode, labels=labels, colors=colors,
                autopct='%1.1f%%', shadow=True, startangle=90)
        self.ax2.axis('equal')  # Dairesel gösterim için
        
        self.pie_chart_title.setText(f"{birim_adi} Birimi vs Diğer Birimler Harcama Dağılımı")
        
        self.canvas2.draw()
        
    def grafik_guncelle_kalem_birim(self, kalem_id):
        try:
            db = Database()
            data = db.get_birim_comparison_by_kalem(kalem_id)
            
            if not data:
                QtWidgets.QMessageBox.warning(self.raporlama_page, "Uyarı", "Kalem için veri bulunamadı.")
                return

            self.ax.clear()
            birim_adlari = [row[0] for row in data]
            total_amounts = [row[1] for row in data]

            index = np.arange(len(birim_adlari))
            bar_width = 0.6

            self.ax.bar(index, total_amounts, bar_width, color='#2ecc71')
            
            self.ax.set_xlabel('Birim Adı')
            self.ax.set_ylabel('Toplam Harcama (TL)')
            self.ax.set_title('Kalem Bazında Birim Harcamaları')
            self.ax.set_xticks(index)
            self.ax.set_xticklabels(birim_adlari, rotation=0, ha='right')
            self.canvas.draw()

        except Exception as e:
            QtWidgets.QMessageBox.warning(self.raporlama_page, "Hata", f"Bir hata oluştu: {str(e)}")

    def pie_chart_kalem_guncelle(self, secilen_kalem):
        db = Database()
        
        # İlk olarak kalem adından ID'yi çıkaralım (format: "1 - Kırtasiye")
        kalem_parcalari = secilen_kalem.split(" - ")
        
        if len(kalem_parcalari) >= 1:
            secilen_kalem_id = kalem_parcalari[0]
            try:
                secilen_kalem_id = int(secilen_kalem_id)
            except ValueError:
                print(f"Kalem ID'si bir sayı değil: {secilen_kalem_id}")
                return
        else:
            print(f"Kalem adı ayrıştırılamadı: {secilen_kalem}")
            return
        
        print(f"Seçilen kalem ID: {secilen_kalem_id}")
        
        # Tüm kalemlerin toplam harcamalarını al
        tum_kalem_harcamalari = db.get_kalem_harcamalari()  # kalemId, toplam_tutar şeklinde dönüyor
        
        secilen_kalem_harcama = 0
        diger_kalemler_harcama = 0
        
        # Harcama tutarlarını topla
        for kalem_id, harcama in tum_kalem_harcamalari:
            if kalem_id == secilen_kalem_id:
                secilen_kalem_harcama = harcama
            else:
                diger_kalemler_harcama += harcama
        
        print(f"Seçilen kalem ({secilen_kalem}) harcaması: {secilen_kalem_harcama}")
        print(f"Diğer kalemler toplam harcaması: {diger_kalemler_harcama}")
        
        self.ax2.clear()
        
        # Kalem adının sadece isim kısmını kullan (ID'yi çıkar)
        kalem_adi = " - ".join(kalem_parcalari[1:]) if len(kalem_parcalari) > 1 else secilen_kalem
        
        labels = [kalem_adi, 'Diğer Kalemler']
        sizes = [secilen_kalem_harcama, diger_kalemler_harcama]
        
        # Eğer herhangi bir harcama yoksa, varsayılan değerler kullan
        if secilen_kalem_harcama == 0 and diger_kalemler_harcama == 0:
            print("Hiç harcama verisi bulunamadı!")
            sizes = [1, 1]
        
        colors = ['#c2a3fd', '#e13661']
        explode = (0.1, 0)
        
        self.ax2.pie(sizes, explode=explode, labels=labels, colors=colors,
                autopct='%1.1f%%', shadow=True, startangle=90)
        self.ax2.axis('equal')
        
        self.pie_chart_title.setText(f"{kalem_adi} Kalemi vs Diğer Kalemler Harcama Dağılımı")
        
        self.canvas2.draw()
    
    def pie_chart_calisan_vs_digerleri(self, secilen_calisan_id):
        try:
            calisan_id = None
            secilen_kisi_adi = None
            
            if isinstance(secilen_calisan_id, int) or (isinstance(secilen_calisan_id, str) and secilen_calisan_id.isdigit()):
                calisan_id = int(secilen_calisan_id)
                db = Database()
                result = db.get_calisan_by_id(calisan_id)
                if result:
                    secilen_kisi_adi = result
                else:
                    secilen_kisi_adi = f"Çalışan {calisan_id}"
            else:
                parts = str(secilen_calisan_id).split(" - ")
                if len(parts) >= 2:
                    try:
                        calisan_id = int(parts[0])
                        secilen_kisi_adi = parts[1].strip()
                    except ValueError:
                        print(f"Kişi ID'si ayrıştırılamadı: {secilen_calisan_id}")
                        QtWidgets.QMessageBox.warning(self.raporlama_page, "Hata", "Seçilen kişi formatı geçersiz.")
                        return
                else:
                    print(f"Kişi adı ayrıştırılamadı: {secilen_calisan_id}")
                    QtWidgets.QMessageBox.warning(self.raporlama_page, "Hata", "Seçilen kişi formatı geçersiz.")
                    return
                    
            print(f"Seçilen kişi ID: {calisan_id}, adı: {secilen_kisi_adi}")
            
            db = Database()
            sonuclar = db.calisan_digerleri_by_birim(calisan_id)
            
            if not sonuclar or len(sonuclar) < 2:
                QtWidgets.QMessageBox.information(self.raporlama_page, "Bilgi", 
                                                "Karşılaştırma için veri bulunamadı.")
                return
            
            secilen_kisi_harcama = sonuclar[0] or 0  # İlk değer seçilen çalışanın toplamı
            diger_kisiler_harcama = sonuclar[1] or 0  # İkinci değer diğer çalışanların toplamı
            
            print(f"Seçilen kişi ({secilen_kisi_adi}) harcaması: {secilen_kisi_harcama}")
            print(f"Diğer kişilerin toplam harcaması: {diger_kisiler_harcama}")
            
            self.ax2.clear()
            
            if secilen_kisi_harcama == 0 and diger_kisiler_harcama == 0:
                QtWidgets.QMessageBox.information(self.raporlama_page, "Bilgi", 
                                                "Seçilen kişi ve diğerleri için harcama bulunamadı.")

                self.pie_chart_title.setText(f"{secilen_kisi_adi} vs Diğer Kişiler Harcama Dağılımı")
                self.canvas2.draw()
                return

            if secilen_kisi_harcama == 0:
                secilen_kisi_harcama = 0.001  # Çok küçük bir değer
            if diger_kisiler_harcama == 0:
                diger_kisiler_harcama = 0.001  # Çok küçük bir değer
            
            sizes = [secilen_kisi_harcama, diger_kisiler_harcama]
            labels = [secilen_kisi_adi, 'Diğer Kişiler']
            colors = ['#c2a3fd', '#e13661']
            explode = (0.1, 0)  # Seçilen kişiyi vurgulamak için

            self.ax2.pie(sizes, explode=explode, labels=labels, colors=colors,
                    autopct='%1.1f%%', shadow=True, startangle=90)
            self.ax2.axis('equal')
            
            self.pie_chart_title.setText(f"{secilen_kisi_adi} vs Diğer Kişiler Harcama Dağılımı")
            self.canvas2.draw()
            
        except Exception as e:
            print(f"Pie chart oluşturulurken hata: {str(e)}")
            QtWidgets.QMessageBox.critical(self.raporlama_page, "Hata", 
                                        f"Grafik oluşturulurken bir hata oluştu: {str(e)}")
        
    def kisi_grafik_baslat(self):
        self.kalem_label.setVisible(False)
        self.kalem_combo.setVisible(False)
        self.sec_buttonKalem.setVisible(False)
        self.birim_label.setVisible(False)
        self.birim_combo.setVisible(False)
        self.sec_buttonBirim.setVisible(False)
        self.kisi_label.setVisible(True)
        self.kisi_combo.clear()
            # self.kisi_combo.addItems(veriler.keys())  # Kişi adları
        self.kisi_combo.setVisible(True)
        self.sec_buttonKisi.setVisible(True)
        db=Database()
        data = db.get_all_calisanlar()
        self.kisi_combo.clear()
        for row in data:
            calisan_id = row[0]
            isim = row[1]
            soyisim = row[2]
            birim = row[3]
            email = row[4]
            self.kisi_combo.addItem(f"{calisan_id} - {isim} {soyisim} - {birim} - {email}")  # Kişi adları ve ID'leri

    def birim_grafik_baslat(self):
        self.kisi_label.setVisible(False)
        self.kisi_combo.setVisible(False)
        self.sec_buttonKisi.setVisible(False)
        self.kalem_label.setVisible(False)
        self.kalem_combo.setVisible(False)
        self.sec_buttonKalem.setVisible(False)
        self.birim_label.setVisible(True)
        self.birim_combo.clear()
        # self.birim_combo.addItems(veriler.keys())  # Birim adları
        self.birim_combo.setVisible(True)
        self.sec_buttonBirim.setVisible(True)
        db=Database()
        data = db.get_birimler()
        self.birim_combo.clear()
        for row in data:
            birim_id = row[0]
            birim_adi = row[1]
            self.birim_combo.addItem(f"{birim_id} - {birim_adi}")  # Birim adları ve ID'leri

    def kalem_grafik_baslat(self):
        self.kisi_label.setVisible(False)
        self.kisi_combo.setVisible(False)
        self.sec_buttonKisi.setVisible(False)
        self.birim_label.setVisible(False)
        self.birim_combo.setVisible(False)
        self.sec_buttonBirim.setVisible(False)
        self.kalem_label.setVisible(True)
        self.kalem_combo.clear()
        # self.kalem_combo.addItems(veriler.keys())  # Kalem adları
        self.kalem_combo.setVisible(True)
        self.sec_buttonKalem.setVisible(True)
        db=Database()
        data = db.get_kalemler()
        self.kalem_combo.clear()
        for row in data:
            kalem_id = row[0]
            kalem_adi = row[1]
            self.kalem_combo.addItem(f"{kalem_id} - {kalem_adi}")  # Kalem adları ve ID'leri

    def grafik_guncelle_filtreli(self, kategori, secilen_id):
        try:
            db = Database()
            data = db.grafik_verisi_getir(kategori, secilen_id)  # Parametreli veri çekimi
            
            if not data:
                QtWidgets.QMessageBox.warning(self.raporlama_page, "Uyarı", f"{kategori.capitalize()} için veri bulunamadı.")
                return

            self.ax.clear()
            all_years = set()
            for entity_data in data.values():
                all_years.update(entity_data.keys())
            all_years = sorted(all_years)
            bars = []
            bar_width = 0.8 / len(data)
            index = np.arange(len(all_years))

            for i, (entity_name, yearly_data) in enumerate(data.items()):
                values = [yearly_data.get(year, 0) for year in all_years]
                position = index + i * bar_width
                bar = self.ax.bar(position, values, bar_width, label=entity_name)
                bars.append(bar)

            kategori_basliklari = {
                'birim': 'Birim - Kalem Bazında Yıllık Harcamalar',
                'kalem': 'Harcama Kalemi Bazında Yıllık Harcamalar',
                'kisi': 'Kişi Bazında Yıllık Harcamalar'
            }

            self.ax.set_xlabel('Yıl')
            self.ax.set_ylabel('Toplam Harcama (TL)')
            self.ax.set_title(kategori_basliklari.get(kategori, 'Yıllık Harcamalar'))
            self.ax.set_xticks(index + bar_width * (len(data) - 1) / 2)
            self.ax.set_xticklabels(all_years)
            self.ax.legend()
            self.canvas.draw()

        except Exception as e:
            QtWidgets.QMessageBox.critical(self.raporlama_page, "Hata", f"Grafik güncellenirken bir hata oluştu: {str(e)}")

    def grafik_guncelle_birim_kalem(self, birim_id):
        try:
            db = Database()
            data = db.get_kalem_comparison_by_birim(birim_id)
            
            if not data:
                QtWidgets.QMessageBox.warning(self.raporlama_page, "Uyarı", "Birim için veri bulunamadı.")
                return

            self.ax.clear()
            kalem_adlari = [row[0] for row in data]
            total_amounts = [row[1] for row in data]

            index = np.arange(len(kalem_adlari))
            bar_width = 0.6

            self.ax.bar(index, total_amounts, bar_width)
            
            self.ax.set_xlabel('Kalem Adı')
            self.ax.set_ylabel('Toplam Harcama (TL)')
            self.ax.set_title('Birim Bazında Kalem Harcamaları')
            self.ax.set_xticks(index)
            self.ax.set_xticklabels(kalem_adlari, rotation=0, ha='right')
            self.ax.legend(['Harcamalar'])
            self.canvas.draw()

        except Exception as e:
            QtWidgets.QMessageBox.warning(self.raporlama_page, "Hata", f"Bir hata oluştu: {str(e)}")
    
    def create_menu_button(self, text, icon_path):
        button = QtWidgets.QPushButton(text)
        button.setIcon(QtGui.QIcon(icon_path))
        button.setIconSize(QtCore.QSize(24, 24))
        button.setStyleSheet("""
        QPushButton {
            text-align: left;
            padding: 8px;
            font-size: 14px;
        }
        """)
        button.setMinimumHeight(40)
        return button

    def create_summary_card(self, title, value, icon_path, color):
        safe_title = re.sub(r'[^a-zA-Z0-9_]', '_', title.lower())
        
        card = QtWidgets.QWidget()
        card.setObjectName(f"card_{safe_title}")
        
        # Apply stylesheet without using objectName in selectors
        general_style = f'''
            background-color: white;
            border-radius: 10px;
            border: 1px solid #ddd;
        '''
        card.setStyleSheet(general_style)
        
        # Set minimum height
        card.setMinimumHeight(120)
        
        # Create layout
        layout = QtWidgets.QHBoxLayout(card)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Create and style icon
        icon_label = QtWidgets.QLabel()
        icon_label.setMaximumSize(QtCore.QSize(48, 48))
        icon_label.setMinimumSize(QtCore.QSize(48, 48))
        icon_label.setPixmap(QtGui.QPixmap(icon_path))
        icon_label.setScaledContents(True)
        icon_label.setStyleSheet(f'''
            border-radius: 24px;
            background-color: {color}30;
            padding: 10px;
        ''')
        
        # Create and style value label
        value_label = QtWidgets.QLabel(value)
        value_label.setStyleSheet(f'''
            font-size: 28px;
            font-weight: bold;
            color: {color};
        ''')
        
        # Create and style title label
        title_label = QtWidgets.QLabel(title)
        title_label.setStyleSheet('''
            font-size: 14px;
            color: #666;
        ''')
        
        # Create text layout and add labels
        text_layout = QtWidgets.QVBoxLayout()
        text_layout.addWidget(value_label)
        text_layout.addWidget(title_label)
        
        # Add everything to main layout
        layout.addWidget(icon_label)
        layout.addSpacing(15)
        layout.addLayout(text_layout)
        layout.addItem(QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))
        
        return card

    def populate_employee_table(self):
        db = Database()
        data = db.get_all_calisanlar()
        self.employees_table.setRowCount(len(data))

        for row_index, row in enumerate(data):
            calisan_id = QTableWidgetItem(str(row[0]))  # calisanId
            isim = QTableWidgetItem(str(row[1]))        # isim
            soyisim = QTableWidgetItem(str(row[2]))     # soyisim
            birim = QTableWidgetItem(str(row[3]))       # birimIsmi
            email = QTableWidgetItem(str(row[4]))       # email

            self.employees_table.setItem(row_index, 0, calisan_id)
            self.employees_table.setItem(row_index, 1, isim)
            self.employees_table.setItem(row_index, 2, soyisim)
            self.employees_table.setItem(row_index, 3, birim)
            self.employees_table.setItem(row_index, 4, email)

            # Alternatif satır renkleme
            if row_index % 2 == 0:
                for col_index in range(self.employees_table.columnCount()):
                    item = self.employees_table.item(row_index, col_index)
                    item.setBackground(QtGui.QColor(236, 240, 241))  # Beyaz
            else:
                for col_index in range(self.employees_table.columnCount()):
                    item = self.employees_table.item(row_index, col_index)
                    item.setBackground(QtGui.QColor(245, 245, 245))  # Alternatif renk

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Yönetici Paneli"))