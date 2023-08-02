import unittest
from unittest.mock import patch, MagicMock
import app


class TestFibonacci(unittest.TestCase):


    # def test_fibonacci_success(self):
    #
    #     with patch('app.time') as mock_sqlalchemy:
    #         mock_db = MagicMock()
    #         mock_sqlalchemy().return_value = mock_db
    #         self.assertEquals(app.generate_fibonacci(1), [0])
    #         mock_db.session.add.assert_called_once()
    #         # assert generate_fibonacci(1) == [0]

    # @patch('app.time')
    def test_time(self):
        with patch('app.flask_sqlalchemy') as mock_db:
            pass
            # app.something()
            # app.generate_fibonacci(1)


if __name__ == "__main__":
    unittest.main()