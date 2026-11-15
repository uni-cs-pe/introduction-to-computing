#include <stdio.h>

int max_of_two(int a, int b) {
    if (a > b) {
        return a;
    }
    return b;
}

// Error: max_of_two recibe dos argumentos.
int main(void) {
    printf("%d\n", max_of_two(5));
    return 0;
}
