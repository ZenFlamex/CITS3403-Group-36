import unittest
from unittest.mock import patch, MagicMock
from wtforms.validators import ValidationError
from app import create_app, db
from app.models import User
from app.forms import SignupForm
from config import TestConfig

# Helper class to mock the data attribute of WTForms fields
class MockField:
    def __init__(self, data, errors=None):
        self.data = data
        self.errors = errors if errors is not None else []

class FormValidationCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # Create a test user to simulate a user already existing in the database
        self.existing_user = User(username='testuser', email='test@example.com')
        self.existing_user.set_password('password') # Set a password for the test user
        db.session.add(self.existing_user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    # Test 3: SignupForm.validate_username - when username is already taken
    @patch('app.forms.User.query') 
    def test_signup_validate_username_taken(self, mock_query):
        mock_query.filter_by.return_value.first.return_value = self.existing_user
        
        form = SignupForm() 
        username_field = MockField(data='testuser') # Simulate user inputting 'testuser'

        with self.assertRaises(ValidationError) as context:
            form.validate_username(username_field)
        self.assertEqual(str(context.exception), 'Username already taken. Please choose a different one.')

if __name__ == '__main__':
    unittest.main(verbosity=2)