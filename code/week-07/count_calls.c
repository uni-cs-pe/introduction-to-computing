#include <stdio.h>

// Intenta contar sus llamadas. Cada llamada crea un calls nuevo.
int count_calls(void) {
    int calls = 0;
    calls = calls + 1;
    return calls;
}

int main(void) {
    printf("%d\n", count_calls());
    printf("%d\n", count_calls());
    printf("%d\n", count_calls());
    return 0;
}
