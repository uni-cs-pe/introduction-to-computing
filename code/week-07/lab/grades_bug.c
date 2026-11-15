// Laboratorio, parte 2: este programa compila sin advertencias, pero tiene 4 bugs.
// Encuéntrenlos con gdb, corríjanlos aquí mismo y dejen la misma forma de salida.
//
// El programa lee la cantidad de notas, y luego las notas (enteros de 0 a 20).
// Se aprueba con 11 o más. Con esta entrada:
//   4
//   12 8 11 15
// debe escribir:
//   Promedio: 11.50
//   Aprobados: 3
//
// Pruébenlo con make test-lab. Para usar gdb, compílenlo como dicen los apuntes.
#include <stdio.h>

// Devuelve 1 si la nota aprueba y 0 si no.
int is_passing(int grade) {
    return grade > 11;
}

// Devuelve la cuenta de aprobados después de mirar una nota más.
int count_if_passing(int passing, int grade) {
    if (is_passing(grade)) {
        passing = passing + 1;
    }
    return passing;
}

// Devuelve el total después de sumarle una nota.
int add_grade(int total, int grade) {
    total = total + grade;
    return total;
}

// Devuelve el promedio de count notas que suman total.
double average(int total, int count) {
    return total / count;
}

int main(void) {
    int count;

    if (scanf("%d", &count) != 1 || count <= 0) {
        printf("Cantidad inválida\n");
        return 1;
    }

    int total = 0;
    int passing = 0;

    for (int i = 1; i < count; i++) {
        int grade;

        if (scanf("%d", &grade) != 1 || grade < 0 || grade > 20) {
            printf("Nota inválida\n");
            return 1;
        }

        add_grade(total, grade);
        passing = count_if_passing(passing, grade);
    }

    printf("Promedio: %.2f\n", average(total, count));
    printf("Aprobados: %d\n", passing);
    return 0;
}
