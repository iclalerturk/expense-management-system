# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem
from models.database import Database
from collections import defaultdict
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

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
        
        # Butonları sidebar'a ekle
        self.sidebar_layout.addWidget(self.btn_home)
        self.sidebar_layout.addWidget(self.btn_employees)
        self.sidebar_layout.addWidget(self.btn_reports)
        
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
        
        # Arama kutusu -> silinebilir, şu an bir işleve sahip değil
        self.search_edit = QtWidgets.QLineEdit()
        self.search_edit.setPlaceholderText("Ara...")
        self.search_edit.setMinimumWidth(250)
        self.top_bar_layout.addWidget(self.search_edit)
        
        # kullanıcı profil butonu
        self.btn_profile = QtWidgets.QPushButton()
        self.btn_profile.setIcon(QtGui.QIcon("images/user.png"))
        self.btn_profile.setIconSize(QtCore.QSize(30, 30))
        self.btn_profile.setStyleSheet('''
            QPushButton {
                background-color: transparent;
                color: #333;
                border: none;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #f0f0f0;
            }
        ''')
        self.top_bar_layout.addWidget(self.btn_profile)
        
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

        # satır seçimi aktif
        self.budget_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        
        self.populate_budget_table()

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
        self.btn_add_budget.clicked.connect(self.add_budget_item)  # Sonra tanımlayacağız

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
        self.btn_edit_budget.clicked.connect(self.edit_budget_item)

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
        self.btn_delete_budget.clicked.connect(self.delete_budget_item)

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


        self.raporlama_page = QtWidgets.QWidget()
        self.raporlama_page.setObjectName("employees_page")
        self.raporlama_layout = QtWidgets.QVBoxLayout(self.raporlama_page)
        self.raporlama_layout.setContentsMargins(30, 30, 30, 30)
        self.button_layout = QtWidgets.QHBoxLayout()

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
        self.button_layout.addWidget(self.button1)
        self.button_layout.addWidget(self.button2)
        self.button_layout.addWidget(self.button3)

        # Grafik alanı için boş bir widget (şimdilik)
        self.graphic_area = QtWidgets.QFrame()
        self.graphic_area.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.graphic_area.setMinimumHeight(300)  # İstersen yüksekliği sabitleyebilirsin

        # Ana layout'a ekle
        self.raporlama_layout.addLayout(self.button_layout)
        self.raporlama_layout.addWidget(self.graphic_area)

        self.graphic_layout = QtWidgets.QVBoxLayout(self.graphic_area)
        self.canvas = FigureCanvas(Figure(figsize=(6, 4)))
        self.ax = self.canvas.figure.add_subplot(111)
        self.graphic_layout.addWidget(self.canvas)


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

        # employees_page'i stacked_widget'e ekle
        self.stacked_widget.addWidget(self.employees_page)
        # raporlama_page'i stacked_widget'e ekle
        self.stacked_widget.addWidget(self.raporlama_page)
        # raporlama_page'i stacked_widget'e ekle
        self.stacked_widget.addWidget(self.raporlama_page)
        # içerikleri ana içerik layouta ekle
        self.content_layout.addWidget(self.top_bar)
        self.content_layout.addWidget(self.stacked_widget)
        
        # ana widgetları main layouta ekle
        self.main_layout.addWidget(self.sidebar_widget)
        self.main_layout.addWidget(self.content_widget)
        
        self.btn_home.setChecked(True)
        self.btn_home.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.content_page))
        self.btn_employees.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.employees_page))
        self.btn_reports.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.raporlama_page))
        self.button1.clicked.connect(lambda: self.update_graph('birim'))
        self.button2.clicked.connect(lambda: self.update_graph('kalem'))
        self.button3.clicked.connect(lambda: self.update_graph('kisi'))
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def update_graph(self, kategori):
        try:
            db = Database()
            data = db.grafik_verisi_getir(kategori)
            
            if not data:
                QtWidgets.QMessageBox.warning(self.raporlama_page, "Uyarı", f"{kategori.capitalize()} için veri bulunamadı.")
                return
                
            # Mevcut grafiği temizle
            self.ax.clear()
            
            # Tüm yılları topla ve sırala
            all_years = set()
            for entity_data in data.values():
                all_years.update(entity_data.keys())
            all_years = sorted(all_years)
            
            # Her bir varlık için yıllara göre verileri düzenle
            bars = []
            bar_width = 0.8 / len(data)  # Çubukların genişliği
            index = np.arange(len(all_years))
            
            # Her bir varlık için çubuk ekle
            for i, (entity_name, yearly_data) in enumerate(data.items()):
                values = [yearly_data.get(year, 0) for year in all_years]
                position = index + i * bar_width
                bar = self.ax.bar(position, values, bar_width, label=entity_name)
                bars.append(bar)
            
            # Eksen etiketleri ve başlık
            kategori_basliklari = {
                'birim': 'Birim Bazında Yıllık Harcamalar',
                'kalem': 'Harcama Kalemi Bazında Yıllık Harcamalar',
                'kisi': 'Kişi Bazında Yıllık Harcamalar'
            }
            
            self.ax.set_xlabel('Yıl')
            self.ax.set_ylabel('Toplam Harcama (TL)')
            self.ax.set_title(kategori_basliklari.get(kategori, 'Yıllık Harcamalar'))
            self.ax.set_xticks(index + bar_width * (len(data) - 1) / 2)
            self.ax.set_xticklabels(all_years)
            self.ax.legend()
            
            # Grafiği güncelle
            self.canvas.draw()
            
        except Exception as e:
            # Use a valid parent widget (self.raporlama_page is a QWidget)
            QtWidgets.QMessageBox.critical(self.raporlama_page, "Hata", f"Grafik güncellenirken bir hata oluştu: {str(e)}")

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
        card = QtWidgets.QWidget()
        card.setObjectName(f"card_{title.lower().replace(' ', '_')}")
        card.setStyleSheet(f'''
            #{card.objectName()} {{
                background-color: white;
                border-radius: 10px;
                border: 1px solid #ddd;
            }}
            QLabel[objectName^="card_value"] {{
                font-size: 28px;
                font-weight: bold;
                color: {color};
            }}
            QLabel[objectName^="card_title"] {{
                font-size: 14px;
                color: #666;
            }}
        ''')
        card.setMinimumHeight(120)
        
        layout = QtWidgets.QHBoxLayout(card)
        layout.setContentsMargins(20, 20, 20, 20)
        
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
        
        value_label = QtWidgets.QLabel(value)
        value_label.setObjectName(f"card_value_{title.lower().replace(' ', '_')}")
        
        title_label = QtWidgets.QLabel(title)
        title_label.setObjectName(f"card_title_{title.lower().replace(' ', '_')}")
        
        text_layout = QtWidgets.QVBoxLayout()
        text_layout.addWidget(value_label)
        text_layout.addWidget(title_label)
        
        layout.addWidget(icon_label)
        layout.addSpacing(15)
        layout.addLayout(text_layout)
        layout.addItem(QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum))
        
        return card
    
    def populate_budget_table(self):
        db = Database()
        data = db.get_unit_and_kalem_budget()  # DB sınıfındaki metodun döndürdüğü liste

        self.budget_table.setRowCount(len(data))

        for row_index, row in enumerate(data):
            birim_adi = QTableWidgetItem(str(row["Birim Adı"]))
            kalem_adi = QTableWidgetItem(str(row["Kalem Adı"]))
            limit_butce = row['Limit Bütçe']
            esik_deger = row['Aşım Oranı']
            # get_unit_and_kalem_budget'den gelen yeni anahtar isimlerini kullan
            toplam_butce = row['Toplam Bütçe'] if 'Toplam Bütçe' in row else row['Tahsis Edilen Bütçe']
            kullanilan_butce = row['Kullanılan Bütçe']
            
            # QTableWidgetItem'leri oluştur
            limit_butce_item = QTableWidgetItem(f"{limit_butce:.2f}")
            toplam_butce_item = QTableWidgetItem(f"{toplam_butce:.2f}")
            kullanilan_item = QTableWidgetItem(f"{kullanilan_butce:.2f}")
            esik_deger_item = QTableWidgetItem(f"{int(esik_deger)}")
            kalan_item = QTableWidgetItem(f"{(toplam_butce - kullanilan_butce):.2f}")

            self.budget_table.setItem(row_index, 0, birim_adi)
            self.budget_table.setItem(row_index, 1, kalem_adi)
            self.budget_table.setItem(row_index, 2, toplam_butce_item)
            self.budget_table.setItem(row_index, 3, kullanilan_item)
            self.budget_table.setItem(row_index, 4, kalan_item)
            self.budget_table.setItem(row_index, 5, limit_butce_item)
            self.budget_table.setItem(row_index, 6, esik_deger_item)

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

    def add_budget_item(self):
        """
        Yeni limit bütçe eklemek için bir dialog gösterir ve bütçeyi veritabanına ekler
        """
        db = Database()
        dialog = QtWidgets.QDialog()
        dialog.setWindowTitle("Yeni Bütçe Ekle")
        dialog.setFixedWidth(800)
        dialog.setStyleSheet("background-color: white;")
        
        layout = QtWidgets.QVBoxLayout(dialog)
        
        title_label = QtWidgets.QLabel("Yeni Bütçe Ekleme Ekranı")
        title_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #2c3e50; margin-bottom: 10px;")
        layout.addWidget(title_label)
        
        form_layout = QtWidgets.QFormLayout()
        birim_combo = QtWidgets.QComboBox()
        birim_combo.addItem("Birim Seçin", None)
        
        birimler = [
            (1, "Satış"),
            (2, "Pazarlama"),
            (3, "Ar-Ge"),
            (4, "Muhasebe"),
            (5, "IT")
        ]
        for birim_id, birim_adi in birimler:
            birim_combo.addItem(birim_adi, birim_id)
        
        # Kalem seçimi
        kalem_combo = QtWidgets.QComboBox()
        kalem_combo.addItem("Kalem Seçin", None)
        
        # Veritabanından kalem listesini al
        try:
            db.cursor.execute("SELECT kalemAd FROM harcamakalemi")
            kalemler = [row[0] for row in db.cursor.fetchall()]
            
            for kalem_adi in kalemler:
                kalem_combo.addItem(kalem_adi, kalem_adi)
        except Exception as e:
            print(f"Kalem listesi yükleme hatası: {e}")
            kalemler = ["Taksi", "Otopark", "Benzin", "Ofis Malzemesi", "Konaklama", "Yemek"]
            for kalem_adi in kalemler:
                kalem_combo.addItem(kalem_adi, kalem_adi)
        
        # Toplam bütçe girişi için validator ekle
        l_butce_input = QtWidgets.QLineEdit()
        l_butce_input.setPlaceholderText("0.00")
        validator = QtGui.QDoubleValidator()
        validator.setBottom(0.0)  # Negatif değer girilememesi için
        l_butce_input.setValidator(validator)
        
        butce_input = QtWidgets.QLineEdit()
        butce_input.setPlaceholderText("0.00")
        validator = QtGui.QDoubleValidator()
        validator.setBottom(0.0)
        butce_input.setValidator(validator)
        
        # eşik değer için slider ve ilgili bileşenler
        esik_deger_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        esik_deger_slider.setMinimum(0)  # Minimum değer
        esik_deger_slider.setMaximum(100)  # Maksimum değer
        esik_deger_slider.setValue(20)
        esik_deger_slider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        esik_deger_slider.setTickInterval(10)

        esik_deger_label = QtWidgets.QLabel(f"Aşım Oranı: 20%")

        esik_deger_slider.valueChanged.connect(lambda value: esik_deger_label.setText(f"Aşım Oranı: {value}%"))
        
        # Slider değeri widget'ı
        esik_slider_widget = QtWidgets.QWidget()
        esik_slider_layout = QtWidgets.QVBoxLayout(esik_slider_widget)
        esik_slider_layout.addWidget(esik_deger_label)
        esik_slider_layout.addWidget(esik_deger_slider)
        esik_slider_widget.setLayout(esik_slider_layout)
        
        form_layout.addRow("Birim:", birim_combo)
        form_layout.addRow("Harcama Kalemi:", kalem_combo)
        form_layout.addRow("Limit Bütçe: ", l_butce_input)
        form_layout.addRow("Bütçe: ", butce_input)
        form_layout.addRow("Aşım Eşik Değeri:", esik_slider_widget)
        
        layout.addLayout(form_layout)
        
        # Butonlar
        buttons = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        )
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        
        layout.addWidget(buttons)
        
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            birim_id = birim_combo.currentData()
            kalem_adi = kalem_combo.currentData()
            
            try:
                l_butce_miktari = float(l_butce_input.text() or 0)
                butce_miktari = float(butce_input.text() or 0)
            except ValueError:
                l_butce_miktari = 0
                butce_miktari = 0
            
            if birim_id is None:
                QtWidgets.QMessageBox.warning(None, "Hata", "Lütfen bir birim seçiniz")
                return
                
            if kalem_adi is None:
                QtWidgets.QMessageBox.warning(None, "Hata", "Lütfen bir harcama kalemi seçiniz")
                return
            
            if l_butce_miktari <= 0:
                QtWidgets.QMessageBox.warning(None, "Hata", "Lütfen geçerli bir limit bütçe miktarı giriniz")
                return
            
            if butce_miktari <= 0:
                QtWidgets.QMessageBox.warning(None, "Hata", "Lütfen geçerli bir bütçe miktarı giriniz")
                return
            
            res = db.add_butce(kalem_adi, birim_id, butce_miktari, l_butce_miktari, esik_deger_slider.value())
            
            if res == "basarili":
                QtWidgets.QMessageBox.information(None, "Başarılı", "Bütçe başarıyla eklendi")
                self.load_budget_data()  # Tabloyu yeniler
            elif res == "var":
                QtWidgets.QMessageBox.warning(None, "Kalem Var", "Bu birim için bu kalem limiti zaten ekli.")
            else:
                QtWidgets.QMessageBox.critical(None, "Başarısız", "Bütçe eklenemedi. Kalem bulunamadı veya bir hata oluştu.")
    
    def edit_budget_item(self):
        selected_rows = self.budget_table.selectedItems() #düzenlenmek istenen row seçilmeli önce
    
        if not selected_rows:
            QtWidgets.QMessageBox.warning(None, "Uyarı", "Lütfen düzenlemek için bir bütçe kalemi seçin")
            return
        
        selected_row = selected_rows[0].row()
        
        birim_adi = self.budget_table.item(selected_row,0).text()
        kalem_adi = self.budget_table.item(selected_row, 1).text()
        tahsis_butce = float(self.budget_table.item(selected_row, 2).text().replace(",", "."))
        kullanilan_butce = float(self.budget_table.item(selected_row, 3).text().replace(",", "."))
        limit_butce = float(self.budget_table.item(selected_row, 5).text().replace(",", "."))
        esik_deger = int(self.budget_table.item(selected_row, 6).text().replace(",","."))
        #düzenleme içinn dialog:
        db = Database()
        dialog = QtWidgets.QDialog()
        dialog.setWindowTitle("Bütçe Düzenle")
        dialog.setFixedWidth(800)
        dialog.setStyleSheet("background-color: white;")
        
        layout = QtWidgets.QVBoxLayout(dialog)
        
        # Başlık ve açıklama
        title_label = QtWidgets.QLabel("Bütçe Düzenleme Ekranı")
        title_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #2c3e50; margin-bottom: 10px;")
        layout.addWidget(title_label)
    
        form_layout = QtWidgets.QFormLayout()
        
        # Düzenlenemez alanlar
        birim_label = QtWidgets.QLineEdit()
        birim_label.setText(birim_adi)
        birim_label.setReadOnly(True)
        birim_label.setStyleSheet("background-color: #ecf0f1; color: #7f8c8d;")
        
        try:
            db.cursor.execute("SELECT birimId FROM birim WHERE birimIsmi = ?", (birim_adi,))
            birim_id_result = db.cursor.fetchone()
            if birim_id_result:
                birim_id = birim_id_result[0]
            else:
                QtWidgets.QMessageBox.critical(None, "Hata", "Seçilen birim bulunamadı")
                return
        except Exception as e:
            print(f"Birim ID bulma hatası: {e}")
            QtWidgets.QMessageBox.critical(None, "Hata", f"Birim bilgisi alınamadı: {e}")
            return

        kalem_label = QtWidgets.QLineEdit()
        kalem_label.setText(kalem_adi)
        kalem_label.setReadOnly(True)
        kalem_label.setStyleSheet("background-color: #ecf0f1; color: #7f8c8d;")
        
        # Düzenlenebilir alanlar - sarı arka plan ile belirginleştiriliyor
        l_butce_input = QtWidgets.QLineEdit()
        l_butce_input.setText(str(limit_butce))
        l_butce_input.setStyleSheet("background-color: #fffde7; font-weight: bold;")
        validator = QtGui.QDoubleValidator()
        validator.setBottom(0.0)  # negatif değer girilememesi için
        l_butce_input.setValidator(validator)
        
        tahsis_butce_input = QtWidgets.QLineEdit()
        tahsis_butce_input.setText(str(tahsis_butce))
        tahsis_butce_input.setStyleSheet("background-color: #fffde7; font-weight: bold;")
        validator = QtGui.QDoubleValidator()
        validator.setBottom(0.0)
        tahsis_butce_input.setValidator(validator)
        
        kullanilan_butce_label = QtWidgets.QLineEdit()
        kullanilan_butce_label.setText(str(kullanilan_butce))
        kullanilan_butce_label.setReadOnly(True)
        kullanilan_butce_label.setStyleSheet("background-color: #ecf0f1; color: #7f8c8d;")
        
        # Slider (düzenlenebilir alan)
        esik_deger_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        esik_deger_slider.setMinimum(0)  # Minimum değer
        esik_deger_slider.setMaximum(100)  # Maksimum değer
        esik_deger_slider.setValue(esik_deger)  # Mevcut değeri ayarla
        esik_deger_slider.setTickPosition(QtWidgets.QSlider.TicksBelow)  # İşaretlerin aşağıda olmasını sağla
        esik_deger_slider.setTickInterval(10)  # İşaretlerin her 10 birim aralıkla yerleşmesini sağla
        esik_deger_slider.setStyleSheet("background-color: #fffde7;")

        # Slider değerini gösteren etiket
        esik_deger_label = QtWidgets.QLabel(f"Aşım Oranı: {esik_deger}%")
        esik_deger_label.setStyleSheet("font-weight: bold; color: #2c3e50;")
        esik_deger_slider.valueChanged.connect(lambda value: esik_deger_label.setText(f"Aşım Oranı: {value}%")) #slider değişince etiket güncellenir
        
        # Slider değeri widget'ı
        esik_slider_widget = QtWidgets.QWidget()
        esik_slider_widget.setStyleSheet("background-color: #fffde7; border-radius: 4px; padding: 5px;")
        esik_slider_layout = QtWidgets.QVBoxLayout(esik_slider_widget)
        esik_slider_layout.addWidget(esik_deger_label)
        esik_slider_layout.addWidget(esik_deger_slider)
        esik_slider_widget.setLayout(esik_slider_layout)
        
        # Form düzeni - etiketlerde düzenlenebilir alanlar belirtiliyor
        form_layout.addRow("Birim (Düzenlenemez):", birim_label)
        form_layout.addRow("Harcama Kalemi (Düzenlenemez):", kalem_label)
        form_layout.addRow("Birim Bütçe (Düzenlenebilir):", tahsis_butce_input)
        form_layout.addRow("Kullanılan Bütçe (Düzenlenemez):", kullanilan_butce_label)
        form_layout.addRow("Limit Bütçe (Düzenlenebilir):", l_butce_input)
        form_layout.addRow("Aşım Oranı (Düzenlenebilir):", esik_slider_widget)
        
        layout.addLayout(form_layout)

        #diyalog için butonlar
        buttons = QtWidgets.QDialogButtonBox(
        QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel
        )
        
        # Özel buton isimleri
        buttons.button(QtWidgets.QDialogButtonBox.Ok).setText("Kaydet")
        buttons.button(QtWidgets.QDialogButtonBox.Cancel).setText("İptal")
        
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        
        layout.addWidget(buttons)
        
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            try:
                yeni_l_butce_miktari = float(l_butce_input.text() or 0)
                yeni_butce_miktari = float(tahsis_butce_input.text() or 0)
                yeni_esik_deger = esik_deger_slider.value()
            except ValueError:
                QtWidgets.QMessageBox.warning(None, "Hata", "Geçersiz bütçe değeri")
                return
            
            if yeni_l_butce_miktari <= 0:
                QtWidgets.QMessageBox.warning(None, "Hata", "Lütfen geçerli bir limit bütçe miktarı giriniz")
                return
            
            if yeni_butce_miktari <= 0:
                QtWidgets.QMessageBox.warning(None, "Hata", "Lütfen geçerli bir bütçe miktarı giriniz")
                return
            
            # veritabanı güncelleme
            res = db.edit_limit_butce(kalem_adi, birim_id, yeni_butce_miktari, yeni_l_butce_miktari, yeni_esik_deger)
            
            if res == "basarili":
                QtWidgets.QMessageBox.information(None, "Başarılı", "Bütçe başarıyla güncellendi")
                self.load_budget_data()
            elif res == "basarisiz":
                QtWidgets.QMessageBox.warning(None, "Hata", "Belirtilen harcama kalemi bulunamadı")
            elif res == "kayit_yok":
                QtWidgets.QMessageBox.warning(None, "Hata", "Bu birim ve kalem için bütçe kaydı bulunamadı")
            else:
                QtWidgets.QMessageBox.critical(None, "Başarısız", f"Bütçe güncellenemedi: {res}")
                
    def load_budget_data(self):
        try:
            # Mevcut sütun genişliklerini kaydet
            column_widths = []
            for i in range(self.budget_table.columnCount()):
                column_widths.append(self.budget_table.columnWidth(i))
            
            # Tablodaki satırları temizleyip yeniden doldur
            self.budget_table.setRowCount(0)
            self.populate_budget_table()
            
            for i in range(len(column_widths)):
                if i < self.budget_table.columnCount() and column_widths[i] > 0:
                    self.budget_table.setColumnWidth(i, column_widths[i])
        except Exception as e:
            print(f"Bütçe verilerini yüklerken hata oluştu: {e}")
            QtWidgets.QMessageBox.critical(None, "Hata", f"Bütçe verilerini yüklerken bir sorun oluştu: {e}")

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Yönetici Paneli"))
        
    def delete_budget_item(self):
        db = Database()
        selected_rows = self.budget_table.selectionModel().selectedRows()
        if not selected_rows:
            QtWidgets.QMessageBox.warning(None, "Uyarı", "Lütfen silmek için bir bütçe seçiniz")
            return
        
        row_index = selected_rows[0].row()
        birim_adi = self.budget_table.item(row_index, 0).text()
        kalem_adi = self.budget_table.item(row_index, 1).text()
        limit_butce = float(self.budget_table.item(row_index, 5).text().replace(",", "."))
        
        # onay ekranı:
        reply = QtWidgets.QMessageBox()
        reply.setWindowTitle("Bütçe Silme Onayı")
        reply.setText(f"{birim_adi} biriminin {kalem_adi} kalemini silmek istediğinize emin misiniz?")
        reply.setIcon(QtWidgets.QMessageBox.Question)

        evet_button = reply.addButton("Evet", QtWidgets.QMessageBox.YesRole)
        hayir_button = reply.addButton("Hayır", QtWidgets.QMessageBox.NoRole)
        reply.setDefaultButton(hayir_button)  # default

        reply.exec_()

        if reply.clickedButton() == evet_button:
            db.delete_limit_butce(kalem_adi, birim_adi, limit_butce)
            self.load_budget_data()
            QtWidgets.QMessageBox.information(None, "Başarılı", "Bütçe başarıyla silindi.")
