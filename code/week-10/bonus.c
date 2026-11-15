// Un int se copia al llamar. Un arreglo no se copia: se pasa su dirección.
#include <stdio.h>

#define N 3

void add_one(int x) {
    x = x + 1;
}

void add_bonus(int a[], int n, int bonus) {
    for (int i = 0; i < n; i++) {
        a[i] = a[i] + bonus;
    }
}

int main(void) {
    int grade = 14;
    add_one(grade);
    printf("grade: %d\n", grade);

    int grades[N] = {14, 9, 17};
    add_bonus(grades, N, 2);
    printf("grades: %d %d %d\n", grades[0], grades[1], grades[2]);
    return 0;
}
