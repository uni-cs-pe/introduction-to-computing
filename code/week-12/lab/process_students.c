// Laboratorio: procesar el archivo de estudiantes de principio a fin.
//
// El programa lee dos líneas de la entrada: el nombre del archivo de estudiantes y el
// nombre del archivo que debe crear. Por ejemplo:
//
//   printf 'estudiantes.txt\nbuild/aprobados.txt\n' | build/lab/process_students
//
// Cada línea del archivo tiene un nombre de una palabra y tres notas enteras:
//
//   Ana 14 9 17
//
// Escriban cada función según su comentario. Borren las líneas (void): solo están para
// que el archivo compile sin advertencias mientras tanto. No cambien el struct ni las
// constantes, ni el nombre o los parámetros de las funciones: las pruebas las llaman.
//
// Pruébenlo con make test-lab.
#include <stdio.h>

#define NAME_SIZE 20
#define N_GRADES 3
#define MAX_STUDENTS 50
#define PASS_GRADE 11
#define PATH_SIZE 128
#define LINE_SIZE 64
#define READ_END 0
#define READ_OK 1
#define READ_TOO_LONG 2

struct student {
    char name[NAME_SIZE];
    int grades[N_GRADES];
};

// Ya está hecha, y es la de la semana 10.
int remove_newline(char s[]) {
    for (int i = 0; s[i] != '\0'; i++) {
        if (s[i] == '\n') {
            s[i] = '\0';
            return 1;
        }
    }
    return 0;
}

// Lee una línea de file en line, sin el salto de línea. Devuelve:
//   READ_END       si no hay más líneas;
//   READ_OK        si la línea cupo, también si es la última y no tiene salto;
//   READ_TOO_LONG  si no cupo. En ese caso descarta el resto, hasta el final de la línea.
// Una línea con size - 1 bytes justos cabe.
int read_line(FILE *file, char line[], int size) {
    (void) file;
    (void) line;
    (void) size;
    return READ_END;
}

// Si la línea es válida, guarda el estudiante en list[pos] y devuelve 1. Si no, devuelve 0.
// Es válida si tiene exactamente un nombre y tres enteros, cada uno entre 0 y 20.
// Una línea con algo de más no es válida. Una línea vacía tampoco.
int parse_student(const char line[], struct student list[], int pos) {
    (void) line;
    (void) list;
    (void) pos;
    return 0;
}

// Devuelve el promedio de las notas, con decimales.
double average(struct student s) {
    (void) s;
    return 0.0;
}

// Devuelve 1 si el promedio es PASS_GRADE o más, y 0 si no.
int is_passed(struct student s) {
    (void) s;
    return 0;
}

// Abre el archivo y guarda sus estudiantes en list. Devuelve cuántos guardó.
//   - Si no puede abrirlo, avisa con perror(path) y devuelve -1.
//   - Por cada línea mal formada o que no cabe, escribe en stderr
//     "Línea N: mal formada, se omite" (la primera línea es la 1) y sigue.
//   - Si hay más líneas que capacity, escribe en stderr
//     "Demasiados estudiantes: solo se leen N", con N igual a capacity, y deja de leer.
//     Con capacity líneas justas, no avisa.
//   - Siempre cierra el archivo.
int read_students(const char path[], struct student list[], int capacity) {
    (void) path;
    (void) list;
    (void) capacity;
    return -1;
}

// Crea el archivo path, con una línea por cada aprobado: el nombre, un espacio y el
// promedio con 2 decimales. Por ejemplo, "Ana 13.33". Devuelve cuántos aprobados escribió.
// Si no puede abrirlo o cerrarlo, avisa con perror(path) y devuelve -1.
int write_passed(const char path[], const struct student list[], int n) {
    (void) path;
    (void) list;
    (void) n;
    return -1;
}

// main debe seguir estos pasos, en este orden:
//   1. Leer los dos nombres. Si falta alguno, escribir en stderr "Faltan los nombres de
//      los archivos" y devolver 1.
//   2. Leer los estudiantes. Si no se pudo abrir el archivo, devolver 1.
//   3. Si no quedó ningún estudiante, escribir en stderr "<archivo>: no hay estudiantes",
//      con el nombre del archivo de entrada, y devolver 1. No se crea el archivo de salida.
//   4. Escribir los aprobados. Si no se pudo, devolver 1.
//   5. Escribir en la salida "Leídos: N. Aprobados: M." y devolver 0.
int main(void) {
    return 1;
}
