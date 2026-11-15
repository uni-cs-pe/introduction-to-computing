# Cuenta los primos hasta un límite que lee de la entrada.


def is_prime(n):
    if n < 2:
        return False
    d = 2
    while d <= n // d:
        if n % d == 0:
            return False
        d = d + 1
    return True


limit = int(input())
count = 0
for n in range(2, limit + 1):
    if is_prime(n):
        count = count + 1
print(f"Hay {count} primos hasta {limit}")
