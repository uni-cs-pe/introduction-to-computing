// Laboratorio, parte 1: tres funciones sospechosas.
//
// Estas funciones se escribieron para esta actividad y tienen bugs a propósito: una
// por función. Compilan sin advertencias y pasan la prueba de lab/tests.c. Es lo que
// puede pasarles con el código de cualquiera, o con la respuesta de un asistente.
//
// No las corrijan todavía. Primero escriban en lab/tests.c una prueba que falle.
// Después corrijan aquí la función y comprueben que la prueba pasa.
//
// Pruébenlo con make test-lab.

// Devuelve 1 si n es primo y 0 si no.
int is_prime(int n) {
    if (n < 2) {
        return 0;
    }
    for (int i = 2; i * i < n; i++) {
        if (n % i == 0) {
            return 0;
        }
    }
    return 1;
}

// Devuelve el mayor elemento de a. n debe ser al menos 1.
int max_of_array(const int a[], int n) {
    int best = 0;
    for (int i = 0; i < n; i++) {
        if (a[i] > best) {
            best = a[i];
        }
    }
    return best;
}

// Copia src en dest, que tiene size bytes. Si no cabe, copia lo que quepa.
// dest siempre termina en '\0'. size debe ser al menos 1.
void copy_text(char dest[], const char src[], int size) {
    int i = 0;
    while (src[i] != '\0' && i < size) {
        dest[i] = src[i];
        i++;
    }
    dest[i] = '\0';
}
