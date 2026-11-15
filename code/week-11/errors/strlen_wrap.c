// Error: strlen da un valor sin signo. Restar 1 a un 0 da la vuelta.
#include <stdio.h>
#include <string.h>

int main(void) {
    char empty[] = "";

    printf("strlen(empty) - 1 = %zu\n", strlen(empty) - 1);
    if (strlen(empty) - 1 >= 0) {
        printf("Esta condición siempre se cumple\n");
    }
    return 0;
}
