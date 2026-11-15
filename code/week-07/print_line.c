#include <stdio.h>

// Escribe una línea de guiones del ancho pedido. No devuelve nada.
void print_line(int width) {
    for (int i = 0; i < width; i++) {
        printf("-");
    }
    printf("\n");
}

// Escribe el encabezado de una boleta. No recibe nada y no devuelve nada.
void print_header(void) {
    print_line(20);
    printf("Boleta de notas\n");
    print_line(20);
}

int main(void) {
    print_header();
    printf("Promedio: 14\n");
    print_line(5);
    return 0;
}
