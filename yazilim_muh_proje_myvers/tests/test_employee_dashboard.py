import unittest
import sys
import os
from unittest.mock import MagicMock, patch
from PyQt5.QtWidgets import QApplication, QTableWidgetItem, QWidget
from PyQt5.QtTest import QTest
from PyQt5.QtCore import Qt
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from screens.employee_dashboard import EmployeeDashboardUI

class TestEmployeeDashboard(unittest.TestCase):

    def setUp(self):
        self.app = QApplication.instance() or QApplication(sys.argv)
        self.form = QWidget()
        self.dashboard = EmployeeDashboardUI()
        self.dashboard.setupUi(self.form)
        self.db_mock = MagicMock()
        
    def tearDown(self):
        self.form = None
        self.dashboard = None
        self.db_mock = None

    @patch('screens.employee_dashboard.Database')
    def test_user_setting(self, MockDatabase):
        mock_db = MagicMock()
        MockDatabase.return_value = mock_db
        test_user = {
            'calisanId': -1,
            'isim': 'Test',
            'soyisim': 'Kullanici',
            'birimId': 2,
            'email': 'test@firma.com'
        }
        
        mock_db.get_unit_and_kalem_budget.return_value = []
        
        with patch.object(self.dashboard, 'get_birim_name', return_value="Test Birim"):
            self.dashboard.set_user(test_user)
        
        self.assertEqual(self.dashboard.current_user, test_user)
        self.assertTrue(hasattr(self.dashboard, 'refresh_button'))
        self.assertTrue(hasattr(self.dashboard, 'past_requests_table'))
        mock_db.get_unit_and_kalem_budget.assert_called_once()
    @patch('screens.employee_dashboard.Database')
    @patch('screens.employee_dashboard.QtWidgets.QMessageBox')

    def test_load_past_expense_requests(self, MockMessageBox, MockDatabase):
        """Geçmiş harcama taleplerini yükleme metodu doğru çalışıyor mu test et."""
        mock_db = MagicMock()
        MockDatabase.return_value = mock_db
        self.dashboard.current_user = {
            'calisanId': -1,
            'isim': 'Test',
            'soyisim': 'Kullanici',
            'birimId': 2,
            'email': 'test@firma.com'
        }
        self.dashboard.past_requests_table.setRowCount = MagicMock()
        self.dashboard.past_requests_table.insertRow = MagicMock()
        self.dashboard.past_requests_table.setItem = MagicMock()
        self.dashboard.past_requests_table.setColumnHidden = MagicMock()
        self.dashboard.past_requests_table.rowCount = MagicMock(return_value=2)
        self.dashboard.request_details_label.setText = MagicMock()
        mock_cursor = MagicMock()
        mock_db.cursor.execute.return_value = mock_cursor
        mock_db.cursor.fetchall.return_value = [
            (1, 1, "Taksi", 150.00, "2025-04-20", "Onaylandi"),
            (2, 2, "Otopark", 50.00, "2025-04-21", "Beklemede")
        ]
        self.dashboard.load_past_expense_requests()
        mock_db.cursor.execute.assert_called_once()
        sql_query = mock_db.cursor.execute.call_args[0][0]
        self.assertTrue("SELECT" in sql_query)
        self.assertTrue("FROM harcama h" in sql_query)
        self.assertTrue("WHERE h.calisanId = ?" in sql_query)
        mock_db.cursor.fetchall.assert_called_once()
        self.dashboard.past_requests_table.setRowCount.assert_called_once_with(0)


if __name__ == '__main__':
    unittest.main()