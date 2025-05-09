
import sys
import os
import unittest
from PyQt5.QtWidgets import QApplication, QLabel

# Add parent directory to sys.path to allow relative imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from screens.yönetici_panel import YoneticiPanelUI
from models.database import Database

app = QApplication(sys.argv)  # Required for QWidget tests

class TestYoneticiPanelAdvanced(unittest.TestCase):
    def setUp(self):
        self.panel = YoneticiPanelUI()
        self.birim_id = 1  # Assume test data for birimId=1 exists
        self.panel.setupUi(self.panel, self.birim_id)

    def test_column_headers(self):
        """Check if all expected column headers are set correctly."""
        expected_headers = [
            "ID", "Ad Soyad", "Kalem", "Tutar", "Tazmin", "Açıklama", "Durum", "Tarih",
            "Limit Aşıldı mı", "Şuan Aşım Var mı", "Aşım Miktarı"
        ]
        for i, expected in enumerate(expected_headers):
            actual = self.panel.table.horizontalHeaderItem(i).text()
            self.assertEqual(actual, expected)

    def test_summary_card_values_are_strings(self):
        """Ensure dashboard cards display string values."""
        self.panel.load_data()
        for card in [self.panel.card_beklemede, self.panel.card_onaylandi, self.panel.card_reddedildi]:
            value_label = card.findChild(QLabel)
            self.assertIsInstance(value_label.text(), str)

if __name__ == "__main__":
    unittest.main()
