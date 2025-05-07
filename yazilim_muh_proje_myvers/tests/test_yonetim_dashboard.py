import unittest
import sys
import os
from unittest.mock import MagicMock, patch
from PyQt5.QtWidgets import QApplication, QTableWidgetItem, QWidget
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from screens.dashboard import DashboardUI
from models.database import Database

class TestYonetimDashboard(unittest.TestCase):
    def setUp(self):
        self.app = QApplication.instance() or QApplication(sys.argv)
        self.form = QWidget()
        self.dashboard = DashboardUI()
        self.dashboard.setupUi(self.form)
        self.db_mock = MagicMock()
    
    def tearDown(self):
        self.form = None
        self.dashboard = None
        self.db_mock = None
        
    #* Burada edit_limit_bugdet (eklenen bütçenin güncellenmesi işleminin) doğru çalışıp çalışmadığını kontrol etmek adına başarılı ve başarısız
    #* olarak kod içerisinde belirtilen durumların testi gerçekleştirilmiştir
    
    @patch('models.database.sqlite3.connect')
    def test_edit_limit_butce_success(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        # kalem_id bulundu
        mock_cursor.fetchone.side_effect = [
            (5,),           # SELECT kalemId sonucu
            ('some_data',)  # SELECT * FROM birim_kalem_butcesi sonucu
        ]

        manager = Database("gider_new.db")
        result = manager.edit_limit_butce("Benzin", 1, 10000, 8000, 10)

        self.assertEqual(result, "basarili")
        self.assertTrue(mock_conn.commit.called)
        self.assertTrue(mock_conn.close.called)

    @patch('models.database.sqlite3.connect')
    def test_edit_limit_butce_no_kalem(self, mock_connect):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        mock_cursor.fetchone.return_value = None  #* kalem bulunamadı -> bu durumda basarisiz olarak buluyor mu test edildi

        manager = Database("gider_new.db")
        result = manager.edit_limit_butce("YanlışKalem", 1, 10000, 8000, 10)

        self.assertEqual(result, "basarisiz")

if __name__ == '__main__':
    unittest.main()
        