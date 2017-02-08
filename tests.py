from app import app
from app.models import db,User,PostData
import unittest

class FlaskTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        # creates a test client
        self.app = app.test_client()
        # propagate the exceptions to the test client
        self.app.testing = True
        db.create_all()

    def login(self, username, password):
        return self.app.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_unlogin1_site_status_code(self):
        # sends HTTP GET request to the application
        # on the specified path
        result1 = self.app.get('/login')
        # assert the response data
        self.assertEqual(result1.status_code, 200)

    def test_unlogin2_site_status_code(self):
        # sends HTTP GET request to the application
        # on the specified path
        result1 = self.app.get('/allPost')
        # assert the response data
        self.assertEqual(result1.status_code, 200)

    def test_user_login(self):
        user = User('admin','admin@test.com','./app/static/uploads/admin-005.jpg','admin')
        db.session.add(user)
        db.session.commit()

        self.assertTrue(user.is_authenticated)
        user2 = self.login('admin', 'admin')
        
        self.logout()


if __name__ == '__main__':
    unittest.main()
