#include <stdio.h>

// Con paréntesis vacíos, C17 no revisa los argumentos de la llamada.
int get_year() {
    return 2026;
}

int main(void) {
    printf("%d\n", get_year(1, 2, 3));
    return 0;
}
