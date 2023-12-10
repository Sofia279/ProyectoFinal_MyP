import unittest
import tempfile
from unittest.mock import patch
from io import StringIO
from main import parse_args
from password import derive_key

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

    def test_derive_key(self):
            # Caso de prueba con una contraseña conocida
            password = "mi_contraseña_123"
            expected_key = b'l3RMFUtpa9Tp-auqDRrl54wKhYUMz6fNX3YiVrWcqtk='  # Este valor puede variar si cambias la contraseña
            # Llamada a la función
            actual_key = derive_key(password)
            # Verificación de la igualdad
            self.assertEqual(actual_key, expected_key)

    def test_derive_key_different_password(self):
        # Caso de prueba con otra contraseña conocida
        password = "otra_contraseña_456"
        expected_key = b'04Ygta5ZSToJ-E8cK74WCkpFr-vwTJUiuahZ0ZOGyKs='  # Este valor puede variar si cambias la contraseña
        # Llamada a la función
        actual_key = derive_key(password)
        # Verificación de la igualdad
        self.assertEqual(actual_key, expected_key)

            
if __name__ == '__main__':
    unittest.main()
