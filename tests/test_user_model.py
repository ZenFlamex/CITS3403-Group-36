import unittest
from app import create_app, db
from app.models import User
from config import TestConfig

class UserModelCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    # Test 1: User.check_password returns True for a correct password_hash
    def test_password_checking_correct(self):
        u = User(username='john', email='john@example.com')
        u.set_password('dog') 
        self.assertTrue(u.check_password('dog'), "check_password should return True for the correct password.")

    # Test 2: User.check_password returns False when password_hash is None
    def test_password_checking_none_hash(self):
        u = User(username='bob', email='bob@example.com')
        # At this point, u.password_hash should be None because set_password has not been called
        self.assertIsNone(u.password_hash, "password_hash should be None for a new user if set_password was not called.")
        self.assertFalse(u.check_password('any_password'), "check_password should return False if password_hash is None.")

if __name__ == '__main__':
    unittest.main(verbosity=2)
