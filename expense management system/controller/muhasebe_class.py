from models.database import Database
from PyQt5 import QtWidgets

class Muhasebe:

    def __init__(self, pending_requests_table, reimburse_full_radio, reimburse_amount, load_approved_expenses_to_table, user_data=None, parent=None):
        self.pending_requests_table = pending_requests_table
        self.reimburse_full_radio = reimburse_full_radio
        self.reimburse_amount = reimburse_amount
        self.load_approved_expenses_to_table = load_approved_expenses_to_table
        self.current_user = user_data
        self.parent = parent  # Arayüz sınıfına referans
        self.db = Database()
    
    def on_approve_button_clicked(self):
        selected_row = self.pending_requests_table.currentRow()
        if selected_row < 0:
            QtWidgets.QMessageBox.warning(None, "Uyarı", "Lütfen onaylamak için bir satır seçin.")
            return

        harcama_id = int(self.pending_requests_table.item(selected_row, 0).text())

        # Arayüzden detail_amount'a eriş
        if self.reimburse_full_radio.isChecked():
            try:
                tazmin_miktar = float(self.parent.detail_amount.text().replace("₺", "").strip())
            except (AttributeError, ValueError):
                QtWidgets.QMessageBox.warning(None, "Hata", "Geçerli bir harcama tutarı bulunamadı.")
                return
        else:
            tazmin_miktar = self.reimburse_amount.value()

        # Use the class database instance instead of creating a new one
        db = self.db

        # Harcama bilgilerini al
        db.cursor.execute("SELECT birimId, kalemId FROM harcama WHERE harcamaId = ?", (harcama_id,))
        result = db.cursor.fetchone()
        if not result:
            QtWidgets.QMessageBox.warning(None, "Hata", "Harcama bilgileri bulunamadı.")
            return
        birim_id, kalem_id = result

        # Birimin toplam bütçesini ve aşım flag'ini al
        db.cursor.execute("SELECT totalButce FROM birim WHERE birimId = ?", (birim_id,))
        result = db.cursor.fetchone()
        if not result:
            QtWidgets.QMessageBox.warning(None, "Hata", "Birim bütçe bilgileri bulunamadı.")
            return
        total_butce = result[0] or 0 
        
        db.cursor.execute("SELECT butceAsildi FROM birim WHERE birimId = ?", (birim_id,))
        butce_asildi_row = db.cursor.fetchone()
        butce_asildi = butce_asildi_row[0] if butce_asildi_row else 0

        # Mevcut toplam harcamayı hesapla
        db.cursor.execute("SELECT SUM(harcanan_butce) FROM birim_kalem_harcanan_butce WHERE birim_id = ?", (birim_id,))
        toplam_harcanan_row = db.cursor.fetchone()
        toplam_harcanan = toplam_harcanan_row[0] or 0


        # Aşım kontrolü
        if toplam_harcanan + tazmin_miktar > total_butce:
            if butce_asildi:
                QtWidgets.QMessageBox.warning(None, "Bütçe Aşıldı", "Bütçe zaten aşıldı. Bu harcama onaylanamaz.")
                db.cursor.execute("UPDATE harcama SET onayDurumu = 'Reddedildi', tazminDurumu = 'Reddedildi' WHERE harcamaId = ?", (harcama_id,))
            else:
                QtWidgets.QMessageBox.warning(None, "Bütçe Aşıldı", "Daha sonra bu kalem için yeni harcama talebi yapılamaz.")
                # İlk defa aşıldıysa flag'i set et
                db.cursor.execute("UPDATE birim SET butceAsildi = 1 WHERE birimId = ?", (birim_id,))
                
                # Kalem adını al
                db.cursor.execute("SELECT kalemAd FROM harcamakalemi WHERE kalemId = ?", (kalem_id,))
                kalem_adi_row = db.cursor.fetchone()
                kalem_adi = kalem_adi_row[0] if kalem_adi_row else f"#{kalem_id}"
                # Harcamayı onayla
                db.cursor.execute("UPDATE harcama SET onayDurumu = 'Onaylandi', tazminDurumu = 'Onaylandi', tazminTutari = ? WHERE harcamaId = ?", (tazmin_miktar, harcama_id))
                # birim_kalem_harcanan_butce tablosunu güncelle
                db.cursor.execute("SELECT id, harcanan_butce FROM birim_kalem_harcanan_butce WHERE birim_id = ? AND harcama_kalem_id = ?", (birim_id, kalem_id))
                row = db.cursor.fetchone()
                if row:
                    existing_id, mevcut_butce = row
                    yeni_butce = mevcut_butce + tazmin_miktar
                    db.cursor.execute("UPDATE birim_kalem_harcanan_butce SET harcanan_butce = ? WHERE id = ?", (yeni_butce, existing_id))
                else:
                    db.cursor.execute("INSERT INTO birim_kalem_harcanan_butce (birim_id, harcama_kalem_id, harcanan_butce) VALUES (?, ?, ?) ", (birim_id, kalem_id, tazmin_miktar))
                # Bildirim gönder
                db.cursor.execute("SELECT calisanId FROM calisan WHERE birimId = ?", (birim_id,))
                kullanicilar = db.cursor.fetchall()

                for (kullanici_id,) in kullanicilar:
                    mesaj = f"'{kalem_adi}' kaleminin bütçesi aşıldı. Bu kalemden yeni tazmin talebi yapılamaz."
                    db.cursor.execute("INSERT INTO bildirim (kullaniciId, mesaj) VALUES (?, ?)", (kullanici_id, mesaj))

        else:
            # Harcamayı onayla
            db.cursor.execute(" UPDATE harcama SET onayDurumu = 'Onaylandi', tazminDurumu = 'Onaylandi', tazminTutari = ? WHERE harcamaId = ?", (tazmin_miktar, harcama_id))

            # birim_kalem_harcanan_butce tablosunu güncelle
            db.cursor.execute("SELECT id, harcanan_butce FROM birim_kalem_harcanan_butce WHERE birim_id = ? AND harcama_kalem_id = ?", (birim_id, kalem_id))
            row = db.cursor.fetchone()

            if row:
                existing_id, mevcut_butce = row
                yeni_butce = mevcut_butce + tazmin_miktar
                db.cursor.execute("UPDATE birim_kalem_harcanan_butce SET harcanan_butce = ? WHERE id = ?", (yeni_butce, existing_id))
            else:
                db.cursor.execute("INSERT INTO birim_kalem_harcanan_butce (birim_id, harcama_kalem_id, harcanan_butce) VALUES (?, ?, ?) ", (birim_id, kalem_id, tazmin_miktar))
            QtWidgets.QMessageBox.information(None, "Onaylandi", f"{tazmin_miktar:.2f} ₺ tutarındaki harcama onaylandı.")
        
        db.conn.commit()
        # Call the method correctly without parameters since we're using the reference to the function
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

        # Use the class database instance
        self.db.reject_expense_request(harcama_id)

        # Bildirim göster+
        QtWidgets.QMessageBox.information(None, "Reddedildi", "Harcama talebi başarıyla reddedildi.")

        # Tabloları güncelle
        self.load_approved_expenses_to_table()

    def get_approved_expenses(self):
        query = "SELECT h.harcamaId, c.email, b.birimIsmi, k.kalemAd, h.tutar, h.tarih, h.onayDurumu FROM harcama h JOIN calisan c ON h.calisanId = c.calisanId JOIN birim b ON h.birimId = b.birimId JOIN harcamakalemi k ON h.kalemId = k.kalemId WHERE h.onayDurumu = 'Onaylandi'"

        self.db.cursor.execute(query)
        return self.db.cursor.fetchall()