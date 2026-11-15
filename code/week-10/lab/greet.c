// Laboratorio, parte 3: este programa tiene un buffer overflow a propósito.
//
// Primero provóquenlo: escriban un nombre de más de 7 letras y lean el informe de
// -fsanitize=address. Después corríjanlo con fgets, para que el programa:
//
//   - lea una línea completa, también con espacios, en name;
//   - quite el salto de línea, si está;
//   - escriba "Hola, " y el nombre, y termine con return 0;
//   - guarde solo los primeros 7 bytes si el nombre no cabe, y escriba eso;
//   - escriba "Entrada inválida" y termine con return 1 si no hay ninguna línea o si
//     la línea está vacía.
//
// No cambien SIZE. Pruébenlo con make test-lab.
#include <stdio.h>

#define SIZE 8

int main(void) {
    char name[SIZE];

    if (scanf("%s", name) != 1) {
        printf("Entrada inválida\n");
        return 1;
    }
    printf("Hola, %s\n", name);
    return 0;
}
