class Yonetici:
    def __init__(self, yonetici_id, isim, soyisim, email, sifre, birim_id):
        self.yonetici_id = yonetici_id
        self.isim = isim
        self.soyisim = soyisim
        self.email = email
        self.sifre = sifre
        self.birim_id = birim_id

    def get_full_name(self):
        return f"{self.isim} {self.soyisim}"

    def __str__(self):
        return f"Yönetici({self.yonetici_id}): {self.get_full_name()} - {self.email}"
