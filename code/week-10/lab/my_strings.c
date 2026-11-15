// Laboratorio, partes 1 y 2: funciones de cadenas, sin string.h.
//
// Escriban cada función según su comentario. Borren la línea (void) de cada una:
// solo está para que el archivo compile sin advertencias mientras tanto.
// Las cadenas pueden traer bytes de UTF-8, como los dos de la ñ.
//
// En main hay una prueba de cada función. Agreguen más con assert: casos normales
// y bordes, como la cadena vacía.
//
// Pruébenlo con make test-lab.
#include <assert.h>
#include <stdio.h>

// Devuelve cuántos bytes hay antes del '\0'.
int my_strlen(const char s[]) {
    (void) s;
    return 0;
}

// Compara a y b byte por byte, hasta la primera diferencia o hasta el final.
// Devuelve 0 si son iguales. Devuelve un número negativo si a va antes que b, y uno
// positivo si a va después. Una cadena que es el inicio de otra va antes.
// Comparen los bytes como unsigned char, para que el resultado no dependa de la máquina.
int my_strcmp(const char a[], const char b[]) {
    (void) a;
    (void) b;
    return 0;
}

// Convierte a mayúscula las letras de la 'a' a la 'z', en el mismo arreglo.
// Todos los demás bytes quedan igual.
void to_upper(char s[]) {
    (void) s;
}

// Devuelve 1 si s se lee igual byte por byte de izquierda a derecha y de derecha a
// izquierda, y 0 si no. Sin ninguna excepción: "Ana" no es palíndromo, porque
// 'A' y 'a' son bytes distintos. La cadena vacía sí lo es.
int is_palindrome(const char s[]) {
    (void) s;
    return 0;
}

// Igual que is_palindrome, pero ignora los espacios y no distingue entre mayúsculas
// y minúsculas de la 'a' a la 'z'. "Anita lava la tina" sí es palíndromo.
// s no se puede cambiar. Una cadena sin nada más que espacios sí es palíndromo.
int is_palindrome_text(const char s[]) {
    (void) s;
    return 0;
}

int main(void) {
    assert(my_strlen("hola") == 4);
    assert(my_strcmp("ana", "ana") == 0);

    char word[] = "hola";
    to_upper(word);
    assert(word[0] == 'H');

    assert(is_palindrome("reconocer") == 1);
    assert(is_palindrome_text("Anita lava la tina") == 1);

    printf("Todas las pruebas pasaron\n");
    return 0;
}
