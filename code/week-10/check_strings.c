// Parte de las pruebas del laboratorio: test_lab.py llama con esto a sus funciones.
// No hace falta leerlo. Usa argumentos de la línea de comandos, que no vemos en el curso.
#include <stdio.h>

int my_strlen(const char s[]);
int my_strcmp(const char a[], const char b[]);
void to_upper(char s[]);
int is_palindrome(const char s[]);
int is_palindrome_text(const char s[]);

// Copia el texto a un arreglo propio, para que la función reciba memoria de la pila.
static void copy(char dest[], const char src[], int size) {
    int i = 0;
    while (src[i] != '\0' && i < size - 1) {
        dest[i] = src[i];
        i++;
    }
    dest[i] = '\0';
}

int main(int argc, char *argv[]) {
    if (argc < 3) {
        return 2;
    }
    char op = argv[1][0];
    char first[64];
    char second[64];
    copy(first, argv[2], 64);
    copy(second, argc > 3 ? argv[3] : "", 64);

    if (op == 'l') {
        printf("%d\n", my_strlen(first));
    } else if (op == 'c') {
        printf("%d\n", my_strcmp(first, second));
    } else if (op == 'u') {
        to_upper(first);
        printf("%s\n", first);
    } else if (op == 'p') {
        printf("%d\n", is_palindrome(first));
    } else if (op == 't') {
        printf("%d\n", is_palindrome_text(first));
    } else {
        return 2;
    }
    return 0;
}
