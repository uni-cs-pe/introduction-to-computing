# Muestra las instrucciones de la máquina virtual de Python para una función.
import dis


def add_one(x):
    return x + 1


dis.dis(add_one)
