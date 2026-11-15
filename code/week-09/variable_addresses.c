#include <stdio.h>

// Escribe el valor, el tamaño y la dirección de tres variables.
int main(void) {
    int age = 19;
    double average = 14.5;
    char section = 'A';

    printf("age     vale %d, ocupa %zu bytes, está en %p\n",
           age, sizeof(age), (void *) &age);
    printf("average vale %.1f, ocupa %zu bytes, está en %p\n",
           average, sizeof(average), (void *) &average);
    printf("section vale %c, ocupa %zu byte, está en %p\n",
           section, sizeof(section), (void *) &section);
    return 0;
}
