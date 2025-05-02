# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) #debug için
from models.database import Database

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
        self.budget_table.setColumnCount(6)
        self.budget_table.setHorizontalHeaderLabels(["Birim Adı", "Kalem Adı", "Toplam Bütçe", "Kullanılan", "Kalan","Limit Bütçe"])
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
        #self.btn_edit_budget.clicked.connect(self.edit_budget_item)  # Sonra tanımlayacağız

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
        #self.btn_delete_budget.clicked.connect(self.delete_budget_item)  # Sonra tanımlayacağız

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
        
        # içerikleri ana içerik layouta ekle
        self.content_layout.addWidget(self.top_bar)
        self.content_layout.addWidget(self.content_page)
        
        # ana widgetları main layouta ekle
        self.main_layout.addWidget(self.sidebar_widget)
        self.main_layout.addWidget(self.content_widget)
        
        self.btn_home.setChecked(True)
        
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
    
    #arayüzde kullanılan metodlar:
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
            # get_unit_and_kalem_budget'den gelen yeni anahtar isimlerini kullan
            toplam_butce = row['Toplam Bütçe'] if 'Toplam Bütçe' in row else row['Tahsis Edilen Bütçe']
            kullanilan_butce = row['Kullanılan Bütçe']
            
            # QTableWidgetItem'leri oluştur
            limit_butce_item = QTableWidgetItem(f"{limit_butce:.2f}")
            toplam_butce_item = QTableWidgetItem(f"{toplam_butce:.2f}")
            kullanilan_item = QTableWidgetItem(f"{kullanilan_butce:.2f}")
            kalan_item = QTableWidgetItem(f"{(toplam_butce - kullanilan_butce):.2f}")

            self.budget_table.setItem(row_index, 0, birim_adi)
            self.budget_table.setItem(row_index, 1, kalem_adi)
            self.budget_table.setItem(row_index, 2, toplam_butce_item)
            self.budget_table.setItem(row_index, 3, kullanilan_item)
            self.budget_table.setItem(row_index, 4, kalan_item)
            self.budget_table.setItem(row_index, 5, limit_butce_item)
            
    def add_budget_item(self):
        """
        Yeni bütçe eklemek için bir dialog gösterir ve bütçeyi veritabanına ekler
        """
        db = Database()
        dialog = QtWidgets.QDialog()
        dialog.setWindowTitle("Yeni Bütçe Ekle")
        dialog.setFixedWidth(400)
        dialog.setStyleSheet("background-color: white;")
        
        layout = QtWidgets.QVBoxLayout(dialog)
        
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
        # Sadece sayı ve nokta girişine izin ver
        validator = QtGui.QDoubleValidator()
        validator.setBottom(0.0)  # Negatif değer girilememesi için
        l_butce_input.setValidator(validator)
        
        butce_input = QtWidgets.QLineEdit()
        butce_input.setPlaceholderText("0.00")
        # Sadece sayı ve nokta girişine izin ver
        validator = QtGui.QDoubleValidator()
        validator.setBottom(0.0)  # Negatif değer girilememesi için
        butce_input.setValidator(validator)
        
        form_layout.addRow("Birim:", birim_combo)
        form_layout.addRow("Harcama Kalemi:", kalem_combo)
        form_layout.addRow("Limit Bütçe: ", l_butce_input)
        form_layout.addRow("Birim Bütçe: ", butce_input)
        
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
                butce_miktari = float(butce_input.text() or 0)
                l_butce_miktari = float(l_butce_input.text() or 0)
            except ValueError:
                butce_miktari = 0
            
            if birim_id is None:
                QtWidgets.QMessageBox.warning(None, "Hata", "Lütfen bir birim seçiniz")
                return
                
            if kalem_adi is None:
                QtWidgets.QMessageBox.warning(None, "Hata", "Lütfen bir harcama kalemi seçiniz")
                return
                
            if butce_miktari <= 0:
                QtWidgets.QMessageBox.warning(None, "Hata", "Lütfen geçerli bir bütçe miktarı giriniz")
                return
            
            if l_butce_miktari <= 0:
                QtWidgets.QMessageBox.warning(None, "Hata", "Lütfen geçerli bir limit bütçe miktarı giriniz")
                return
            
            res = db.add_butce(kalem_adi, birim_id, butce_miktari)
            
            if res == "basarili":
                QtWidgets.QMessageBox.information(None, "Başarılı", "Bütçe başarıyla eklendi")
                self.load_budget_data()  # Tabloyu yenile (bu metodu da düzenlemeniz gerekebilir)
            elif res == "var":
                QtWidgets.QMessageBox.warning(None, "Kalem Var", "Bu birim için bu kalem limiti zaten ekli.")
            else:
                QtWidgets.QMessageBox.critical(None, "Başarısız", "Bütçe eklenemedi. Kalem bulunamadı veya bir hata oluştu.")
    
    def load_budget_data(self):
        try:
            self.budget_table.setRowCount(0)
            self.populate_budget_table()
            self.budget_table.resizeColumnsToContents()
            self.update_budget_summary()
        except Exception as e:
            print(f"Bütçe verilerini yüklerken hata oluştu: {e}")
            QtWidgets.QMessageBox.critical(None, "Hata", f"Bütçe verilerini yüklerken bir sorun oluştu: {e}")
    
    def update_budget_summary(self):
        db = Database()
        data = db.get_unit_and_kalem_budget()
        
        toplam_tahsis = sum(row['Tahsis Edilen Bütçe'] for row in data)
        toplam_kullanilan = sum(row['Kullanılan Bütçe'] for row in data)
        toplam_kalan = toplam_tahsis - toplam_kullanilan
        
        self.lbl_total_budget.setText(f"{toplam_tahsis:.2f} TL")
        self.lbl_used_budget.setText(f"{toplam_kullanilan:.2f} TL")
        self.lbl_remaining_budget.setText(f"{toplam_kalan:.2f} TL")
        
        if toplam_kalan < 0:
            self.lbl_remaining_budget.setStyleSheet("font-size: 18px; font-weight: bold; color: #D8000C;")
        elif toplam_kalan < 0.1 * toplam_tahsis:
            self.lbl_remaining_budget.setStyleSheet("font-size: 18px; font-weight: bold; color: #9F6000;")
        else:
            self.lbl_remaining_budget.setStyleSheet("font-size: 18px; font-weight: bold; color: #4F8A10;")
    
    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Yönetici Paneli"))
        
    def delete_budget_item(self):
            selected_rows = self.budget_table.selectionModel().selectedRows()
            if not selected_rows:
                QtWidgets.QMessageBox.warning(None, "Uyarı", "Lütfen silmek için bir bütçe seçiniz")
                return
                
            # Seçilen satırdan bilgileri al
            row_index = selected_rows[0].row()
            birim_adi = self.budget_table.item(row_index, 0).text()
            kalem_adi = self.budget_table.item(row_index, 1).text()
            
            # Onay iste
            reply = QtWidgets.QMessageBox.question(
                self, 
                "Bütçe Silme Onayı", 
                f"{birim_adi} biriminin {kalem_adi} kalemini silmek istediğinize emin misiniz?",
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, 
                QtWidgets.QMessageBox.No
            )
            
            if reply == QtWidgets.QMessageBox.Yes:
                # TODO: Veritabanından bütçeyi sil
                # butce_id = ...
                # self.db.delete_butce(butce_id)
                
                # Tabloyu güncelle
                self.load_budget_data()
                QtWidgets.QMessageBox.information(self, "Başarılı", "Bütçe başarıyla silindi.")

# Uygulamayı çalıştırmak için ->sonrasında silinecek bu
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = DashboardUI()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())