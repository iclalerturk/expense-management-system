from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QTableWidgetItem
from models.database import Database

class BudgetManager:
    def __init__(self, budget_table_widget):
        self.budget_table = budget_table_widget
    
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
    
    def add_budget_item(self):
        from models.database import Database
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
