// Un arreglo de struct: cada elemento guarda todos los datos de un estudiante.
#include <stdio.h>

#define NAME_SIZE 20
#define N_GRADES 3
#define MAX_STUDENTS 5

struct student {
    char name[NAME_SIZE];
    int grades[N_GRADES];
};

double average(struct student s) {
    int total = 0;
    for (int i = 0; i < N_GRADES; i++) {
        total = total + s.grades[i];
    }
    return (double) total / N_GRADES;
}

// Devuelve la posición del mejor promedio, o -1 si no hay estudiantes.
int best_index(const struct student list[], int n) {
    if (n <= 0) {
        return -1;
    }
    int best = 0;
    for (int i = 1; i < n; i++) {
        if (average(list[i]) > average(list[best])) {
            best = i;
        }
    }
    return best;
}

// Elimina la posición pos y devuelve la longitud nueva, como en la semana 10.
int remove_at(struct student list[], int n, int pos) {
    if (pos < 0 || pos >= n) {
        return n;
    }
    for (int i = pos; i < n - 1; i++) {
        list[i] = list[i + 1];
    }
    return n - 1;
}

// Recibe un arreglo: sí cambia los elementos de quien llama.
void reset_first_grades(struct student list[], int n) {
    for (int i = 0; i < n; i++) {
        list[i].grades[0] = 0;
    }
}

void print_list(const struct student list[], int n) {
    for (int i = 0; i < n; i++) {
        printf("%s: %.2f\n", list[i].name, average(list[i]));
    }
}

int main(void) {
    struct student list[MAX_STUDENTS] = {
        {"Ana", {14, 9, 17}},
        {"Bruno", {8, 10, 11}},
        {"Carla", {11, 11, 11}},
    };
    int n = 3;

    print_list(list, n);
    printf("Mejor: %s\n", list[best_index(list, n)].name);

    n = remove_at(list, n, 1);
    printf("Sin Bruno:\n");
    print_list(list, n);

    reset_first_grades(list, n);
    printf("Con la primera nota en 0:\n");
    print_list(list, n);
    return 0;
}
