#include <stdio.h>

// Devuelve el mayor de dos enteros.
int max_of_two(int a, int b) {
    if (a > b) {
        return a;
    }
    return b;
}

// Devuelve el mayor de tres enteros, apoyándose en la función anterior.
int max_of_three(int a, int b, int c) {
    return max_of_two(max_of_two(a, b), c);
}

int main(void) {
    int a, b, c;

    if (scanf("%d %d %d", &a, &b, &c) != 3) {
        printf("Entrada inválida\n");
        return 1;
    }

    printf("%d\n", max_of_three(a, b, c));
    return 0;
}
