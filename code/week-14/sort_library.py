# Los mismos datos, con sorted: un algoritmo mejor, escrito en C dentro de Python.
n = int(input())
values = [(i * 7919) % 100003 for i in range(n)]
values = sorted(values)
print(f"menor: {values[0]}, mayor: {values[n - 1]}")
