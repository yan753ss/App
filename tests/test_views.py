import unittest
from app import create_app, db
from app.models import LogEntry
from datetime import datetime

class ViewTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['TESTING'] = True
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_get_logs(self):
        log_entry = LogEntry(
            ip_address='127.0.0.1',
            timestamp=datetime.strptime('2023-01-01 12:00:00', '%Y-%m-%d %H:%M:%S'),
            request='GET / HTTP/1.1',
            status_code=200,
            size=1234
        )
        db.session.add(log_entry)
        db.session.commit()

        response = self.client.get('/logs')
        self.assertEqual(response.status_code, 200)
        self.assertIn('127.0.0.1', response.get_data(as_text=True))

if __name__ == '__main__':
    unittest.main()
