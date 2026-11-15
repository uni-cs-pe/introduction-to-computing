// Laboratorio, partes 2, 3 y 4: notas en una matriz.
//
// Cada fila es un estudiante y cada columna un curso. Las funciones reciben students, las
// filas que están en uso, que van de 1 a STUDENTS. No cambien STUDENTS ni COURSES.
// Borren las líneas (void): solo están para que el archivo compile sin advertencias.
//
// En main hay algunas pruebas. Agreguen más con assert: casos normales y bordes.
//
// Pruébenlo con make test-lab.
#include <assert.h>
#include <stdio.h>

#define STUDENTS 4
#define COURSES 3

// Guarda en averages[i] el promedio de las notas del estudiante i.
void student_averages(int grades[][COURSES], int students, double averages[]) {
    (void) grades;
    (void) students;
    (void) averages;
}

// Guarda en averages[j] el promedio de las notas del curso j.
void course_averages(int grades[][COURSES], int students, double averages[]) {
    (void) grades;
    (void) students;
    (void) averages;
}

// Guarda en best[j] el índice del estudiante con la nota más alta del curso j.
// Si hay un empate, gana el de índice menor.
void best_students(int grades[][COURSES], int students, int best[]) {
    (void) grades;
    (void) students;
    (void) best;
}

// Guarda en result la transpuesta de grades, que tiene STUDENTS filas: la fila i de
// grades pasa a ser la columna i de result.
void transpose(int grades[][COURSES], int result[][STUDENTS]) {
    (void) grades;
    (void) result;
}

// Devuelve 1 si result es la transpuesta de grades, y 0 si no.
// Revisa todas las casillas.
int is_transpose(int grades[][COURSES], int result[][STUDENTS]) {
    (void) grades;
    (void) result;
    return 0;
}

// Devuelve 1 si a y b se diferencian en menos de 0.001. Dos double no se comparan con ==.
int close_to(double a, double b) {
    double difference = a - b;
    return difference < 0.001 && difference > -0.001;
}

int main(void) {
    int grades[STUDENTS][COURSES] = {
        {14, 9, 17},
        {11, 16, 8},
        {18, 10, 15},
        {12, 20, 7},
    };
    double by_student[STUDENTS] = {0};
    double by_course[COURSES] = {0};
    int best[COURSES] = {0};
    int result[COURSES][STUDENTS] = {{0}};

    student_averages(grades, STUDENTS, by_student);
    assert(close_to(by_student[1], 35.0 / 3));

    course_averages(grades, STUDENTS, by_course);
    assert(close_to(by_course[0], 13.75));

    best_students(grades, STUDENTS, best);
    assert(best[0] == 2);

    transpose(grades, result);
    assert(result[2][1] == 8);
    assert(is_transpose(grades, result));

    result[0][0] = 0;
    assert(!is_transpose(grades, result));

    printf("Todas las pruebas pasaron\n");
    return 0;
}
