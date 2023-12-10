import argparse
from polynomial import Polynomial
from getpass import getpass

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('option', choices=['c', 'd'], help='Opciones: "c" para cifrar y "d" para descifrar.')
    parser.add_argument('-p', 
                        '--pair_file',
                        help='Nombre del archivo para guardar las evaluaciones pares del polinomio.')
    parser.add_argument('-n', 
                        '--shares', 
                        type=int,
                        help='Número total de evaluaciones requeridas (n > 2).')
    parser.add_argument('-m', 
                        '--minimum',
                        type=int, 
                        help='Número mínimo de puntos necesarios para descifrar (1 < t ≤ n).')
    parser.add_argument('-f', 
                        '--clear_file', 
                        help='Nombre del archivo con el documento claro.')

    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    
    if args.option == 'c':
        assert args.pair_file is not None, "Especifica el nombre del archivo para guardar las evaluaciones del polinomio."
        assert args.shares is not None and args.shares > 2, "Especifica el número total de evaluaciones requeridas, el cual tiene que ser mayor a 2 (n > 2)."
        assert args.minimum is not None and 1 < args.minimum <= args.shares, "Especifica un número mínimo de puntos necesarios para descifrar, el cual tiene que ser mayor a 1 y menor o igual a el número total de evaluaciones requeridas (1 < t ≤ n)."
        assert args.clear_file is not None, "Especifica el nombre del archivo con el documento claro."

        password = getpass("Contraseña: ")
        p = Polynomial(args.pair_file)
        p.write_pairs(args.shares, args.minimum, password)
        p.encrypt_file(args.clear_file, password) 

    elif args.option == 'd':
        assert args.pair_file is not None, "Especifica el nombre del archivo con al menos t de las n evaluaciones del polinomio."
        assert args.clear_file is not None, "Especifica el nombre del archivo cifrado."

        password = getpass("Contraseña: ")
        p = Polynomial(args.pair_file)
        p.decrypt_file(args.clear_file, password) 
        
    else:
        print("Opción no válida. Usa 'c' para cifrar o 'd' para descifrar.")
