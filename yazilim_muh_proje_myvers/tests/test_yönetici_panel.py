import sys
import os
import unittest
from PyQt5.QtWidgets import QApplication

# Add the parent directory to sys.path to allow imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from screens.yönetici_panel import YoneticiPanelUI
from models.database import Database

app = QApplication(sys.argv)  # Needed for QWidget-based tests

class TestYoneticiPanel(unittest.TestCase):
    def setUp(self):
        self.panel = YoneticiPanelUI()
        self.birim_id = 1  # Use an existing birimId in your test DB
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

if __name__ == "__main__":
    unittest.main()
