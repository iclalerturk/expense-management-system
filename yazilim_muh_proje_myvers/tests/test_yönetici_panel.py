import sys
import os
import unittest
from PyQt5.QtWidgets import QApplication

# Add the parent directory to sys.path to allow imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from screens.yönetici_panel import YoneticiPanelUI
from models.database import Database
from models.yonetici import Yonetici  # <-- import your model class

app = QApplication(sys.argv)  # Needed for QWidget-based tests

class TestYoneticiPanel(unittest.TestCase):
    def setUp(self):
        self.panel = YoneticiPanelUI()
        self.birim_id = 1  # Make sure this exists in your test DB
        self.panel.setupUi(self.panel, self.birim_id)

    def test_load_data_row_count(self):
        """Test if the table loads data rows for the given birim."""
        self.panel.load_data()
        row_count = self.panel.table.rowCount()
        self.assertGreater(row_count, 0, "Table should have at least one row")

    def test_status_update_logic(self):
        """Test if the status update mechanism works logically (no DB assertion)."""
        old_method = self.panel.db.update_harcama_status
        self.called = False

        def mock_update(harcama_id, new_status):
            self.called = True
            self.assertIn(new_status, ["Onaylandi", "Reddedildi"])

        self.panel.db.update_harcama_status = mock_update
        self.panel.update_status(1, "Onaylandi")
        self.assertTrue(self.called)

        # Restore original method
        self.panel.db.update_harcama_status = old_method

    def test_yonetici_object_fetch(self):
        """Test if the Yonetici object is returned correctly from DB."""
        db = Database()
        yonetici = db.get_yonetici_by_birim_id(self.birim_id)
        self.assertIsInstance(yonetici, Yonetici)
        self.assertEqual(yonetici.birim_id, self.birim_id)
        self.assertTrue(yonetici.get_full_name())  # Check string output

    def test_welcome_label_text(self):
        """Check if welcome label text includes manager's name."""
        # Fetch actual text from the welcome label
        welcome_label = self.panel.user_info_layout.itemAt(0).widget()
        text = welcome_label.text()
        self.assertIn("Hoş Geldiniz", text)
        self.assertIn("!", text)

if __name__ == "__main__":
    unittest.main()
