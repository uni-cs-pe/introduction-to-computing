// Laboratorio, parte 1: dos funciones con sus pruebas.
//
// is_prime(n)       devuelve 1 si n es primo y 0 si no lo es. Un primo es un entero
//                   mayor que 1 cuyos únicos divisores positivos son 1 y él mismo.
//                   Debe funcionar con cualquier int, también con 0 y con negativos,
//                   que no son primos.
// is_leap_year(y)   devuelve 1 si el año y es bisiesto y 0 si no lo es. La regla es la
//                   de la semana 4.
//
// Las dos versiones de abajo compilan, pero están mal: solo sirven para empezar.
// Reemplácenlas. Las funciones no leen ni escriben nada.
//
// En main, agreguen sus pruebas con assert: al menos 6 para is_prime y 4 para
// is_leap_year. Las pruebas de make test-lab cuentan esas líneas, así que escriban un
// assert por línea, empezando con assert(is_prime( o assert(is_leap_year(.
//
// Pruébenlo con make test-lab.
#include <assert.h>
#include <stdio.h>

int is_prime(int n) {
    return n == 2;
}

int is_leap_year(int year) {
    return year == 2024;
}

int main(void) {
    assert(is_prime(2) == 1);
    assert(is_leap_year(2024) == 1);
    // Escriban aquí el resto de sus pruebas.

    printf("Todas las pruebas pasaron\n");
    return 0;
}
