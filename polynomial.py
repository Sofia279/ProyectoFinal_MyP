from password import derive_key
from cryptography.fernet import Fernet
from fractions import Fraction
import pathlib
import random


class Polynomial:
    def __init__(self, pair_file: str) -> None:
        self.pair_file = pair_file

    def write_pairs(self, shares: int, minimum: int, password: str) -> None:
        assert shares > 2, "El número total de datos debe ser mayor a dos."
        assert shares >= minimum, "El mínimo de datos no puede ser mayor" \
            "que el número total de datos."
        coefficients: list[int] = []

        def generate_coefficients(key: bytes) -> None:
            rand = random.SystemRandom()
            coefficients.append(int.from_bytes(key))
            for i in range(minimum - 1):
                coefficients.append(rand.randint(0, 2 ** 16))

        def polynomial(x: int) -> int:
            return sum(coefficients[i] * x ** i for i in range(minimum))

        generate_coefficients(derive_key(password))

        # https://en.wikipedia.org/wiki/Shamir%27s_secret_sharing#Preparation
        with open(self.pair_file, 'w') as file:
            for point in range(1, shares + 1):
                file.write(f"{point} {polynomial(point)}\n")

    def get_password(self) -> str:
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
        clear_file = pathlib.Path(file)
        assert clear_file.exists(), "El archivo proporcionado no existe."
        fernet = Fernet(derive_key(password))
        with open(clear_file.stem + '.aes', 'wb') as encrypted_file:
            encrypted_file.write(fernet.encrypt(clear_file.read_bytes()))
