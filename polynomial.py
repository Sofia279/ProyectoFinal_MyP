from password import derive_key
from cryptography.fernet import Fernet
from fractions import Fraction
import pathlib
import random


class Polynomial:
    def __init__(self, pair_file: str) -> None:
        '''
        Método constructor que inicializa una instancia de la clase Polynomial con un atributo pair_file.
        Parámetros:
        - pair_file: Ruta al archivo donde se guardarán las evaluaciones del polinomio.
        Resultado:
        - Ninguno (_init_ no regresa resultados explicitos).
        Precondiciones:
        - Ninguno.
        Postcondiciones:
        - Se crea una instancia de Polynomial con el atributo pair_file inicializado.
        '''
        self.pair_file = pair_file

    def write_pairs(self, shares: int, minimum: int, password: str) -> None:
        ''' 
        Función que genera coeficientes aleatorios para un polinomio y escribe puntos (x, f(x)) en un archivo. 
        Este archivo se utiliza posteriormente para recuperar la contraseña.
        Parámetros:
        - shares: Número total de evaluaciones requeridas (n > 2).
        - minimum : Número mínimo de puntos necesarios para descifrar (1 < t ≤ n).
        - password: Contraseña (solicitada durante la ejecución sin hacer eco en la terminal).
        Resultado:
        - Ninguno
        Precondiciones:
        - shares > 2
        - shares >= minimum
        - El archivo especificado por `pair_file` debe existir.
        Postcondiciones:
        - Se generan coeficientes aleatorios y se escriben pares de puntos (x, f(x)) en el archivo.
        '''
        assert shares > 2, "El número total de datos debe ser mayor a dos."
        assert shares >= minimum, "El mínimo de datos no puede ser mayor" \
            "que el número total de datos."
        coefficients: list[int] = []

        def generate_coefficients(key: bytes) -> None:
            ''' 
             Función que construye una lista de coeficientes para un polinomio. 
             El primer coeficiente es derivado de la clave dada, y los coeficientes restantes son números 
             aleatorios generados criptográficamente.
             Parámetros:
             - key: Clave utilizada para derivar el primer coeficiente.
             Resultado:
             - Ninguno.
             Precondiciones:
             - Ninguno.
             Postcondiciones:
             - Se generan coeficientes para un polinomio.
             '''
            rand = random.SystemRandom()
            coefficients.append(int.from_bytes(key))
            for i in range(minimum - 1):
                coefficients.append(rand.randint(0, 2 ** 16))

        def polynomial(x: int) -> int:
            '''
            Función que toma un valor x como entrada y devuelve el resultado de evaluar un polinomio cuyos 
            coeficientes están definidos en la lista coefficients. 
            Parámetros:
            - x: Valor para evaluar el polinomio.
            Resultado:
            - int: Resultado de evaluar el polinomio en x.
            Precondiciones:
            - Ninguna
            Postcondiciones:
            - Ninguna
            '''
            return sum(coefficients[i] * x ** i for i in range(minimum))

        '''
        Genera una clave derivada a partir de una contraseña utilizando PBKDF2-HMAC con SHA-256 
        y luego utiliza esa clave derivada para generar coeficientes para un polinomio. 
        '''
        generate_coefficients(derive_key(password))

        with open(self.pair_file, 'w') as file:
            '''
            Crea un archivo y escribe pares de puntos (x, f(x)) generados por un polinomio en el rango de 1 a shares. 
            '''
            for point in range(1, shares + 1):
                file.write(f"{point} {polynomial(point)}\n")

    def get_password(self) -> str:
        '''
        Reconstruye la contraseña original utilizando la interpolación de Lagrange
        a partir de los puntos almacenados en el archivo y evalúa el polinomio en x=0.
        Parámetros:
        - Ninguno explícito, pero depende del atributo `pair_file` de la instancia.
        Resultado:
        - Una cadena de texto que representa la contraseña original.
        Precondiciones:
        - El archivo especificado por `pair_file` debe contener pares de puntos (x, y)
          que serán utilizados para la interpolación de Lagrange.
        Postcondiciones:
        - Ninguna explícita.
        '''
        with open(self.pair_file, 'r') as file:
            pairs = [(int(x), int(y))
                     for x, y in [line.split() for line in file]]
        acc = Fraction(0)
        for i in range(len(pairs)):
            prod = Fraction(1)
            for j in range(len(pairs)):
                if i == j:
                    continue
                prod *= Fraction(pairs[i][0], pairs[i][0] - pairs[j][0])
            acc += pairs[i][1] * prod
        return int(acc).to_bytes(length=44).decode('utf-8')

    def encrypt_file(self, file: str, password: str) -> None:
        '''
        Encripta un archivo utilizando el algoritmo de cifrado simétrico Fernet.
        Parámetros:
        - file: Ruta al archivo de entrada que se va a encriptar.
        - password: Contraseña utilizada para derivar la clave de encriptación.
        Resultado:
        - Ninguno.
        Precondiciones:
        - El archivo especificado por `file` debe existir.
        Postcondiciones:
        - Un nuevo archivo con extensión '.aes' se crea en la misma ubicación que el archivo de entrada,
          conteniendo el contenido encriptado.
        '''
        clear_file = pathlib.Path(file)
        assert clear_file.exists(), "El archivo proporcionado no existe."
        fernet = Fernet(derive_key(password))
        with open(clear_file.stem + '.aes', 'wb') as encrypted_file:
            encrypted_file.write(fernet.encrypt(clear_file.read_bytes()))

    def decrypt_file(self, file: str, password: str) -> None:
        '''
        Desencripta un archivo que fue encriptado utilizando encriptación simétrica Fernet.
        Parámetros:
        - file: Ruta al archivo encriptado que se va a desencriptar.
        - password: Contraseña utilizada para derivar la clave de encriptación.
        Resultado:
        - Ninguno.
        Precondiciones:
        - El archivo especificado por `file` debe existir.
        Postcondiciones:
        - Un nuevo archivo con extensión '.txt' se crea en la misma ubicación que el archivo encriptado,
          conteniendo el contenido desencriptado.
        '''
        encrypted_file = pathlib.Path(file)
        assert encrypted_file.exists(), "El archivo proporcionado no existe."
        fernet = Fernet(derive_key(password))
        with open(encrypted_file.stem + '.txt', 'wb') as clear_file:
            clear_file.write(fernet.decrypt(encrypted_file.read_bytes()))
