import sqlite3
import os
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from collections import defaultdict
class Database:
    def __init__(self, db_path=None):
        if db_path is None:
            db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gider.db')
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()


    def grafik_verisi_getir(self, kategori, secilen_id=None):
        query_map = {
            'birim': """
                SELECT b.birimIsmi AS ad, strftime('%Y', h.tarih) AS yil, SUM(h.tutar) AS toplam
                FROM harcama h
                JOIN birim b ON h.birimId = b.birimId
                {where}
                GROUP BY b.birimIsmi, yil
            """,
            'kalem': """
                SELECT k.kalemAd AS ad, strftime('%Y', h.tarih) AS yil, SUM(h.tutar) AS toplam
                FROM harcama h
                JOIN harcamakalemi k ON h.kalemId = k.kalemId
                {where}
                GROUP BY k.kalemAd, yil
            """,
            'kisi': """
                SELECT c.isim || ' ' || c.soyisim AS ad, strftime('%Y', h.tarih) AS yil, SUM(h.tutar) AS toplam
                FROM harcama h
                JOIN calisan c ON h.calisanId = c.calisanId
                {where}
                GROUP BY c.isim || ' ' || c.soyisim, yil
            """
        }

        if kategori not in query_map:
            raise ValueError(f"Geçersiz kategori: {kategori}")

        # ID'ye göre WHERE filtreleme ekle
        if secilen_id:
            if kategori == 'birim':
                where_clause = f"WHERE h.birimId = ?"
            elif kategori == 'kalem':
                where_clause = f"WHERE h.kalemId = ?"
            elif kategori == 'kisi':
                where_clause = f"WHERE h.calisanId = ?"
        else:
            where_clause = ""

        query = query_map[kategori].format(where=where_clause)

        if secilen_id:
            self.cursor.execute(query, (secilen_id,))
        else:
            self.cursor.execute(query)

        veri = self.cursor.fetchall()

        data = defaultdict(lambda: defaultdict(float))
        for row in veri:
            ad = row["ad"]
            yil = row["yil"]
            toplam = row["toplam"]
            data[ad][yil] += toplam

        print("debug kontrol:\n")
        print("Veri:", data)
        return data


    def authUser(self, email, sifre):
        try:
            user_tables = [
                ("calisan", "calisanId", "calisan"),
                ("yonetici", "yoneticiId", "yonetici"),
                ("ustyonetici", "ustYoneticiId", "ustyonetici"),
                ("muhasebe", "muhasebeId", "muhasebe")
            ]
            
            for table_name, id_field, user_type in user_tables:
                query = f"SELECT * FROM {table_name} WHERE email = ? AND sifre = ?"
                self.cursor.execute(query, (email, sifre))
                user = self.cursor.fetchone()
                if user:
                    user_dict = dict(user)
                    user_dict["user_type"] = user_type
                    self.conn.commit()
                    return user_dict

            return None
        except Exception as e:
            print(f"Giriş hatası: {e}")
            return None

    def get_all_calisanlar(self):
        query = """
        SELECT calisan.calisanId, calisan.isim, calisan.soyisim, birim.birimIsmi, calisan.email
        FROM calisan
        LEFT JOIN birim ON calisan.birimId = birim.birimId
        """
        self.cursor.execute(query)
        rows = self.cursor.fetchall()
        return rows

    def get_total_employees(self):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM calisan")
        total_employees = cursor.fetchone()[0]
        connection.close()
        return total_employees

    def get_total_butce(self):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute("SELECT SUM(totalButce) FROM birim")
        total_butce = cursor.fetchone()[0]
        connection.close()
        return total_butce
    
    def get_used_butce(self): #totalde -> birim başına değil -> birim başına da hesaplanacak
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute("SELECT SUM(tutar) FROM harcama")
        used_butce = cursor.fetchone()[0]
        connection.close()
        return used_butce
    
    def get_birimler(self):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute("SELECT birimId, birimIsmi FROM birim")
        birimler = cursor.fetchall()
        connection.close()
        return birimler
    
    def get_kalemler(self):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute("SELECT kalemId, kalemAd FROM harcamakalemi")
        kalemler = cursor.fetchall()
        connection.close()
        return kalemler
    
    def get_unit_expenses_by_category(self, unit_id):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        try:
            query = """
            SELECT hk.kalemAd, SUM(h.tutar) as total_amount
            FROM harcama h
            JOIN harcamakalemi hk ON h.kalemId = hk.kalemId
            WHERE h.birimId = ? AND h.onayDurumu = 'Onaylandi'
            GROUP BY h.kalemId
            """
            cursor.execute(query, (unit_id,))
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error fetching unit expenses: {e}")
            return []
    
    def get_category_expenses_by_unit(self, category_id):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        try:
            query = """
            SELECT b.birimIsmi, SUM(h.tutar) as total_amount
            FROM harcama h
            JOIN birim b ON h.birimId = b.birimId
            WHERE h.kalemId = ? AND h.onayDurumu = 'Onaylandi'
            GROUP BY h.birimId
            """
            cursor.execute(query, (category_id,))
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error fetching category expenses: {e}")
            return []
    
    def get_unit_and_kalem_budget(self):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute("""
        SELECT 
            b.birimIsmi,
            k.kalemAd,
            bkb.limitButce AS limitButce,
            b.totalButce AS tahsisEdilenButce,
            bkb.asimOrani AS asimOrani,
            COALESCE(
            (SELECT SUM(h.tutar) 
            FROM harcama h 
            WHERE h.birimId = bkb.birimId 
            AND h.kalemId = bkb.kalemId 
            AND h.onayDurumu = 'Onaylandi'), 0) AS kullanilanButce
            FROM 
                birim_kalem_butcesi bkb
            JOIN 
                birim b ON b.birimId = bkb.birimId
            JOIN 
                harcamakalemi k ON k.kalemId = bkb.kalemId
            ORDER BY 
                b.birimIsmi, k.kalemAd
        """)
        
        rows = cursor.fetchall()
        result = []
        for row in rows:
            birim_adi = row[0]
            kalem_adi = row[1]
            limit_butce = row[2] if row[2] else 0
            tahsis_edilen_butce = row[3] if row[3] else 0
            esik_deger = row[4] if row[4] else 0
            kullanilan_butce = row[5] if row[5] is not None else 0
            kalan_butce = tahsis_edilen_butce - kullanilan_butce
            
            result.append({
                'Birim Adı': birim_adi,
                'Kalem Adı': kalem_adi,
                'Limit Bütçe': limit_butce,
                'Tahsis Edilen Bütçe': tahsis_edilen_butce,
                'Kullanılan Bütçe': kullanilan_butce,
                'Kalan Bütçe': kalan_butce,
                'Aşım Oranı': esik_deger
            })

        connection.close()
        return result

    def add_butce(self, kalem_adi, birim_id, butce_miktari, l_butce_miktari, esik_deger):
            connection = sqlite3.connect(self.db_path)
            cursor = connection.cursor()
            cursor.execute("SELECT kalemId FROM harcamakalemi WHERE kalemAd = ?", (kalem_adi,))
            kalem_id = cursor.fetchone()

            if kalem_id:
                kalem_id = kalem_id[0]
                
                # limit bütçeyi eklemek için sorgu
                cursor.execute(
                    "SELECT * FROM birim_kalem_butcesi WHERE birimId = ? AND kalemId = ?", 
                    (birim_id, kalem_id)
                )
                existing_record = cursor.fetchone()
                
                if existing_record:
                    return "var"  # Bu kalem için zaten limit bütçe var.

                # yeni limit bütçeyi ekleme:
                cursor.execute(
                    "INSERT INTO birim_kalem_butcesi (birimId, kalemId, limitButce, asimOrani) VALUES (?, ?, ?, ?)",
                    (birim_id, kalem_id, l_butce_miktari, esik_deger)
                )
                # yeni bütçeyi ekleme:
                cursor.execute(
                    "INSERT INTO butce (birimId, kalemId, butceMiktari) VALUES (?, ?, ?)",
                    (birim_id, kalem_id, butce_miktari)
                )            
                connection.commit()
                return "basarili"
            else:
                return "basarisiz"  # kalem bulunamadı
            
    def edit_limit_butce(self, kalem_adi, birim_id, birim_butce, l_butce_miktari, esik_deger_miktari): #bütçe miktarını düzenlemek yöneticinin görevi, üst yönetim sadece limit bütçeyi düzenleyebiliyor
        try:
            connection = sqlite3.connect(self.db_path)
            cursor = connection.cursor()

            cursor.execute("SELECT kalemId FROM harcamakalemi WHERE kalemAd = ?", (kalem_adi,))
            kalem_result = cursor.fetchone()
            
            if not kalem_result:
                return "basarisiz"  # kalem bulunamadı
                
            kalem_id = kalem_result[0]
            
            cursor.execute(
                "SELECT * FROM birim_kalem_butcesi WHERE birimId = ? AND kalemId = ?", 
                (birim_id, kalem_id)
            )
            existing_rec = cursor.fetchone()
            
            if not existing_rec:
                return "kayit_yok"
            
            cursor.execute(
                "UPDATE birim_kalem_butcesi SET limitButce = ?, asimOrani = ? WHERE birimId = ? AND kalemId = ?",
                (l_butce_miktari, esik_deger_miktari, birim_id, kalem_id)
            )
            
            cursor.execute(
                "UPDATE butce SET butceMiktari = ? WHERE birimId = ? AND kalemId = ?",
                (birim_butce, birim_id, kalem_id)
            )
            
            connection.commit()
            return "basarili"
        except Exception as e:
            print(f"Düzenleme hatası: {e}")
            return f"hata: {str(e)}"
        finally:
            if connection:
                connection.close()
    
    def delete_limit_butce(self, kalem_adi, birim_adi, l_butce_miktari):
        try:
            connection = sqlite3.connect(self.db_path)
            cursor = connection.cursor()

            cursor.execute("SELECT kalemId FROM harcamakalemi WHERE kalemAd = ?", (kalem_adi,))
            kalem_result = cursor.fetchone()
            
            if not kalem_result:
                return "basarisiz"  # kalem bulunamadı
                
            kalem_id = kalem_result[0]
            
            cursor.execute("SELECT birimId FROM birim WHERE birimIsmi = ?", (birim_adi,))
            birim_result = cursor.fetchone()
            
            if not birim_result:
                return "birim_bulunamadi"
            birim_id = birim_result[0]
            
            cursor.execute(
                "SELECT * FROM birim_kalem_butcesi WHERE birimId = ? AND kalemId = ?", 
                (birim_id, kalem_id)
            )
            existing_rec = cursor.fetchone()
            
            if not existing_rec:
                return "kayit_yok"
            
            cursor.execute(
                "DELETE FROM birim_kalem_butcesi WHERE limitButce = ? AND birimId = ? AND kalemId = ?",
                (l_butce_miktari, birim_id, kalem_id)
            )
            
            if cursor.rowcount > 0:
                connection.commit()
                return "basarili"
            else:
                return "silme_islemi_yapilmadi"  # eşleşen kayıt bulunamadı
                
        except Exception as e:
            print(f"Düzenleme hatası: {e}")
            return f"hata: {str(e)}"
        finally:
            if connection:
                connection.close()