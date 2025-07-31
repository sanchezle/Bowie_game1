from unittest.mock import patch
import unittest
from app import app, db, generate_provisional_username

class TestProvisionalUsername(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    @patch('app.db.execute')
    def test_username_generation_unique(self, mock_db_execute):
        # Set a side_effect to handle any username, mimicking database behavior
        def mock_execute(query, params):
            username = params[0]
            # Simulate database count responses: 'user1' to 'user12' are taken
            if username in [f'user{i}' for i in range(1, 13)]:
                return [{'count': 1}]
            return [{'count': 0}]

        mock_db_execute.side_effect = mock_execute
        
        result = generate_provisional_username('user1')
        self.assertEqual(result, 'user13')

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
