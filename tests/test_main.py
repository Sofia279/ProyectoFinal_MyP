import unittest
from unittest.mock import patch
from io import StringIO
from main import parse_args

class MainTestCase(unittest.TestCase):
    def test_parse_args_c_encrypt(self):
        with patch('sys.argv', ['main.py', 'c', '-p', 'pairs.txt', '-n', '10', '-m', '5', '-f', 'pruebaTest.txt']):
            args = parse_args()
        self.assertEqual(args.option, 'c')
        self.assertEqual(args.pair_file, 'pairs.txt')
        self.assertEqual(args.shares, 10)
        self.assertEqual(args.minimum, 5)
        self.assertEqual(args.clear_file, 'pruebaTest.txt')

    def test_parse_args_d_decrypt(self):
        with patch('sys.argv', ['main.py', 'd', '-p', 'pairs.txt', '-f', 'pruebaTest.aes']):
            args = parse_args()
        self.assertEqual(args.option, 'd')
        self.assertEqual(args.pair_file, 'pairs.txt')
        self.assertEqual(args.clear_file, 'pruebaTest.aes')

    def test_parse_args_invalid_option(self):
        with patch('sys.argv', ['main.py', 'x']):
            with patch('sys.stderr', new_callable=StringIO) as mock_stderr:
                with self.assertRaises(SystemExit) as cm:
                    parse_args()
                self.assertEqual(cm.exception.code, 2)
                self.assertIn('invalid choice', mock_stderr.getvalue().lower())

if __name__ == '__main__':
    unittest.main()
