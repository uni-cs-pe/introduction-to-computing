// Un struct agrupa los datos de un estudiante.
#include <stdio.h>
#include <string.h>

#define NAME_SIZE 20
#define N_GRADES 3

struct student {
    char name[NAME_SIZE];
    int grades[N_GRADES];
};

int main(void) {
    struct student s = {"Ana", {14, 9, 17}};

    printf("%s: %d %d %d\n", s.name, s.grades[0], s.grades[1], s.grades[2]);
    s.grades[1] = 12;
    printf("Después del cambio: %d\n", s.grades[1]);
    strncpy(s.name, "Beatriz", NAME_SIZE - 1);
    s.name[NAME_SIZE - 1] = '\0';
    printf("Nuevo nombre: %s\n", s.name);
    printf("sizeof(struct student) = %zu\n", sizeof(struct student));
    return 0;
}
