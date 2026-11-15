// Notas de 3 estudiantes en 4 cursos: promedios por fila y por columna.
#include <stdio.h>

#define STUDENTS 3
#define COURSES 4

int main(void) {
    int grades[STUDENTS][COURSES] = {
        {14, 9, 17, 12},
        {11, 16, 8, 13},
        {18, 10, 15, 20},
    };

    // Por filas: cada estudiante, y dentro de él, cada curso.
    for (int i = 0; i < STUDENTS; i++) {
        int total = 0;
        for (int j = 0; j < COURSES; j++) {
            total = total + grades[i][j];
        }
        printf("Estudiante %d: suma %d, promedio %.2f\n", i, total, (double) total / COURSES);
    }

    // Por columnas: cada curso, y dentro de él, cada estudiante.
    for (int j = 0; j < COURSES; j++) {
        int total = 0;
        for (int i = 0; i < STUDENTS; i++) {
            total = total + grades[i][j];
        }
        printf("Curso %d: suma %d, promedio %.2f\n", j, total, (double) total / STUDENTS);
    }
    return 0;
}
