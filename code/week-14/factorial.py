# El mismo factorial. Aquí el entero crece todo lo que haga falta.
n = int(input())
result = 1
for i in range(2, n + 1):
    result = result * i
print(f"{n}! = {result}")
