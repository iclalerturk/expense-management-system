-- INSERT INTO harcamakalemi(kalemAd, aciklama) VALUES 
-- ('Konaklama','Otel masrafları'),
-- ('Yemek','Yiyecek/içecek temini');

ALTER TABLE harcama ADD COLUMN tazminDurumu TEXT;
UPDATE harcama
SET tazminDurumu = 'Beklemede'

update harcama
set tazminTutari = 0