// Factorial recursivo, con un rastro de cada llamada.
#include <assert.h>
#include <stdio.h>

// n debe ser 0 o más, y a lo sumo 20: 21! ya no cabe en 64 bits.
long long factorial(int n) {
    if (n <= 1) {
        return 1;
    }
    return n * factorial(n - 1);
}

long long factorial_trace(int n) {
    printf("entra factorial(%d)\n", n);
    if (n <= 1) {
        printf("caso base: factorial(%d) devuelve 1\n", n);
        return 1;
    }
    long long result = n * factorial_trace(n - 1);
    printf("factorial(%d) devuelve %lld\n", n, result);
    return result;
}

int main(void) {
    assert(factorial(0) == 1);
    assert(factorial(1) == 1);
    assert(factorial(5) == 120);
    assert(factorial(20) == 2432902008176640000);

    factorial_trace(4);
    printf("factorial(20) = %lld\n", factorial(20));
    return 0;
}
