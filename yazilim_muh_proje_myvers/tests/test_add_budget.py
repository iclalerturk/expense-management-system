import unittest
from unittest.mock import MagicMock, patch
from unittest import mock
from PyQt5.QtWidgets import QApplication, QTableWidget
from PyQt5 import QtWidgets
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from controller.budget_manager import BudgetManager

class TestAddBudget(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication(sys.argv)
    
    def setUp(self):
        self.table_widget = QTableWidget()
        self.budget_manager = BudgetManager(self.table_widget)
        self.budget_manager.budget_table = mock.Mock(spec=QtWidgets.QTableWidget)
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        
        headers = ["Birim Adı", "Kalem Adı", "Toplam Bütçe", "Kullanılan Bütçe", 
                "Kalan Bütçe", "Limit Bütçe", "Aşım Oranı"]
        self.table.setHorizontalHeaderLabels(headers)

        self.budget_manager = BudgetManager(self.table)
        
        self.db_patcher = patch('models.database.Database')
        self.mock_db = self.db_patcher.start()
    
    def tearDown(self):
        self.db_patcher.stop()
    
    @patch('PyQt5.QtWidgets.QDialog.exec_')
    @patch('PyQt5.QtWidgets.QMessageBox.warning')
    @patch('PyQt5.QtWidgets.QMessageBox.information')
    def test_add_budget_item_success(self, mock_info, mock_warning, mock_exec):
        instance = self.mock_db.return_value
        instance.add_butce.return_value = "basarili"

        instance.cursor = MagicMock()
        instance.cursor.fetchall.return_value = [("Taksi",), ("Benzin",)]
        
        mock_exec.return_value = 1
        
        with patch('PyQt5.QtWidgets.QComboBox.currentData', side_effect=["Satış", "Benzin"]), \
            patch('PyQt5.QtWidgets.QLineEdit.text', side_effect=["5000", "10000"]), \
            patch('PyQt5.QtWidgets.QSlider.value', return_value=20), \
            patch.object(self.budget_manager, 'load_budget_data'):
            
            self.budget_manager.add_budget_item()

            instance.add_butce.assert_called_once_with("Benzin", "Satış", 10000.0, 5000.0, 20)

            mock_info.assert_called_once()

            self.budget_manager.load_budget_data.assert_called_once()
    
    @patch('PyQt5.QtWidgets.QDialog.exec_')
    @patch('PyQt5.QtWidgets.QMessageBox.warning')
    def test_add_budget_item_already_exists(self, mock_warning, mock_exec):
        instance = self.mock_db.return_value
        instance.add_butce.return_value = "var"

        instance.cursor = MagicMock()
        instance.cursor.fetchall.return_value = [("Taksi",), ("Benzin",)]

        mock_exec.return_value = 1  # QDialog.Accepted

        with patch('PyQt5.QtWidgets.QComboBox.currentData', side_effect=["Satış", "Benzin"]), \
            patch('PyQt5.QtWidgets.QLineEdit.text', side_effect=["5000", "10000"]), \
            patch('PyQt5.QtWidgets.QSlider.value', return_value=20), \
            patch.object(self.budget_manager, 'load_budget_data'):
            
            self.budget_manager.add_budget_item()
            
            mock_warning.assert_called_once()
            
            self.budget_manager.load_budget_data.assert_not_called()
    
    def test_load_budget_data(self):
        column_widths = [100, 120, 80, 90, 70, 110, 60]
        for i, width in enumerate(column_widths):
            self.table.setColumnWidth(i, width)
        
        with patch.object(self.budget_manager, 'populate_budget_table'):
            self.budget_manager.load_budget_data()
            
            self.budget_manager.populate_budget_table.assert_called_once()
            
            for i, width in enumerate(column_widths):
                self.assertEqual(self.table.columnWidth(i), width)
    
if __name__ == '__main__':
    unittest.main()