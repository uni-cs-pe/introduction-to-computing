// No compila: el nombre del tipo es "struct student", no "student".
#include <stdio.h>

#define NAME_SIZE 20
#define N_GRADES 3

struct student {
    char name[NAME_SIZE];
    int grades[N_GRADES];
};

int main(void) {
    student s;

    printf("%zu\n", sizeof(s));
    return 0;
}
