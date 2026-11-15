// Un struct llega por valor: la función trabaja sobre una copia.
#include <stdio.h>

#define NAME_SIZE 20
#define N_GRADES 3

struct student {
    char name[NAME_SIZE];
    int grades[N_GRADES];
};

void print_student(struct student s) {
    printf("%s: %d %d %d\n", s.name, s.grades[0], s.grades[1], s.grades[2]);
}

// Cambia su copia. Quien llama no ve nada.
void reset_first(struct student s) {
    s.grades[0] = 0;
    printf("En la función: %d\n", s.grades[0]);
}

// Devuelve la copia cambiada. Quien llama decide si la guarda.
struct student with_first(struct student s, int grade) {
    s.grades[0] = grade;
    return s;
}

// Recibe un arreglo: llega su dirección, y sí cambia el original.
void reset_first_array(int grades[]) {
    grades[0] = 0;
}

int main(void) {
    struct student a = {"Ana", {14, 9, 17}};

    reset_first(a);
    print_student(a);

    a = with_first(a, 16);
    print_student(a);

    reset_first_array(a.grades);
    print_student(a);
    return 0;
}
