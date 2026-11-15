// No compila: un arreglo, como name, no se asigna con =.
#include <stdio.h>

#define NAME_SIZE 20
#define N_GRADES 3

struct student {
    char name[NAME_SIZE];
    int grades[N_GRADES];
};

int main(void) {
    struct student s;

    s.name = "Ana";
    printf("%s\n", s.name);
    return 0;
}
