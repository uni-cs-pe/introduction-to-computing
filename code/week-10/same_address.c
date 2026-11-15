// La función recibe la dirección donde empieza el arreglo de main.
#include <stdio.h>

void show_address(int a[]) {
    printf("en la función, a: %p\n", (void *) a);
}

int main(void) {
    int grades[3] = {14, 9, 17};

    printf("en main, grades:  %p\n", (void *) grades);
    show_address(grades);
    return 0;
}
