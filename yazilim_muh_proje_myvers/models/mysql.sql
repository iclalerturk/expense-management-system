ALTER TABLE harcama ADD COLUMN tazminDurumu TEXT;

INSERT INTO birim_kalem_butcesi (birimId, kalemId, limitButce, asimOrani, maxKisiLimit)
VALUES
(5, 4, 5000, 10, 500),
(5, 2, 4000, 10, 500),
(5, 3, 4000, 10, 500),
(5, 6, 3000, 10, 500);