// No compila: dos struct no se comparan con ==.
#include <stdio.h>

#define NAME_SIZE 20
#define N_GRADES 3

struct student {
    char name[NAME_SIZE];
    int grades[N_GRADES];
};

int main(void) {
    struct student a = {"Ana", {14, 9, 17}};
    struct student b = a;

    if (a == b) {
        printf("Iguales\n");
    }
    return 0;
}
