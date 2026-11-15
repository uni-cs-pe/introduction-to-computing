#include <stdio.h>

// Con una condición falsa desde el inicio, while no entra y do while entra una vez.
int main(void) {
    int n = 5;

    while (n < 5) {
        printf("while: entré\n");
        n++;
    }

    do {
        printf("do while: entré\n");
        n++;
    } while (n < 5);

    printf("n vale %d\n", n);
    return 0;
}
