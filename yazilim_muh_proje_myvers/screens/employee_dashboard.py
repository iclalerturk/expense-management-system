from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem
from models.database import Database

class EmployeeDashboardUI(object):
    def setupUi(self, Form):
        Form.setObjectName("EmployeeDashboard")
        Form.resize(1100, 700)
        Form.setStyleSheet('''
            QWidget {
                font-family: 'Segoe UI', Arial;
                color: #333;
                background-color: #f0f0f0;
            }
            QLabel {
                font-size: 24px;
                color: #2c3e50;
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
            QTableWidget {
                background-color: white;
                border-radius: 8px;
                border: 1px solid #ddd;
            }
            QTableWidget::item {
                padding: 5px;
            }
            QTableWidget QHeaderView::section {
                background-color: #f5f5f5;
                border: 1px solid #ddd;
                padding: 5px;
                font-weight: bold;
            }
            QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox {
                border: 1px solid #ddd;
                border-radius: 4px;
                padding: 8px;
                background: white;
            }
            QGroupBox {
                border: 1px solid #ddd;
                border-radius: 8px;
                margin-top: 1ex;
                background-color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 5px;
            }
        ''')

        # Ana layout
        self.main_layout = QtWidgets.QHBoxLayout(Form)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # Sol Menü
        self.sidebar_widget = QtWidgets.QWidget()
        self.sidebar_widget.setMaximumWidth(160)
        self.sidebar_widget.setStyleSheet('''
            QWidget {
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
                color: white;
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

        self.sidebar_layout = QtWidgets.QVBoxLayout(self.sidebar_widget)
        self.sidebar_layout.setContentsMargins(0, 0, 0, 0)
        self.sidebar_layout.setSpacing(0)

        # Menü Butonları
        self.btn_new_expense = QtWidgets.QPushButton("Harcama Yap")
        self.btn_new_expense.setCheckable(True)
        self.btn_past_requests = QtWidgets.QPushButton("Geçmiş Harcamalar")
        self.btn_past_requests.setCheckable(True)

        self.sidebar_layout.addWidget(self.btn_new_expense)
        self.sidebar_layout.addWidget(self.btn_past_requests)

        # Spacer ve Çıkış Butonu
        self.sidebar_layout.addStretch()
        self.btn_logout = QtWidgets.QPushButton("Çıkış Yap")
        self.sidebar_layout.addWidget(self.btn_logout)

        # Ana İçerik
        self.content_widget = QtWidgets.QStackedWidget()
        self.content_widget.setStyleSheet('''
            QWidget {
                background-color: #f8f9fa;
            }
        ''')

        # Harcamalar Tabı
        self.new_expenses_page = QtWidgets.QWidget()
        self.expenses_layout = QtWidgets.QVBoxLayout(self.new_expenses_page)
        
        # Başlık
        self.expenses_header = QtWidgets.QWidget()
        self.expenses_header_layout = QtWidgets.QHBoxLayout(self.expenses_header)
        self.expenses_label = QtWidgets.QLabel("Harcama Kalemleri")
        self.expenses_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #2c3e50;")
        self.expenses_header_layout.addWidget(self.expenses_label)
        self.expenses_header_layout.addStretch()
        
        self.expenses_layout.addWidget(self.expenses_header)
        
        # Harcama Kalemleri Tablosu
        self.expense_table = QtWidgets.QTableWidget()
        self.expense_table.setColumnCount(4)
        self.expense_table.setHorizontalHeaderLabels(["Kalem ID", "Kalem Adı", "Departman Bütçesi", "Kalan Bütçe"])
        self.expense_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.expense_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.expense_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.expense_table.setAlternatingRowColors(True)
        
        self.expenses_layout.addWidget(self.expense_table)
        
        # Harcama Talep Formu
        self.expense_form_group = QtWidgets.QGroupBox("Yeni Harcama Talebi Oluştur")
        self.expense_form_group.setStyleSheet("QGroupBox { font-weight: bold; }")
        self.expense_form_layout = QtWidgets.QFormLayout(self.expense_form_group)
        
        # Seçilen kalem etiketi
        self.selected_item_label = QtWidgets.QLabel("Seçilen Kalem: ")
        self.selected_item_value = QtWidgets.QLabel("Lütfen tabloda bir kalem seçiniz")
        self.selected_item_value.setStyleSheet("font-weight: bold; color: #2c3e50;")
        self.selected_item_layout = QtWidgets.QHBoxLayout()
        self.selected_item_layout.addWidget(self.selected_item_label)
        self.selected_item_layout.addWidget(self.selected_item_value)
        self.selected_item_layout.addStretch()
        self.expense_form_layout.addRow(self.selected_item_layout)
        
        # Miktar giriş alanı
        self.amount_label = QtWidgets.QLabel("Harcama Miktarı (TL):")
        self.amount_input = QtWidgets.QDoubleSpinBox()
        self.amount_input.setRange(0, 100000)
        self.amount_input.setDecimals(2)
        self.amount_input.setSingleStep(10)
        self.expense_form_layout.addRow(self.amount_label, self.amount_input)
        
        # Açıklama alanı
        """
        self.description_label = QtWidgets.QLabel("Açıklama:")
        self.description_input = QtWidgets.QTextEdit()
        self.description_input.setMaximumHeight(80)
        self.expense_form_layout.addRow(self.description_label, self.description_input)
        """
        
        # Talep oluştur butonu
        self.submit_button_layout = QtWidgets.QHBoxLayout()
        self.submit_button_layout.addStretch()
        self.submit_button = QtWidgets.QPushButton("Talep Oluştur")
        self.submit_button.setMinimumWidth(150)
        self.submit_button.setStyleSheet('''
            QPushButton {
                background-color: #2ecc71;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
        ''')
        self.submit_button_layout.addWidget(self.submit_button)
        self.expense_form_layout.addRow("", self.submit_button_layout)
        
        self.expenses_layout.addWidget(self.expense_form_group)
        
        # Geçmiş talepler Tabı
        self.past_requests_page = QtWidgets.QWidget()
        self.past_requests_layout = QtWidgets.QVBoxLayout(self.past_requests_page)

        # Başlık
        self.past_requests_header = QtWidgets.QWidget()
        self.past_requests_header_layout = QtWidgets.QHBoxLayout(self.past_requests_header)
        self.past_requests_label = QtWidgets.QLabel("Geçmiş Harcama Talepleri")
        self.past_requests_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #2c3e50;")
        self.past_requests_header_layout.addWidget(self.past_requests_label)
        self.past_requests_header_layout.addStretch()
        
        # Yenile butonu
        self.refresh_button = QtWidgets.QPushButton("Talepleri Yenile")
        self.refresh_button.setStyleSheet('''
            QPushButton {
                background-color: #3498db;
                padding: 8px 15px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        ''')
        self.past_requests_header_layout.addWidget(self.refresh_button)
        
        self.past_requests_layout.addWidget(self.past_requests_header)
        
        # Geçmiş talepler tablosu
        self.past_requests_table = QtWidgets.QTableWidget()
        self.past_requests_table.setColumnCount(5)
        self.past_requests_table.setHorizontalHeaderLabels(["ID", "Harcama Kalemi", "Tutar", "Tarih", "Onay Durumu"])
        self.past_requests_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.past_requests_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.past_requests_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.past_requests_table.setAlternatingRowColors(True)
        
        self.past_requests_layout.addWidget(self.past_requests_table)
        
        # Detay kutusu
        self.request_details_group = QtWidgets.QGroupBox("Seçili Talep Detayları")
        self.request_details_group.setStyleSheet("QGroupBox { font-weight: bold; }")
        self.request_details_layout = QtWidgets.QVBoxLayout(self.request_details_group)
        
        self.request_details_label = QtWidgets.QLabel("Lütfen detaylarını görmek için bir talep seçin")
        self.request_details_label.setAlignment(QtCore.Qt.AlignCenter)
        self.request_details_layout.addWidget(self.request_details_label)
        
        self.past_requests_layout.addWidget(self.request_details_group)

        # Tabları StackedWidget'e Ekle
        self.content_widget.addWidget(self.new_expenses_page)
        self.content_widget.addWidget(self.past_requests_page)

        # Ana Layout'a Ekle
        self.main_layout.addWidget(self.sidebar_widget)
        self.main_layout.addWidget(self.content_widget)

        # Buton Bağlantıları
        self.btn_new_expense.clicked.connect(lambda: self.change_tab(self.new_expenses_page, self.btn_new_expense, self.btn_past_requests))
        self.btn_past_requests.clicked.connect(lambda: self.change_tab(self.past_requests_page, self.btn_past_requests, self.btn_new_expense))
        
        # Tablo seçim bağlantısı
        self.expense_table.itemSelectionChanged.connect(self.on_expense_selected)
        
        # Talep oluşturma buton bağlantısı
        self.submit_button.clicked.connect(self.create_expense_request)
        
        # Varsayılan Seçim
        self.btn_new_expense.setChecked(True)
        self.content_widget.setCurrentWidget(self.new_expenses_page)
        
        # Kullanıcı bilgisi
        
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("EmployeeDashboard", "Çalışan Paneli"))

    def change_tab(self, page, active_btn, other_btn):
        self.content_widget.setCurrentWidget(page)
        active_btn.setChecked(True)
        other_btn.setChecked(False)
        
        # Harcama sayfasına geçildiğinde kalemleri yükle
        if page == self.new_expenses_page and self.current_user:
            self.load_expense_items()
        # Geçmiş talepler sayfasına geçildiğinde talepleri yükle
        elif page == self.past_requests_page and self.current_user:
            self.load_past_expense_requests()
    
    def set_user(self, user_data):
        """Çalışanın bilgilerini ayarlar ve ilişkili verileri yükler"""
        self.current_user = user_data
        if self.current_user:
            self.load_expense_items()
            # Yenileme butonuna bağlantı ekle
            self.refresh_button.clicked.connect(self.load_past_expense_requests)
            # Geçmiş talepler tablosunda seçim değişikliği için bağlantı
            self.past_requests_table.itemSelectionChanged.connect(self.on_past_request_selected)
    
    def load_expense_items(self):
        """Çalışanın birimine ait harcama kalemlerini yükler"""
        if not self.current_user or 'birimId' not in self.current_user:
            return
        
        try:
            db = Database()
            birim_id = self.current_user['birimId']
            
            # Birim-Kalem bütçe bilgilerini al
            budget_data = db.get_unit_and_kalem_budget()
            
            # Tabloyu temizle
            self.expense_table.setRowCount(0)
            
            # Kullanıcının birimindeki bütçeleri filtrele
            row_count = 0
            for item in budget_data:
                if item['Birim Adı'] == self.get_birim_name(birim_id):
                    self.expense_table.insertRow(row_count)
                    
                    # Kalem ID'sini bulmak için veritabanına sorgu yap
                    db.cursor.execute("SELECT kalemId FROM harcamakalemi WHERE kalemAd = ?", 
                                     (item['Kalem Adı'],))
                    kalem_id = db.cursor.fetchone()
                    kalem_id = kalem_id[0] if kalem_id else "-"
                    
                    # Kalem ID sütunu
                    id_item = QTableWidgetItem(str(kalem_id))
                    self.expense_table.setItem(row_count, 0, id_item)
                    
                    # Kalem Adı sütunu
                    name_item = QTableWidgetItem(item['Kalem Adı'])
                    self.expense_table.setItem(row_count, 1, name_item)
                    
                    # Departman Bütçesi sütunu
                    total_budget = item['Tahsis Edilen Bütçe']
                    budget_item = QTableWidgetItem(f"{total_budget:.2f} TL")
                    self.expense_table.setItem(row_count, 2, budget_item)
                    
                    # Kalan Bütçe sütunu
                    remaining_budget = item['Kalan Bütçe']
                    remaining_item = QTableWidgetItem(f"{remaining_budget:.2f} TL")
                    if remaining_budget < 0:
                        remaining_item.setForeground(QtGui.QColor(255, 0, 0))  # Negatif değerler kırmızı
                    self.expense_table.setItem(row_count, 3, remaining_item)
                    
                    row_count += 1
            
            # ID sütununu gizle
            self.expense_table.setColumnHidden(0, True)
            
            # Kullanıcıya bilgilendirme
            if row_count == 0:
                QtWidgets.QMessageBox.information(
                    None, 
                    "Bilgi", 
                    f"Biriminize ait harcama kalemi bulunamadı."
                )
        
        except Exception as e:
            QtWidgets.QMessageBox.critical(
                None, 
                "Hata", 
                f"Harcama kalemleri yüklenirken bir hata oluştu: {str(e)}"
            )
            
    def get_birim_name(self, birim_id):
        """Birim ID'sine göre birim adını döndürür"""
        try:
            db = Database()
            db.cursor.execute("SELECT birimIsmi FROM birim WHERE birimId = ?", (birim_id,))
            result = db.cursor.fetchone()
            return result[0] if result else "Bilinmeyen Birim"
        except Exception as e:
            print(f"Birim adı alınamadı: {str(e)}")
            return "Bilinmeyen Birim"
        
    
    def on_expense_selected(self):
        """Tabloda bir kalem seçildiğinde çalışır"""
        selected_rows = self.expense_table.selectedItems()
        if not selected_rows:
            self.selected_item_value.setText("Lütfen tabloda bir kalem seçiniz")
            return
        
        # Seçilen satırdaki kalem adını al
        row = selected_rows[0].row()
        kalem_id = self.expense_table.item(row, 0).text()
        kalem_adi = self.expense_table.item(row, 1).text()
        kalan_butce_text = self.expense_table.item(row, 3).text()
        kalan_butce = float(kalan_butce_text.replace(" TL", ""))
        
        # Seçilen kalemi göster
        self.selected_item_value.setText(f"{kalem_adi} (ID: {kalem_id})")
        
        # Kalan bütçeye göre miktar sınırı belirle
        self.amount_input.setMaximum(max(0, kalan_butce))
        
        # Eğer kalan bütçe negatifse veya 0'sa uyarı göster
        if kalan_butce <= 0:
            self.amount_input.setEnabled(False)
            self.submit_button.setEnabled(False)
            QtWidgets.QMessageBox.warning(
                None, 
                "Bütçe Uyarısı", 
                f"{kalem_adi} kalemi için kalan bütçe yetersiz! Harcama talebi oluşturamazsınız."
            )
        else:
            self.amount_input.setEnabled(True)
            self.submit_button.setEnabled(True)
    
    def create_expense_request(self):
        """Harcama talebi oluşturma fonksiyonu"""
        if not self.current_user:
            QtWidgets.QMessageBox.warning(None, "Hata", "Kullanıcı bilgisi bulunamadı!")
            return
        
        # Seçilen kalem kontrolü
        selected_rows = self.expense_table.selectedItems()
        if not selected_rows:
            QtWidgets.QMessageBox.warning(None, "Hata", "Lütfen bir harcama kalemi seçiniz!")
            return
        
        row = selected_rows[0].row()
        kalem_id = int(self.expense_table.item(row, 0).text())
        kalem_adi = self.expense_table.item(row, 1).text()
        
        # Miktar kontrolü
        amount = self.amount_input.value()
        if amount <= 0:
            QtWidgets.QMessageBox.warning(None, "Hata", "Lütfen geçerli bir miktar giriniz!")
            return
        
        # Açıklama kontrolü
        """
        description = self.description_input.toPlainText().strip()
        if not description:
            QtWidgets.QMessageBox.warning(None, "Hata", "Lütfen açıklama giriniz!")
            return
        """
        
        # Harcama talebini veritabanına kaydet
        try:
            db = Database()
            calisan_id = self.current_user['calisanId']
            birim_id = self.current_user['birimId']
            
            # Şimdiki tarih
            import datetime
            current_date = datetime.datetime.now().strftime("%Y-%m-%d")
            
            # Harcama tablosuna ekle
            db.cursor.execute(
                """
                INSERT INTO harcama 
                (calisanId, kalemId, birimId, tutar, onayDurumu, tarih) 
                VALUES (?, ?, ?, ?, ?, ?)
                """, 
                (calisan_id, kalem_id, birim_id, amount, "Beklemede", current_date)
            )
            db.conn.commit()
            
            # Başarılı mesajı
            QtWidgets.QMessageBox.information(
                None, 
                "Başarılı", 
                f"Harcama talebiniz başarıyla oluşturuldu!\n\nKalem: {kalem_adi}\nMiktar: {amount:.2f} TL\nDurum: Beklemede"
            )
            
            # Formu sıfırla
            self.amount_input.setValue(0)
            #self.description_input.clear()
            self.expense_table.clearSelection()
            self.selected_item_value.setText("Lütfen tabloda bir kalem seçiniz")
            
            # Tabloyu güncelle
            self.load_expense_items()
            
        except Exception as e:
            QtWidgets.QMessageBox.critical(
                None, 
                "Hata", 
                f"Harcama talebi oluşturulurken bir hata oluştu: {str(e)}"
            )
            
    def load_past_expense_requests(self):
        """Çalışanın geçmiş harcama taleplerini yükler"""
        if not self.current_user or 'calisanId' not in self.current_user:
            return
        
        try:
            db = Database()
            calisan_id = self.current_user['calisanId']
            
            # Harcama taleplerini al
            query = """
            SELECT h.harcamaId, h.kalemId, k.kalemAd, h.tutar, h.tarih, h.onayDurumu
            FROM harcama h
            JOIN harcamakalemi k ON h.kalemId = k.kalemId
            WHERE h.calisanId = ?
            ORDER BY h.tarih DESC
            """
            db.cursor.execute(query, (calisan_id,))
            expense_requests = db.cursor.fetchall()
            
            # Tabloyu temizle
            self.past_requests_table.setRowCount(0)
            
            # Talepleri tabloya ekle
            for row_index, request in enumerate(expense_requests):
                self.past_requests_table.insertRow(row_index)
                
                # Talep ID
                id_item = QTableWidgetItem(str(request[0]))
                self.past_requests_table.setItem(row_index, 0, id_item)
                
                # Kalem Adı
                kalem_item = QTableWidgetItem(request[2])
                self.past_requests_table.setItem(row_index, 1, kalem_item)
                
                # Tutar
                amount_item = QTableWidgetItem(f"{request[3]:.2f} TL")
                self.past_requests_table.setItem(row_index, 2, amount_item)
                
                # Tarih
                date_item = QTableWidgetItem(request[4])
                self.past_requests_table.setItem(row_index, 3, date_item)
                
                # Onay Durumu
                status_item = QTableWidgetItem(request[5])
                
                # Duruma göre renklendirme
                if request[5] == "Onaylandi":
                    status_item.setForeground(QtGui.QColor(46, 204, 113))
                elif request[5] == "Reddedildi":
                    status_item.setForeground(QtGui.QColor(231, 76, 60))
                elif request[5] == "Beklemede":
                    status_item.setForeground(QtGui.QColor(52, 152, 219))
                    
                self.past_requests_table.setItem(row_index, 4, status_item)
            
            # ID sütununu gizle
            self.past_requests_table.setColumnHidden(0, True)
            
            # Kullanıcıya bilgilendirme
            if self.past_requests_table.rowCount() == 0:
                self.request_details_label.setText("Henüz hiç harcama talebiniz bulunmamaktadır.")
        
        except Exception as e:
            QtWidgets.QMessageBox.critical(
                None, 
                "Hata", 
                f"Geçmiş harcama talepleri yüklenirken bir hata oluştu: {str(e)}"
            )
            
    def on_past_request_selected(self):
        """Geçmiş talep tablosunda bir talep seçildiğinde çalışır"""
        selected_rows = self.past_requests_table.selectedItems()
        if not selected_rows:
            self.request_details_label.setText("Lütfen detaylarını görmek için bir talep seçin")
            return
        
        # Seçilen satırdaki bilgileri al
        row = selected_rows[0].row()
        talep_id = self.past_requests_table.item(row, 0).text()
        kalem_adi = self.past_requests_table.item(row, 1).text()
        tutar = self.past_requests_table.item(row, 2).text()
        tarih = self.past_requests_table.item(row, 3).text()
        durum = self.past_requests_table.item(row, 4).text()
        
        # Detay bilgisini HTML formatında hazırla
        detail_html = f"""
        <html>
        <head>
        <style>
            body {{ font-family: 'Segoe UI', Arial; }}
            table {{ width: 100%; border-collapse: collapse; }}
            th, td {{ padding: 8px; text-align: left; border-bottom: 1px solid #ddd; }}
            th {{ background-color: #f2f2f2; }}
        </style>
        </head>
        <body>
        <h3>Harcama Talebi Detayları</h3>
        <table>
            <tr><th>Talep No</th><td>{talep_id}</td></tr>
            <tr><th>Harcama Kalemi</th><td>{kalem_adi}</td></tr>
            <tr><th>Talep Edilen Tutar</th><td>{tutar}</td></tr>
            <tr><th>Talep Tarihi</th><td>{tarih}</td></tr>
            <tr><th>Onay Durumu</th><td>{durum}</td></tr>
        </table>
        </body>
        </html>
        """
        
        # Detay etiketini güncelle
        self.request_details_label.setText(detail_html)