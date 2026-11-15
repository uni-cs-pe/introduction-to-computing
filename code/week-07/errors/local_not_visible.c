#include <stdio.h>

int twice(int x) {
    int result = x * 2;
    return result;
}

// Error: result es local de twice. Aquí no existe.
int main(void) {
    twice(5);
    printf("%d\n", result);
    return 0;
}
