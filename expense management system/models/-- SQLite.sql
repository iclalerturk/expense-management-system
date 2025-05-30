-- INSERT INTO harcamakalemi(kalemAd, aciklama) VALUES 
-- ('Konaklama','Otel masrafları'),
-- ('Yemek','Yiyecek/içecek temini');

ALTER TABLE harcama ADD COLUMN tazminDurumu TEXT;
UPDATE harcama
SET tazminDurumu = 'Beklemede'

update harcama
set tazminTutari = 0

create table birim_kalem_harcanan_butce (
    id integer primary key autoincrement,
    birim_id integer,
    harcama_kalem_id integer,
    harcanan_butce real,
    FOREIGN KEY (birim_id) REFERENCES birim(id),
    FOREIGN KEY (harcama_kalem_id) REFERENCES harcamakalemi(id)
);

INSERT INTO birim_kalem_harcanan_butce (birim_id, harcama_kalem_id, harcanan_butce) VALUES
(1, 1, 1200.00), -- Satış birimi için Taksi harcaması
(1, 2, 800.00),  -- Satış birimi için Otopark harcaması
(2, 3, 1500.00), -- Pazarlama birimi için Benzin harcaması
(2, 4, 1000.00), -- Pazarlama birimi için Ofis Malzemesi harcaması
(3, 5, 3000.00), -- Ar-Ge birimi için Konaklama harcaması
(3, 6, 2000.00), -- Ar-Ge birimi için Yemek harcaması
(4, 1, 500.00),  -- Muhasebe birimi için Taksi harcaması
(4, 2, 200.00),  -- Muhasebe birimi için Otopark harcaması
(5, 3, 2500.00), -- IT birimi için Benzin harcaması
(5, 4, 1500.00); -- IT birimi için Ofis Malzemesi harcaması


UPDATE birim_kalem_butcesi set limitButce=1000 where birimId = 3 and kalemId = 4;
UPDATE harcama set tutar=400 where harcamaId = 1;
delete from birim_kalem_harcanan_butce where id = 14;
ALTER TABLE birim ADD COLUMN butceAsildi INTEGER DEFAULT 0;

UPDATE harcama set calisanId = 3 where harcamaId = 24;

CREATE TABLE bildirim (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    kullaniciId INTEGER,
    mesaj TEXT,
    okundu INTEGER DEFAULT 0,
    tarih TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (kullaniciId) REFERENCES calisan(calisanId)
);

UPDATE harcama SET tazminDurumu='Beklemede', onayDurumu='Onaylandi' WHERE harcamaId=20;
