// Parte de las pruebas del laboratorio: test_lab.py llama con esto a sus funciones.
// No hace falta leerlo. Usa argumentos de la línea de comandos, que no vemos en el curso.
#include <stdio.h>
#include <stdlib.h>

#define STUDENTS 4
#define COURSES 3

int count_word(const char text[], const char word[]);
void student_averages(int grades[][COURSES], int students, double averages[]);
void course_averages(int grades[][COURSES], int students, double averages[]);
void best_students(int grades[][COURSES], int students, int best[]);
void transpose(int grades[][COURSES], int result[][STUDENTS]);
int is_transpose(int grades[][COURSES], int result[][STUDENTS]);

// Copia el texto a un arreglo propio, para que la función reciba memoria de la pila.
static void copy(char dest[], const char src[], int size) {
    int i = 0;
    while (src[i] != '\0' && i < size - 1) {
        dest[i] = src[i];
        i++;
    }
    dest[i] = '\0';
}

// Lee la matriz de los argumentos, fila por fila, y guarda una copia.
static void read_matrix(char *argv[], int first, int grades[][COURSES], int saved[][COURSES]) {
    for (int i = 0; i < STUDENTS; i++) {
        for (int j = 0; j < COURSES; j++) {
            grades[i][j] = atoi(argv[first + i * COURSES + j]);
            saved[i][j] = grades[i][j];
        }
    }
}

// Avisa si la función cambió la matriz que debía solo leer.
static void check_intact(int grades[][COURSES], int saved[][COURSES]) {
    for (int i = 0; i < STUDENTS; i++) {
        for (int j = 0; j < COURSES; j++) {
            if (grades[i][j] != saved[i][j]) {
                printf("la función cambió grades\n");
                return;
            }
        }
    }
}

static void print_doubles(const double a[], int n) {
    for (int i = 0; i < n; i++) {
        printf("%.2f ", a[i]);
    }
    printf("\n");
}

static int run_words(int argc, char *argv[]) {
    char text[128];
    char word[64];
    if (argc != 4) {
        return 2;
    }
    copy(text, argv[2], 128);
    copy(word, argv[3], 64);
    printf("%d\n", count_word(text, word));
    return 0;
}

static int run_matrix(char op, int argc, char *argv[]) {
    int grades[STUDENTS][COURSES];
    int saved[STUDENTS][COURSES];
    int total_args = 3 + STUDENTS * COURSES;

    if (argc < total_args) {
        return 2;
    }
    int students = atoi(argv[2]);
    read_matrix(argv, 3, grades, saved);

    if (op == 's') {
        double averages[STUDENTS] = {-1, -1, -1, -1};
        student_averages(grades, students, averages);
        print_doubles(averages, STUDENTS);
    } else if (op == 'c') {
        double averages[COURSES] = {-1, -1, -1};
        course_averages(grades, students, averages);
        print_doubles(averages, COURSES);
    } else if (op == 'b') {
        int best[COURSES] = {-1, -1, -1};
        best_students(grades, students, best);
        printf("%d %d %d\n", best[0], best[1], best[2]);
    } else if (op == 't') {
        int result[COURSES][STUDENTS];
        transpose(grades, result);
        for (int j = 0; j < COURSES; j++) {
            for (int i = 0; i < STUDENTS; i++) {
                printf("%d ", result[j][i]);
            }
            printf("\n");
        }
    } else if (op == 'i') {
        int other[COURSES][STUDENTS];
        if (argc != total_args + STUDENTS * COURSES) {
            return 2;
        }
        for (int j = 0; j < COURSES; j++) {
            for (int i = 0; i < STUDENTS; i++) {
                other[j][i] = atoi(argv[total_args + j * STUDENTS + i]);
            }
        }
        printf("%d\n", is_transpose(grades, other));
    } else {
        return 2;
    }
    check_intact(grades, saved);
    return 0;
}

int main(int argc, char *argv[]) {
    if (argc < 2) {
        return 2;
    }
    if (argv[1][0] == 'w') {
        return run_words(argc, argv);
    }
    return run_matrix(argv[1][0], argc, argv);
}
