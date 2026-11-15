# Cuántos bytes ocupa un entero de Python. Depende de la versión y de la máquina.
import sys

print(sys.getsizeof(1))
print(sys.getsizeof(2 ** 100))
