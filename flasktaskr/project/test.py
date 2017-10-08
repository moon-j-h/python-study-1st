import os
import unittest

from views import app, db
from _config import basedir
from models import User

TEST_DB = 'test.db'

class AllTests(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, TEST_DB)
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_users_can_register(self):
        new_user = User('moon1234', 'moon1234@gmail.com', '1234567890')
        db.session.add(new_user)
        db.session.commit()
        test = db.session.query(User).all()
        for t in test:
            t.name
        assert t.name == 'moon1234'

    # def test_form_is_present(self):
    #     response = self.app.get('/')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIn(b'Please sign in to access your task list', response.data)

    def login(self, name, password):
        return self.app.post('/', data=dict(name=name, password=password), follow_redirects=True)

    def test_users_cannot_login_unless_registered(self):
        response = self.login('foo', 'bar')
        self.assertIn(b'Invalid username or password', response.data)

    def register(self, name, email, password, confirm):
        return self.app.post(
            'register/',
            data=dict(name=name, email=email, password=password, confirm=confirm),
            follow_redirects=True
        )

    def test_users_can_login(self):
        self.register('moon1008', 'moon1008@gmail.com', '123456789', '123456789')
        response = self.login('alert("alert box!")', 'moon1008')
        self.assertIn(b'Invalid username or password', response.data)

    def test_form_is_present_on_register_page(self):
        response = self.app.get('register/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please register to access the task list.', response.data)

    def test_user_registration(self):
        self.app.get('register/', follow_redirects=True)
        response = self.register('moon1008', 'moon1008@gmail.com', '123456789', '123456789')
        self.assertIn(b'Thanks for registering. Please login.', response.data)

    def test_user_registration_error(self):
        self.app.get('register/', follow_redirects=True)
        self.register('moon1008', 'moon1008@gmail.com', '123456789', '123456789')
        self.app.get('register/', follow_redirects=True)
        response = self.register('moon1008', 'moon1008@gmail.com', '123456789', '123456789')
        self.assertIn(b'already exist.', response.data)

    def logout(self):
        return self.app.get('logout/', follow_redirects=True)

    def test_logged_in_users_can_logout(self):
        self.register('moon1008', 'moon1008@gmail.com', '123456789', '123456789')
        self.login('moon1008', '123456789')
        response = self.logout()
        self.assertIn(b'Goodbye!', response.data)

    def test_not_logged_in_users_cannot_logout(self):
        response = self.logout()
        self.assertNotIn(b'Goodbye!', response.data)

    def test_logged_in_users_can_access_tasks_page(self):
        self.register('moon1008', 'moon1008@gmail.com', '123456789', '123456789')
        self.login('moon1008', '123456789')
        response = self.app.get('tasks/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Add a new task:', response.data)

    def test_not_logged_in_users_cannot_access_tasks_page(self):
        response = self.app.get('tasks/', follow_redirects=True)
        self.assertIn(b'login first.', response.data)

    def create_user(self, name, email, password):
        new_user = User(name=name, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

    def create_task(self):
        return self.app.post('add/', data=dict(
            name='Go to the bank',
            due_date='10/18/2107',
            priority='1',
            posted_date='10/08/2017',
            status='1'
        ), follow_redirects=True)

    def test_users_can_add_tasks(self):
        self.create_user('moon1234', 'moon1234@naver.com', 'python')
        self.login('moon1234', 'python')
        self.app.get('tasks/', follow_redirects=True)
        response = self.create_task()
        self.assertIn(b'Successfully posted.', response.data)

    def test_users_cannot_add_tasks_when_error(self):
        self.create_user('moon1234', 'moon1234@naver.com', 'python')
        self.login('moon1234', 'python')
        self.app.get('tasks/', follow_redirects=True)
        response = self.app.post('add/', data=dict(
            name='Go to the bank',
            due_date='',
            priority='1',
            posted_date='10/08/2017',
            status='1'
        ), follow_redirects=True)

    def test_users_can_complete_tasks(self):
        self.create_user('moon1234', 'moon1234@naver.com', 'python')
        self.login('moon1234', 'python')
        self.app.get('tasks/', follow_redirects=True)
        self.create_task()
        response = self.app.get('complete/1/', follow_redirects=True)
        self.assertIn(b'Complete!', response.data)

    def test_users_can_delete_tasks(self):
        self.create_user('moon1234', 'moon1234@naver.com', 'python')
        self.login('moon1234', 'python')
        self.app.get('tasks/', follow_redirects=True)
        self.create_task()
        response = self.app.get('delete/1/', follow_redirects=True)
        self.assertIn(b'Successfully Deleted', response.data)

    def test_users_cannot_complete_tasks_that_are_not_created_by_them(self):
        self.create_user('moon1234', 'moon1234@naver.com', 'python')
        self.login('moon1234', 'python')
        self.app.get('tasks/', follow_redirects=True)
        self.create_task()
        self.logout()
        self.create_user('moon4567', 'moon4567@naver.com', 'python')
        self.login('moon4567', 'python')
        self.app.get('tasks/', follow_redirects=True)
        response = self.app.get("complete/1/", follow_redirects=True)
        self.assertNotIn(b'Complete!', response.data)

if __name__=='__main__':
    unittest.main()