// Asignar un struct copia todos sus campos, también los arreglos que tiene dentro.
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

int main(void) {
    struct student a = {"Ana", {14, 9, 17}};
    struct student b = a;

    b.name[0] = 'E';
    b.grades[0] = 20;
    print_student(a);
    print_student(b);
    return 0;
}
