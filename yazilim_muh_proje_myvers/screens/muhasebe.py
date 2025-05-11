from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox
from models.database import Database

class MuhasebeDashboardUI(object):
    def setupUi(self, Form):
        Form.setObjectName("AccountingDashboard")
        Form.resize(1300, 800)
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

        # Main layout
        self.main_layout = QtWidgets.QHBoxLayout(Form)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # Left Menu
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

        # Menu Buttons
        self.btn_pending_requests = QtWidgets.QPushButton("Bekleyen Talepler")
        self.btn_pending_requests.setCheckable(True)
        self.btn_all_requests = QtWidgets.QPushButton("Tüm Talepler")
        self.btn_all_requests.setCheckable(True)

        self.sidebar_layout.addWidget(self.btn_pending_requests)
        self.sidebar_layout.addWidget(self.btn_all_requests)

        # Spacer and Logout Button
        self.sidebar_layout.addStretch()
        self.btn_logout = QtWidgets.QPushButton("Çıkış Yap")
        self.sidebar_layout.addWidget(self.btn_logout)

        # Main Content
        self.content_widget = QtWidgets.QStackedWidget()
        self.content_widget.setStyleSheet('''
            QWidget {
                background-color: #f8f9fa;
            }
        ''')

        # ----- PENDING REQUESTS PAGE -----
        self.pending_requests_page = QtWidgets.QWidget()
        self.pending_requests_layout = QtWidgets.QVBoxLayout(self.pending_requests_page)
        
        # Title
        self.pending_header = QtWidgets.QWidget()
        self.pending_header_layout = QtWidgets.QHBoxLayout(self.pending_header)
        self.pending_label = QtWidgets.QLabel("Bekleyen Tazmin Talepleri")
        self.pending_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #2c3e50;")
        self.pending_header_layout.addWidget(self.pending_label)
        self.pending_header_layout.addStretch()
        
        # Refresh button
        self.refresh_pending_button = QtWidgets.QPushButton("Talepleri Yenile")
        self.refresh_pending_button.setStyleSheet('''
            QPushButton {
                background-color: #3498db;
                padding: 8px 15px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        ''')
        self.pending_header_layout.addWidget(self.refresh_pending_button)
        
        self.pending_requests_layout.addWidget(self.pending_header)
        
        # Pending requests table
        self.pending_requests_table = QtWidgets.QTableWidget()
        self.pending_requests_table.setColumnCount(8)
        self.pending_requests_table.setHorizontalHeaderLabels([
            "ID", "Çalışan", "Birim", "Harcama Kalemi", "Tutar", "Tarih", "Durum","Karşılanabilecek\nTutar"
        ])
        self.pending_requests_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.pending_requests_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.pending_requests_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.pending_requests_table.setAlternatingRowColors(True)
        self.load_approved_expenses_to_table()

        self.pending_requests_layout.addWidget(self.pending_requests_table)
        
        # Request details and actions group
        self.request_actions_group = QtWidgets.QGroupBox("Talep İşlemleri")
        self.request_actions_group.setStyleSheet("QGroupBox { font-weight: bold; }")
        self.request_actions_layout = QtWidgets.QHBoxLayout(self.request_actions_group)
        
        # Details panel (left side)
        self.details_panel = QtWidgets.QWidget()
        self.details_layout = QtWidgets.QFormLayout(self.details_panel)
        self.details_layout.setContentsMargins(0, 0, 20, 0)
        
        self.detail_request_id = QtWidgets.QLabel("--")
        self.detail_employee = QtWidgets.QLabel("--")
        self.detail_department = QtWidgets.QLabel("--")
        self.detail_expense_item = QtWidgets.QLabel("--")
        self.detail_amount = QtWidgets.QLabel("--")
        self.detail_budget_remaining = QtWidgets.QLabel("--")
        self.detail_threshold_info = QtWidgets.QLabel("--")
        self.detail_karsilanabilecek_tutar_info = QtWidgets.QLabel("--")
        
        self.details_layout.addRow("Talep ID:", self.detail_request_id)
        self.details_layout.addRow("Çalışan:", self.detail_employee)
        self.details_layout.addRow("Birim:", self.detail_department)
        self.details_layout.addRow("Harcama Kalemi:", self.detail_expense_item)
        self.details_layout.addRow("Talep Tutarı:", self.detail_amount)
        self.details_layout.addRow("Kalan Bütçe:", self.detail_budget_remaining)
        self.details_layout.addRow("Eşik Bilgisi:", self.detail_threshold_info)
        self.details_layout.addRow("Karşılanabilecek\nTutar:", self.detail_karsilanabilecek_tutar_info)
        
        # Actions panel (right side)
        self.actions_panel = QtWidgets.QWidget()
        self.actions_layout = QtWidgets.QVBoxLayout(self.actions_panel)
        
        # Override expense item
        self.kalem_override_group = QtWidgets.QGroupBox("Harcama Kalemi Değiştir")
        self.kalem_override_layout = QtWidgets.QHBoxLayout(self.kalem_override_group)
        self.kalem_combobox = QtWidgets.QComboBox()
        self.kalem_override_layout.addWidget(self.kalem_combobox)
        self.harcama_kalemlerini_getir()
 
        self.apply_kalem_button = QtWidgets.QPushButton("Uygula")
        self.apply_kalem_button.setStyleSheet('''
            QPushButton {
                background-color: #f39c12;
            }
            QPushButton:hover {
                background-color: #e67e22;
            }
        ''')
        self.kalem_override_layout.addWidget(self.apply_kalem_button)
        self.apply_kalem_button.clicked.connect(self.apply_kalem_button_clicked)

        self.actions_layout.addWidget(self.kalem_override_group)

        # Reimburse amount
        self.reimburse_group = QtWidgets.QGroupBox("Tazmin Miktarı")
        self.reimburse_layout = QtWidgets.QVBoxLayout(self.reimburse_group)
        
        self.reimburse_full_radio = QtWidgets.QRadioButton("Tam Tutarı Tazmin Et")
        self.reimburse_full_radio.setChecked(True)
        
        self.reimburse_partial_radio = QtWidgets.QRadioButton("Kısmi Tazmin")
        self.reimburse_amount = QtWidgets.QDoubleSpinBox()
        self.reimburse_amount.setRange(0, 100000)
        self.reimburse_amount.setDecimals(2)
        self.reimburse_amount.setSingleStep(10)
        self.reimburse_amount.setEnabled(False)
        
        self.reimburse_layout.addWidget(self.reimburse_full_radio)
        self.reimburse_layout.addWidget(self.reimburse_partial_radio)
        self.reimburse_layout.addWidget(self.reimburse_amount)
        
        self.actions_layout.addWidget(self.reimburse_group)
        
        # # Notes field
        # self.notes_group = QtWidgets.QGroupBox("Notlar")
        # self.notes_layout = QtWidgets.QVBoxLayout(self.notes_group)
        
        # self.notes_edit = QtWidgets.QTextEdit()
        # self.notes_layout.addWidget(self.notes_edit)
        
        # self.actions_layout.addWidget(self.notes_group)
        
        # Action buttons
        self.buttons_layout = QtWidgets.QHBoxLayout()
        
        self.approve_button = QtWidgets.QPushButton("Tazmin Et")
        self.approve_button.setStyleSheet('''
            QPushButton {
                background-color: #2ecc71;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
        ''')
        self.approve_button.clicked.connect(self.on_approve_button_clicked)
        self.reject_button = QtWidgets.QPushButton("Reddet")
        self.reject_button.setStyleSheet('''
            QPushButton {
                background-color: #e74c3c;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        ''')
        
        self.buttons_layout.addWidget(self.approve_button)
        self.buttons_layout.addWidget(self.reject_button)
        self.reject_button.clicked.connect(self.on_reject_button_clicked)
        self.actions_layout.addLayout(self.buttons_layout)
        
        self.request_actions_layout.addWidget(self.details_panel, 1)
        self.request_actions_layout.addWidget(self.actions_panel, 1)
        self.pending_requests_table.cellClicked.connect(self.on_table_row_clicked)

        self.pending_requests_layout.addWidget(self.request_actions_group)

        # ----- Tüm İsteklerin Listelendiği Sayfa -----
        self.all_requests_page = QtWidgets.QWidget()
        self.all_requests_layout = QtWidgets.QVBoxLayout(self.all_requests_page)
        
        self.all_requests_header = QtWidgets.QWidget()
        self.all_requests_header_layout = QtWidgets.QHBoxLayout(self.all_requests_header)
        self.all_requests_label = QtWidgets.QLabel("Tüm Harcama Talepleri")
        self.all_requests_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #2c3e50;")
        self.all_requests_header_layout.addWidget(self.all_requests_label)
        self.all_requests_header_layout.addStretch()
        #yenile butonu:
        self.refresh_all_button = QtWidgets.QPushButton("Talepleri Yenile")
        self.refresh_all_button.setStyleSheet('''
            QPushButton {
                background-color: #3498db;
                padding: 8px 15px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        ''')
        
        self.export_button = QtWidgets.QPushButton("Dışa Aktar")
        self.export_button.setStyleSheet('''
            QPushButton {
                background-color: #27ae60;
                padding: 8px 15px;
            }
            QPushButton:hover {
                background-color: #2ecc71;
            }
        ''')
        
        self.all_requests_header_layout.addWidget(self.refresh_all_button)
        self.all_requests_header_layout.addWidget(self.export_button)
        
        self.all_requests_layout.addWidget(self.all_requests_header)
        
        self.status_filter = QtWidgets.QComboBox()
        self.status_filter.addItem("Tüm Durumlar")
        self.status_filter.addItem("Onaylandı")
        self.status_filter.addItem("Reddedildi")
        self.status_filter.addItem("Beklemede")
        
        self.date_from = QtWidgets.QDateEdit(QtCore.QDate.currentDate().addMonths(-1))
        self.date_from.setCalendarPopup(True)
        
        self.date_to = QtWidgets.QDateEdit(QtCore.QDate.currentDate())
        self.date_to.setCalendarPopup(True)
        
        # All requests table
        self.all_requests_table = QtWidgets.QTableWidget()
        self.all_requests_table.setColumnCount(8)
        self.all_requests_table.setHorizontalHeaderLabels([
            "ID", "Çalışan", "Birim", "Harcama Kalemi", "Tutar", "Tarih", "İşlem Tarihi", "Durum"
        ])
        self.all_requests_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.all_requests_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.all_requests_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.all_requests_table.setAlternatingRowColors(True)
        
        self.all_requests_layout.addWidget(self.all_requests_table)
        
        # Detail view
        self.all_request_details = QtWidgets.QGroupBox("Talep Detayları")
        self.all_request_details.setMaximumHeight(150)
        self.all_request_details_layout = QtWidgets.QVBoxLayout(self.all_request_details)
        
        self.all_request_detail_label = QtWidgets.QLabel("Detayları görmek için talep seçin")
        self.all_request_detail_label.setAlignment(QtCore.Qt.AlignCenter)
        self.all_request_details_layout.addWidget(self.all_request_detail_label)
        
        self.all_requests_layout.addWidget(self.all_request_details)

        self.content_widget.addWidget(self.pending_requests_page)
        self.content_widget.addWidget(self.all_requests_page)

        self.main_layout.addWidget(self.sidebar_widget)
        self.main_layout.addWidget(self.content_widget)

        self.btn_pending_requests.clicked.connect(lambda: self.change_tab(
            self.pending_requests_page, self.btn_pending_requests, 
            [self.btn_all_requests]
        ))
        self.btn_all_requests.clicked.connect(lambda: self.change_tab(
            self.all_requests_page, self.btn_all_requests,
            [self.btn_pending_requests]
        ))
        
        self.btn_pending_requests.setChecked(True)
        self.content_widget.setCurrentWidget(self.pending_requests_page)
        
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)


  

    def on_table_row_clicked(self):
        db = Database()
        selected_row = self.pending_requests_table.currentRow()
        if selected_row < 0:
            return

        harcama_id = int(self.pending_requests_table.item(selected_row, 0).text())
        detaylar = db.get_expense_details_by_id_muhasebe(harcama_id)

        if detaylar:
            self.detail_request_id.setText(str(detaylar[0]))
            self.detail_employee.setText(detaylar[1])
            self.detail_department.setText(detaylar[2])
            self.detail_expense_item.setText(detaylar[3])
            self.detail_amount.setText(f"{detaylar[4]:.2f} ₺")
            self.detail_budget_remaining.setText(f"{detaylar[5]:.2f} ₺")
            self.detail_threshold_info.setText(detaylar[6])
            self.detail_karsilanabilecek_tutar_info.setText(f"{detaylar[7]:.2f} ₺")
            self.kalem_combobox.setCurrentText(detaylar[3])

            # Tazmin kontrolü
            talep_tutar = detaylar[4]
            karsilanabilecek_tutar = detaylar[7]
            esik_orani_str = detaylar[6].split("Aşım Oranı: ")[-1].replace("%", "")
            try:
                esik_orani = float(esik_orani_str)
            except:
                esik_orani = 0

            esik_miktar = (esik_orani / 100) * karsilanabilecek_tutar
            maksimum_tutar = karsilanabilecek_tutar + esik_miktar

            if talep_tutar > maksimum_tutar:
                # Tam tazmin mümkün değil
                self.reimburse_full_radio.setEnabled(False)
                self.reimburse_partial_radio.setChecked(True)
                self.reimburse_amount.setEnabled(True)
                self.reimburse_amount.setMaximum(maksimum_tutar)
                self.reimburse_amount.setValue(maksimum_tutar)
            else:
                self.reimburse_full_radio.setEnabled(True)
                self.reimburse_full_radio.setChecked(True)
                self.reimburse_partial_radio.setChecked(False)
                self.reimburse_amount.setEnabled(False)
                self.reimburse_amount.setValue(talep_tutar)


    def harcama_kalemlerini_getir(self):
        db = Database()
        kalem_listesi = db.get_harcama_kalemleri_items()
        self.kalem_combobox.clear()
        self.kalem_combobox.addItems(kalem_listesi)

    def load_approved_expenses_to_table(self):
        db = Database()
        expenses = db.get_approved_expenses()
        self.pending_requests_table.setRowCount(len(expenses))

        for row_index, row_data in enumerate(expenses):
            for col_index, col_data in enumerate(row_data):
                item = QtWidgets.QTableWidgetItem(str(col_data))
                self.pending_requests_table.setItem(row_index, col_index, item)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("AccountingDashboard", "Muhasebe Paneli"))
    
    def set_user(self, user_data):
        self.current_user = user_data
    
    def change_tab(self, page, active_btn, other_btns):
        self.content_widget.setCurrentWidget(page)
        active_btn.setChecked(True)
        for btn in other_btns:
            btn.setChecked(False)
        """
        if page == self.pending_requests_page:
            self.load_pending_requests()
        elif page == self.all_requests_page:
            self.load_all_requests()
        """

    def apply_kalem_button_clicked(self):
        selected_row = self.pending_requests_table.currentRow()
        if selected_row < 0:
            return

        harcama_id_item = self.pending_requests_table.item(selected_row, 0)
        if not harcama_id_item:
            return

        harcama_id = int(harcama_id_item.text())
        yeni_kalem_ad = self.kalem_combobox.currentText()

        db = Database()
        # Kalem adına göre kalem ID'si al
        db.cursor.execute("SELECT rowid FROM harcamakalemi WHERE kalemAd = ?", (yeni_kalem_ad,))
        result = db.cursor.fetchone()
        if not result:
            return
        yeni_kalem_id = result[0]

        # Veritabanında güncelle
        db.cursor.execute("UPDATE harcama SET kalemId = ? WHERE harcamaId = ?", (yeni_kalem_id, harcama_id))
        db.conn.commit()

        # Detayları güncelle
        detaylar = db.get_expense_details_by_id_muhasebe(harcama_id)
        if detaylar:
            self.detail_request_id.setText(str(detaylar[0]))
            self.detail_employee.setText(detaylar[1])
            self.detail_department.setText(detaylar[2])
            self.detail_expense_item.setText(detaylar[3])
            self.detail_amount.setText(f"{detaylar[4]:.2f} ₺")
            self.detail_budget_remaining.setText(f"{detaylar[5]:.2f} ₺")
            self.detail_threshold_info.setText(detaylar[6])
            self.detail_karsilanabilecek_tutar_info.setText(f"{detaylar[7]:.2f} ₺")
            self.kalem_combobox.setCurrentText(detaylar[3])

        # Tabloları güncelle
        self.load_approved_expenses_to_table()

    def on_approve_button_clicked(self):
        selected_row = self.pending_requests_table.currentRow()
        if selected_row < 0:
            return

        harcama_id = int(self.pending_requests_table.item(selected_row, 0).text())

        if self.reimburse_full_radio.isChecked():
            tazmin_miktar = float(self.detail_amount.text().replace("₺", "").strip())
        else:
            tazmin_miktar = self.reimburse_amount.value()

        db = Database()

        # Harcama bilgilerini al
        db.cursor.execute("SELECT birimId, kalemId FROM harcama WHERE harcamaId = ?", (harcama_id,))
        result = db.cursor.fetchone()
        if not result:
            return
        birim_id, kalem_id = result

        # Birimin toplam bütçesini ve aşım flag'ini al
        db.cursor.execute("SELECT limitButce FROM birim_kalem_butcesi WHERE birimId = ?", (birim_id,))
        total_butce = db.cursor.fetchone()[0] or 0
        db.cursor.execute("SELECT butceAsildi FROM birim WHERE birimId = ?", (birim_id,))
        butce_asildi_row = db.cursor.fetchone()
        butce_asildi = butce_asildi_row[0] if butce_asildi_row else 0


        # Mevcut toplam harcamayı hesapla
        db.cursor.execute("""
            SELECT SUM(harcanan_butce) FROM birim_kalem_harcanan_butce
            WHERE birim_id = ?
        """, (birim_id,))
        toplam_harcanan = db.cursor.fetchone()[0] or 0

        # Aşım kontrolü
        if toplam_harcanan + tazmin_miktar > total_butce:
            if butce_asildi:
                QtWidgets.QMessageBox.warning(None, "Bütçe Aşıldı", "Bütçe zaten aşıldı. Bu harcama onaylanamaz.")
                db.cursor.execute("""
                    UPDATE harcama 
                    SET onayDurumu = 'Reddedildi', tazminDurumu = 'Reddedildi'
                    WHERE harcamaId = ?
                """, (harcama_id,))
            else:
                QtWidgets.QMessageBox.warning(None, "Bütçe Aşıldı", "Daha sonra bu kalem için yeni harcama talebi yapılamaz.")
                # İlk defa aşıldıysa flag'i set et
                db.cursor.execute("UPDATE birim SET butceAsildi = 1 WHERE birimId = ?", (birim_id,))
                
                # Kalem adını al
                db.cursor.execute("SELECT kalemAd FROM harcamakalemi WHERE kalemId = ?", (kalem_id,))
                kalem_adi_row = db.cursor.fetchone()
                kalem_adi = kalem_adi_row[0] if kalem_adi_row else f"#{kalem_id}"

                # Bildirim gönder
                db.cursor.execute("SELECT calisanId FROM calisan WHERE birimId = ?", (birim_id,))
                kullanicilar = db.cursor.fetchall()

                for (kullanici_id,) in kullanicilar:
                    mesaj = f"'{kalem_adi}' kaleminin bütçesi aşıldı. Bu kalemden yeni tazmin talebi yapılamaz."
                    db.cursor.execute("""
                        INSERT INTO bildirim (kullaniciId, mesaj)
                        VALUES (?, ?)
                    """, (kullanici_id, mesaj))

        else:
            # Harcamayı onayla
            db.cursor.execute("""
                UPDATE harcama 
                SET onayDurumu = 'Onaylandi', tazminDurumu = 'Onaylandi', tazminTutari = ? 
                WHERE harcamaId = ?
            """, (tazmin_miktar, harcama_id))

            # birim_kalem_harcanan_butce tablosunu güncelle
            db.cursor.execute("""
                SELECT id, harcanan_butce FROM birim_kalem_harcanan_butce
                WHERE birim_id = ? AND harcama_kalem_id = ?
            """, (birim_id, kalem_id))
            row = db.cursor.fetchone()

            if row:
                existing_id, mevcut_butce = row
                yeni_butce = mevcut_butce + tazmin_miktar
                db.cursor.execute("""
                    UPDATE birim_kalem_harcanan_butce SET harcanan_butce = ?
                    WHERE id = ?
                """, (yeni_butce, existing_id))
            else:
                db.cursor.execute("""
                    INSERT INTO birim_kalem_harcanan_butce (birim_id, harcama_kalem_id, harcanan_butce)
                    VALUES (?, ?, ?)
                """, (birim_id, kalem_id, tazmin_miktar))
            QtWidgets.QMessageBox.information(None, "Onaylandi", f"{tazmin_miktar:.2f} ₺ tutarındaki harcama onaylandı.")
        db.conn.commit()
        self.load_approved_expenses_to_table()


    def on_reject_button_clicked(self):
        selected_row = self.pending_requests_table.currentRow()
        if selected_row < 0:
            QtWidgets.QMessageBox.warning(None, "Uyarı", "Lütfen reddetmek için bir satır seçin.")
            return

        cevap = QtWidgets.QMessageBox.question(
            None, "Onay", "Seçilen harcama tamamen silinecek. Emin misiniz?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        )

        if cevap == QtWidgets.QMessageBox.No:
            return

        # Harcama ID'sini al
        harcama_id = int(self.pending_requests_table.item(selected_row, 0).text())

        # # Veritabanını güncelle
        db = Database()
        db.reject_expense_request(harcama_id)

        # Bildirim göster
        QtWidgets.QMessageBox.information(None, "Reddedildi", "Harcama talebi başarıyla reddedildi.")

        # Tabloları güncelle
        self.load_approved_expenses_to_table()
