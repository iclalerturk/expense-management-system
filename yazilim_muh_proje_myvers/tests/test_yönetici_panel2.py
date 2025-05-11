import sys
import os
import unittest
from PyQt5.QtWidgets import QApplication, QLabel

# Add parent directory to sys.path to allow relative imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from screens.yönetici_panel import YoneticiPanelUI

app = QApplication(sys.argv)  # Required for QWidget-based tests

class TestYoneticiPanelAdvanced(unittest.TestCase):
    def setUp(self):
        self.panel = YoneticiPanelUI()
        self.birim_id = 1  # Ensure this birimId exists in test DB
        self.panel.setupUi(self.panel, self.birim_id)

    def test_column_headers(self):
        """Check if all expected column headers are set correctly."""
        self.panel.load_data()  # Ensure headers are set

        expected_headers = [
            "ID", "Ad Soyad", "Kalem", "Tutar", "Tazmin", "Açıklama", 
            "Durum", "Tarih", "Limit Aşıldı mı", "Şuan Aşım Var mı", "Aşım Miktarı", "İşlem"
        ]

        self.assertEqual(self.panel.table.columnCount(), len(expected_headers), "Column count mismatch")

        for i, expected in enumerate(expected_headers):
            header_item = self.panel.table.horizontalHeaderItem(i)
            self.assertIsNotNone(header_item, f"Header at index {i} is None")
            self.assertEqual(header_item.text(), expected)


    def test_summary_card_value_labels_are_strings(self):
        """Ensure each summary card value is a string (e.g., '0', '5', etc)."""
        self.panel.load_data()

        cards = [self.panel.card_beklemede, self.panel.card_onaylandi, self.panel.card_reddedildi]
        for card in cards:
            # Access the QLabel assigned in `create_summary_card`
            value_label = card.value_label  # Access via dynamic property
            self.assertIsInstance(value_label.text(), str, "Card value is not a string")

if __name__ == "__main__":
    unittest.main()
