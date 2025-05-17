import unittest
from unittest.mock import MagicMock, patch
from PyQt5 import QtWidgets
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from controller.muhasebe_class import Muhasebe

class TestMuhasebe(unittest.TestCase):

    @patch("controller.muhasebe_class.QtWidgets.QMessageBox")
    def test_on_approve_button_budget_already_exceeded(self, mock_messagebox):
        mock_table = MagicMock()
        mock_table.currentRow.return_value = 0
        mock_table.item.return_value.text.return_value = "1"  # harcama_id

        mock_radio = MagicMock()
        mock_radio.isChecked.return_value = True  # Full reimbursement seçili

        mock_detail_amount = MagicMock()
        mock_detail_amount.text.return_value = "150.0 ₺"  # tazmin miktarı

        mock_parent = MagicMock()
        mock_parent.detail_amount = mock_detail_amount

        mock_reimburse_amount = MagicMock()

        load_func = MagicMock()

        mock_db = MagicMock()
        mock_db.cursor.fetchone.side_effect = [
            (10, 20),      # birimId, kalemId
            (100.0,),      # limitButce
            (1,),          # butceAsildi = 1
            (90.0,)        # toplam_harcanan
        ]
        mock_db.cursor.fetchall.return_value = [(99,)]  # kullanıcı listesi

        with patch("controller.muhasebe_class.Database", return_value=mock_db):
            muhasebe = Muhasebe(mock_table, mock_radio, mock_reimburse_amount, load_func, user_data=None, parent=mock_parent)
            muhasebe.on_approve_button_clicked()

        mock_messagebox.warning.assert_called_with(None, "Bütçe Aşıldı", "Bütçe zaten aşıldı. Bu harcama onaylanamaz.")

        mock_db.cursor.execute.assert_any_call(
            "UPDATE harcama SET onayDurumu = 'Reddedildi', tazminDurumu = 'Reddedildi' WHERE harcamaId = ?", (1,)
        )
        mock_db.conn.commit.assert_called()
        load_func.assert_called()
    
    @patch('controller.muhasebe_class.Database')
    def test_on_approve_button_budget_exceeded_first_time(self, MockDatabase):
        mock_db = MockDatabase.return_value
        mock_db.conn = MagicMock() 
        mock_cursor = mock_db.cursor
        mock_cursor.fetchone.side_effect = [
            (1, 2),        # harcama: birimId, kalemId
            (100.0,),      # limitButce
            (0,),          # butceAsildi
            (90.0,),       # toplam harcanan
            ('Kalem A',),  # kalem adı
            (5, 100.0)     # birim_kalem_harcanan_butce: id, mevcut_butce
        ]
        mock_cursor.fetchall.return_value = [(10,), (11,)]  # kullanıcılar      
        mock_table = MagicMock()
        mock_table.currentRow.return_value = 0
        mock_table.item.return_value.text.return_value = "1"  # harcamaId
        mock_radio = MagicMock()
        mock_radio.isChecked.return_value = False
        mock_spinbox = MagicMock()
        mock_spinbox.value.return_value = 20.0  # yeni talep edilen miktar
        mock_parent = MagicMock()
        mock_parent.detail_amount.text.return_value = "₺20"
        with patch.object(QtWidgets.QMessageBox, 'warning') as mock_warning:
            muhasebe = Muhasebe(
                pending_requests_table=mock_table,
                reimburse_full_radio=mock_radio,
                reimburse_amount=mock_spinbox,
                load_approved_expenses_to_table=lambda: None,
                user_data=None,
                parent=mock_parent
            )
            muhasebe.on_approve_button_clicked()

        mock_cursor.execute.assert_any_call(
            "UPDATE birim SET butceAsildi = 1 WHERE birimId = ?", (1,)
        )
        bildirim_calls = [
            c for c in mock_cursor.execute.call_args_list
            if "INSERT INTO bildirim" in c.args[0]
        ]
        assert len(bildirim_calls) == 2
        mock_cursor.execute.assert_any_call(
            "UPDATE harcama SET onayDurumu = 'Onaylandi', tazminDurumu = 'Onaylandi', tazminTutari = ? WHERE harcamaId = ?",
            (20.0, 1)
        )
        expected_new_amount = 100.0 + 20.0
        mock_cursor.execute.assert_any_call(
            "UPDATE birim_kalem_harcanan_butce SET harcanan_butce = ? WHERE id = ?",
            (expected_new_amount, 5)
        )
        mock_db.conn.commit.assert_called_once() 
        mock_warning.assert_called_once()


    def test_get_approved_expenses(self):
        mock_db = MagicMock()
        # Geri döndürülecek örnek veri
        expected_result = [
            (1, "email@example.com", "Birim A", "Kalem X", 100.0, "2025-05-17", "Onaylandi"),
            (2, "email2@example.com", "Birim B", "Kalem Y", 200.0, "2025-05-16", "Onaylandi")
        ]
        mock_db.cursor.fetchall.return_value = expected_result

        muhasebe = Muhasebe.__new__(Muhasebe)  # Yapıcıyı çağırmadan örnek oluştur
        muhasebe.db = mock_db

        result = muhasebe.get_approved_expenses()

        # Sorgu doğru çalıştı mı kontrolü
        mock_db.cursor.execute.assert_called_once()
        self.assertEqual(result, expected_result)



if __name__ == '__main__':
    unittest.main()
