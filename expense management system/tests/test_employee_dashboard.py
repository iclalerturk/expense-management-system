import unittest
from unittest.mock import MagicMock, patch, mock_open
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from controller.employee import Employee
import datetime

class TestEmployeeDashboard(unittest.TestCase):
    
    def setUp(self):
        """Set up test environment before each test method."""
        self.mock_user_data = {
            'calisanId': 1,
            'birimId': 2,
            'isim': 'Test',
            'soyisim': 'User',
            'email': 'test@example.com'
        }
        
        # Create an Employee instance with mock user data
        self.employee = Employee(self.mock_user_data)
        
    @patch('controller.employee.Database')
    def test_create_expense_request_success(self, mock_db_class):
        """Test creating a valid expense request."""
        # Mock database operations
        mock_db_instance = MagicMock()
        mock_db_class.return_value = mock_db_instance
        self.employee.db = mock_db_instance
        
        # Mock the current date for consistency
        current_date = "2025-05-25"
        with patch('datetime.datetime') as mock_date:
            mock_date.now.return_value.strftime.return_value = current_date
            
            # Mock database cursor and connection
            mock_cursor = MagicMock()
            mock_db_instance.cursor = mock_cursor
            mock_db_instance.conn = MagicMock()
            
            # Set up mock return values
            mock_cursor.fetchone.return_value = ("Test Kalem",)
            
            # Call the method to test
            result = self.employee.create_expense_request(kalem_id=5, amount=1000)
            
            # Verify the result
            self.assertEqual(result['status'], 'success')
            self.assertIn('Harcama talebiniz başarıyla oluşturuldu', result['message'])
            self.assertIn('Test Kalem', result['message'])
            self.assertIn('1000.00 TL', result['message'])
            
            # Verify database calls
            mock_cursor.execute.assert_any_call(
                """
                INSERT INTO harcama 
                (calisanId, kalemId, birimId, tutar, onayDurumu, tarih) 
                VALUES (?, ?, ?, ?, ?, ?)
                """, 
                (1, 5, 2, 1000, "Beklemede", current_date)
            )
            mock_db_instance.conn.commit.assert_called_once()
    
    @patch('controller.employee.Database')
    def test_create_expense_request_invalid_amount(self, mock_db_class):
        """Test creating an expense request with an invalid amount."""
        # Set up the employee with mock db
        mock_db_instance = MagicMock()
        mock_db_class.return_value = mock_db_instance
        self.employee.db = mock_db_instance
        
        # Test with zero amount (invalid)
        result = self.employee.create_expense_request(kalem_id=5, amount=0)
        self.assertEqual(result['status'], 'error')
        self.assertIn('Lütfen geçerli bir miktar giriniz', result['message'])
        
        # Test with negative amount (invalid)
        result = self.employee.create_expense_request(kalem_id=5, amount=-100)
        self.assertEqual(result['status'], 'error')
        self.assertIn('Lütfen geçerli bir miktar giriniz', result['message'])
        
        # Verify database was never called for inserts in these cases
        mock_db_instance.conn.commit.assert_not_called()
    
    @patch('controller.employee.ExpensePdfGenerator')
    def test_generate_expense_pdf_success(self, mock_pdf_generator_class):
        """Test successful generation of expense PDF."""
        # Mock the PDF generator
        mock_pdf_generator = MagicMock()
        mock_pdf_generator_class.return_value = mock_pdf_generator
        
        # Mock the sample PDF path that would be returned
        sample_pdf_path = "c:/users/expense_reports/expense_1.pdf"
        mock_pdf_generator.generate_expense_pdf.return_value = sample_pdf_path
        
        # Mock the database operations for get_approved_expense_detail
        self.employee.db = MagicMock()
        self.employee.db.cursor = MagicMock()
        
        # Mock data that would be returned for an approved expense
        mock_expense_data = {
            'harcamaId': 1,
            'kalemAd': 'Test Kalem',
            'tutar': 1000.0,
            'tarih': '2025-05-25',
            'onayDurumu': 'Onaylandi',
            'tazminTutari': 1000.0,
            'isim': 'Test',
            'soyisim': 'User'
        }
        
        # Mock the get_approved_expense_detail method to return our mock data
        with patch.object(Employee, 'get_approved_expense_detail', return_value=mock_expense_data):
            # Call the method to test
            result = self.employee.generate_expense_pdf(expense_id=1)
            
            # Verify results
            self.assertEqual(result['status'], 'success')
            self.assertEqual(result['path'], sample_pdf_path)
            self.assertIn(sample_pdf_path, result['message'])
            
            # Verify the PDF generator was called with correct parameters
            mock_pdf_generator.generate_expense_pdf.assert_called_once_with(mock_expense_data, self.mock_user_data)
            
            # Verify database update was called
            self.employee.db.cursor.execute.assert_called_once_with(
                "UPDATE harcama SET belgeYolu = ? WHERE harcamaId = ?", 
                (sample_pdf_path, 1)
            )
            self.employee.db.conn.commit.assert_called_once()
    
    @patch('controller.employee.ExpensePdfGenerator')
    def test_generate_expense_pdf_not_approved(self, mock_pdf_generator_class):
        """Test attempting to generate a PDF for a non-approved expense."""
        # Mock the get_approved_expense_detail to return None (no approved expense)
        with patch.object(Employee, 'get_approved_expense_detail', return_value=None):
            # Call the method to test
            result = self.employee.generate_expense_pdf(expense_id=1)
            
            # Verify results show an error
            self.assertEqual(result['status'], 'error')
            self.assertIn('Onaylanmış harcama bulunamadı', result['message'])
            
            # Verify PDF generator was never called
            mock_pdf_generator_class.return_value.generate_expense_pdf.assert_not_called()

if __name__ == '__main__':
    unittest.main()