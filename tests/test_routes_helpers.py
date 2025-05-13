import unittest
from datetime import datetime
from app import create_app, db 
from config import TestConfig 
from app.routes import format_datetime_custom, allowed_file, get_favorite_genre 

class RoutesHelpersTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        
    def tearDown(self):
        self.app_context.pop()
        
    # Test 4: allowed_file allows valid file extensions
    def test_allowed_file_allows_valid_extensions(self):
        """Test if the allowed_file function correctly identifies permitted file extensions."""
        self.assertTrue(allowed_file('image.png'), ".png should be allowed")
        self.assertTrue(allowed_file('document.JPG'), ".JPG (uppercase) should be allowed if logic is case-insensitive")
        self.assertTrue(allowed_file('archive.jpeg'), ".jpeg should be allowed")
        self.assertTrue(allowed_file('animation.gif'), ".gif should be allowed")
        self.assertFalse(allowed_file('script.txt'), ".txt should not be allowed") # Test a disallowed extension
        self.assertFalse(allowed_file('image.png.exe'), ".exe should not be allowed even if .png is present") # Test tricky filename
        self.assertFalse(allowed_file('nodotextension'), "filename with no dot should not be allowed") # Test filename without extension


    # Test 5: format_datetime_custom with a datetime object
    def test_format_datetime_with_datetime_object(self):
        """Test if the format_datetime_custom template filter correctly formats datetime objects."""
        dt = datetime(2023, 1, 15, 14, 30, 0)
        # Test default format
        self.assertEqual(format_datetime_custom(dt), "15 January 2023 14:30")
        # Test custom format
        self.assertEqual(format_datetime_custom(dt, format="%Y/%m/%d"), "2023/01/15")
        # Test date only format
        self.assertEqual(format_datetime_custom(dt, format="%d-%m-%Y"), "15-01-2023")


if __name__ == '__main__':
    unittest.main(verbosity=2)