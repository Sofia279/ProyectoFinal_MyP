# Proyecto 3: Esquema del Secreto Compartido de Shamir
El proyecto consiste en encriptar una llave de cifrado usando el esquema de
Secreto Compartido de Shamir. Específicamente la llave de cifrado se usa para
encriptar y desencriptar un archivo con el esquema AES modo CBC a través de la
interfaz criptográfica de alto nivel Fernet.

## Integrantes del equipo:
- Alatorre Méndez Sofía Guadalupe
- Cornejo de la Mora Iñaki
- Orta Castillo Maria de los Angeles

## Pre-requisitos para compilar
- Python >= 3.6
- cryptography >= 41.0.7

Es necesario instalar la librería de Python cryptography, la forma más sencilla
es con el gestor de paquetes pip:
```bash
pip install cryptography
```
## Compilación del proyecto
Para compilar el proyecto, simplemente ejecuta el script principal `main.py` desde la línea de comandos, proporcionando los argumentos necesarios según la funcionalidad que desees utilizar. 
Para cifrar, se tendrá que proporcionar la bandera "c" (indica que se escogio la opcion de cifrado), la bandera "-p + [Nombre archivo de los pares del polinomio]", la bandera "-n + [Número total de evaluaciones requeridas (n > 2)]", la bandera "-m + [Número mínimo de puntos necesarios para descifrar (1 < t ≤ n).]" y la bandera [-f + Nombre del archivo con el documento claro].
Un ejemplo de como comilarlo es el siguiente: 
```bash
python main.py c -p pairs.txt -n 10 -m 5 -f foobar.txt
```
Para decifrar, se tendrá que proporcionar la bandera "d" (indica que se escogio la opcion de decifrado), la bandera "-p + [Nombre del archivo con al menos t de las n evaluaciones del polinomio]" y la bandera "-f + [Nombre del archivo cifrado]". 
Un ejemplo de como compilarlo es el siguiente: 
```bash
python main.py d -p pairs.txt -f foobar.aes
```
NOTA IMPORTANTE: En el repositorio no se agrego un ningun archivo de prueba para cifrar mas que el que se encuentra en la carpeta tests [pruebaTest.txt].
## Compilación de tests
Se compilara con el comando "python -m unittest". Lo que hará este comando será compilar todas las pruebas que encunetre en la carpeta tests. Además, se puede compilar estando en la carpeta principal ProyectoFinal_MyP.
```bash
python -m unittest
```
## Licencia
El proyecto se distribuirá bajo la Licencia MIT. La cual proporciona libertad significativa a los usuarios al permitirles utilizar, modificar y distribuir el software sin restricciones excesivas. Se otorga de forma gratuita y solo requiere que se incluyan los avisos de copyright y la exención de responsabilidad en las copias o derivados del software. Esta licencia fomenta la colaboración y el uso compartido, permitiendo tanto el uso comercial como no comercial del software, y garantiza una flexibilidad esencial para la comunidad de desarrollo.
