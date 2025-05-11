from PyQt5 import QtWidgets
from models.database import Database
from controller.expense_pdf import ExpensePdfGenerator
import datetime

class Employee:

    def __init__(self, user_data=None):

        self.current_user = user_data
        self.db = Database()
    
    def set_user_data(self, user_data):

        self.current_user = user_data
    
    def get_user_data(self):

        return self.current_user
    
    def get_birim_name(self, birim_id):

        try:
            self.db.cursor.execute("SELECT birimIsmi FROM birim WHERE birimId = ?", (birim_id,))
            result = self.db.cursor.fetchone()
            return result[0] if result else "Bilinmeyen Birim"
        except Exception as e:
            print(f"Birim adı alınamadı: {str(e)}")
            return "Bilinmeyen Birim"
    
    def get_expense_items(self):

        if not self.current_user or 'birimId' not in self.current_user:
            return None
        
        try:
            birim_id = self.current_user['birimId']
            birim_name = self.get_birim_name(birim_id)
            
            budget_data = self.db.get_unit_and_kalem_budget()
            
            department_budget_data = []
            for item in budget_data:
                if item['Birim Adı'] == birim_name:
                    # Get kalem ID
                    self.db.cursor.execute("SELECT kalemId FROM harcamakalemi WHERE kalemAd = ?", 
                                (item['Kalem Adı'],))
                    kalem_id = self.db.cursor.fetchone()
                    
                    # Add kalem ID to the item
                    item_with_id = item.copy()
                    item_with_id['kalemId'] = kalem_id[0] if kalem_id else None
                    
                    department_budget_data.append(item_with_id)
            
            return department_budget_data
        except Exception as e:
            print(f"Harcama kalemleri yüklenirken hata: {str(e)}")
            return None
    
    def create_expense_request(self, kalem_id, amount):

        if not self.current_user:
            return {'status': 'error', 'message': 'Kullanıcı bilgisi bulunamadı!'}
        
        if amount <= 0:
            return {'status': 'error', 'message': 'Lütfen geçerli bir miktar giriniz!'}
        
        try:
            calisan_id = self.current_user['calisanId']
            birim_id = self.current_user['birimId']
            
            current_date = datetime.datetime.now().strftime("%Y-%m-%d")
            
            self.db.cursor.execute(
                """
                INSERT INTO harcama 
                (calisanId, kalemId, birimId, tutar, onayDurumu, tarih) 
                VALUES (?, ?, ?, ?, ?, ?)
                """, 
                (calisan_id, kalem_id, birim_id, amount, "Beklemede", current_date)
            )
            self.db.conn.commit()
            
            self.db.cursor.execute("SELECT kalemAd FROM harcamakalemi WHERE kalemId = ?", (kalem_id,))
            kalem_result = self.db.cursor.fetchone()
            kalem_adi = kalem_result[0] if kalem_result else 'Bilinmeyen Kalem'
            
            return {
                'status': 'success', 
                'message': f"Harcama talebiniz başarıyla oluşturuldu!\n\nKalem: {kalem_adi}\nMiktar: {amount:.2f} TL\nDurum: Beklemede"
            }
            
        except Exception as e:
            return {'status': 'error', 'message': f"Harcama talebi oluşturulurken bir hata oluştu: {str(e)}"}
    
    def get_past_expense_requests(self):

        if not self.current_user or 'calisanId' not in self.current_user:
            return None
        
        try:
            calisan_id = self.current_user['calisanId']
            
            # Get expense requests
            query = """
            SELECT h.harcamaId, h.kalemId, k.kalemAd, h.tutar, h.tarih, h.onayDurumu
            FROM harcama h
            JOIN harcamakalemi k ON h.kalemId = k.kalemId
            WHERE h.calisanId = ?
            ORDER BY h.tarih DESC
            """
            self.db.cursor.execute(query, (calisan_id,))
            expense_requests = self.db.cursor.fetchall()
            
            return expense_requests
        except Exception as e:
            print(f"Geçmiş harcama talepleri yüklenirken hata: {str(e)}")
            return None
    
    def get_expense_request_detail(self, request_id):

        try:
            query = """
            SELECT 
                h.harcamaId,
                k.kalemAd,
                h.tutar,
                h.tarih,
                h.onayDurumu
            FROM harcama h
            JOIN harcamakalemi k ON h.kalemId = k.kalemId
            WHERE h.harcamaId = ?
            """
            self.db.cursor.execute(query, (request_id,))
            result = self.db.cursor.fetchone()
            
            if result:
                return {
                    'harcamaId': result[0],
                    'kalemAd': result[1],
                    'tutar': result[2],
                    'tarih': result[3],
                    'onayDurumu': result[4]
                }
            return None
        except Exception as e:
            print(f"Harcama detayı alınırken hata: {str(e)}")
            return None

    def get_approved_expense_detail(self, request_id):
        """Get detailed information about an approved expense with reimbursement amount"""
        try:
            query = """
            SELECT 
                h.harcamaId,
                k.kalemAd,
                h.tutar,
                h.tarih,
                h.onayDurumu,
                IFNULL(h.tazminTutari, 0) as tazminTutari,
                c.isim,
                c.soyisim
            FROM harcama h
            JOIN harcamakalemi k ON h.kalemId = k.kalemId
            JOIN calisan c ON h.calisanId = c.calisanId
            WHERE h.harcamaId = ? AND h.onayDurumu = 'Onaylandi'
            """
            self.db.cursor.execute(query, (request_id,))
            result = self.db.cursor.fetchone()
            
            if result:
                return {
                    'harcamaId': result[0],
                    'kalemAd': result[1],
                    'tutar': result[2],
                    'tarih': result[3],
                    'onayDurumu': result[4],
                    'tazminTutari': result[5],
                    'isim': result[6],
                    'soyisim': result[7]
                }
            return None
        except Exception as e:
            print(f"Onaylı harcama detayı alınırken hata: {str(e)}")
            return None
            
    def generate_expense_pdf(self, expense_id):
        
        expense_data = self.get_approved_expense_detail(expense_id)
        if not expense_data:
            return {'status': 'error', 'message': 'Onaylanmış harcama bulunamadı veya tazmin işlemi yapılmamış.'}
            
        pdf_generator = ExpensePdfGenerator()
        try:
            pdf_path = pdf_generator.generate_expense_pdf(expense_data, self.current_user)
            if pdf_path:
                self.db.cursor.execute(
                    "UPDATE harcama SET belgeYolu = ? WHERE harcamaId = ?", 
                    (pdf_path, expense_id)
                )
                self.db.conn.commit()
                return {'status': 'success', 'message': f'PDF başarıyla oluşturuldu: {pdf_path}', 'path': pdf_path}
            else:
                return {'status': 'error', 'message': 'PDF oluşturulamadı.'}
        except Exception as e:
            return {'status': 'error', 'message': f'PDF oluşturulurken hata: {str(e)}'}
