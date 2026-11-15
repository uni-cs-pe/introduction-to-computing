// Lee una respuesta HTTP de la entrada y resume sus partes.
//   curl -si http://127.0.0.1:8014/saludo | build/lab/http_status
//
// Completen las partes marcadas con TAREA. Los apuntes explican cada una.
#include <stdio.h>
#include <string.h>

#define LINE_SIZE 256

// Devuelve el código de una línea como "HTTP/1.1 404 Not Found", o -1 si no tiene esa forma.
// Tiene esa forma si empieza con HTTP/ y una versión, y le sigue un número entre 100 y 599.
int parse_status(const char line[]) {
    // TAREA: sepárenla con sscanf y revisen lo que devuelve. Pongan límite a la versión.
    (void) line;
    return -1;
}

// Devuelve 1 si la línea está vacía. HTTP termina las líneas con \r\n; se acepta también \n.
int is_blank_line(const char line[]) {
    // TAREA: comparen con strcmp.
    (void) line;
    return 0;
}

int main(void) {
    char line[LINE_SIZE];
    if (fgets(line, LINE_SIZE, stdin) == NULL) {
        printf("La entrada está vacía\n");
        return 1;
    }
    int code = parse_status(line);
    if (code == -1) {
        printf("No es una respuesta HTTP\n");
        return 1;
    }

    // TAREA: cuenten los encabezados. Terminan en la primera línea vacía, que no se cuenta.
    int headers = 0;

    // TAREA: sumen los bytes del cuerpo, que es todo lo que queda.
    int body_bytes = 0;

    printf("código: %d\n", code);
    printf("clase: %dxx\n", code / 100);
    printf("encabezados: %d\n", headers);
    printf("cuerpo: %d bytes\n", body_bytes);
    return 0;
}
