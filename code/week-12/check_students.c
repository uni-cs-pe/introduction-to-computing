// Parte de las pruebas del laboratorio: test_lab.py llama con esto a sus funciones.
// No hace falta leerlo. Usa argumentos de la línea de comandos, que no vemos en el curso.
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define NAME_SIZE 20
#define N_GRADES 3
#define CAPACITY 4
#define READ_END 0
#define READ_OK 1
#define READ_TOO_LONG 2

struct student {
    char name[NAME_SIZE];
    int grades[N_GRADES];
};

int read_line(FILE *file, char line[], int size);
int parse_student(const char line[], struct student list[], int pos);
double average(struct student s);
int is_passed(struct student s);
int read_students(const char path[], struct student list[], int capacity);
int write_passed(const char path[], const struct student list[], int n);

static void print_student(struct student s) {
    printf("%s %d %d %d\n", s.name, s.grades[0], s.grades[1], s.grades[2]);
}

// Escribe qué devuelve read_line con un buffer de 8 bytes, línea por línea.
static int check_read_line(const char path[]) {
    FILE *file = fopen(path, "r");
    if (file == NULL) {
        return 2;
    }
    char line[8];
    for (int guard = 0; guard < 100; guard++) {
        int result = read_line(file, line, 8);
        if (result == READ_END) {
            printf("end\n");
            break;
        }
        printf(result == READ_OK ? "ok \"%s\"\n" : "long\n", line);
    }
    fclose(file);
    return 0;
}

// Lee el archivo varias veces. Las pruebas bajan el límite de archivos abiertos: si
// read_students no cierra el archivo, fopen termina fallando.
static int check_many_reads(const char path[]) {
    struct student list[CAPACITY];
    int total = 0;
    for (int i = 0; i < 200; i++) {
        int n = read_students(path, list, CAPACITY);
        if (n < 0) {
            printf("falló en la lectura %d\n", i);
            return 1;
        }
        total = total + n;
    }
    printf("%d\n", total);
    return 0;
}

// Llama a write_passed y mira el archivo sin terminar el programa. Si write_passed no
// llama a fclose, lo escrito puede no estar todavía en el archivo.
static int check_write(const char path[]) {
    struct student list[3] = {
        {"Ana", {14, 9, 17}},
        {"Bruno", {8, 10, 11}},
        {"Carla", {11, 11, 11}},
    };
    printf("%d\n", write_passed(path, list, 3));
    FILE *file = fopen(path, "r");
    if (file == NULL) {
        return 0;
    }
    char line[64];
    while (fgets(line, 64, file) != NULL) {
        printf("%s", line);
    }
    fclose(file);
    return 0;
}

int main(int argc, char *argv[]) {
    if (argc < 3) {
        return 2;
    }
    const char *op = argv[1];
    if (strcmp(op, "parse") == 0) {
        // Con centinelas alrededor: guardar fuera de list[pos] se nota.
        struct student list[3] = {{"antes", {1, 1, 1}}, {"medio", {2, 2, 2}}, {"despues", {3, 3, 3}}};
        int ok = parse_student(argv[2], list, 1);
        printf("%d\n", ok);
        if (ok) {
            print_student(list[1]);
        }
        if (strcmp(list[0].name, "antes") != 0 || strcmp(list[2].name, "despues") != 0) {
            printf("cambió otra posición\n");
        }
    } else if (strcmp(op, "average") == 0 || strcmp(op, "passed") == 0) {
        struct student s = {"x", {atoi(argv[2]), atoi(argv[3]), atoi(argv[4])}};
        if (op[0] == 'a') {
            printf("%.4f\n", average(s));
        } else {
            printf("%d\n", is_passed(s));
        }
    } else if (strcmp(op, "read") == 0) {
        struct student list[CAPACITY];
        int n = read_students(argv[2], list, CAPACITY);
        printf("%d\n", n);
        for (int i = 0; i < n; i++) {
            print_student(list[i]);
        }
    } else if (strcmp(op, "line") == 0) {
        return check_read_line(argv[2]);
    } else if (strcmp(op, "many") == 0) {
        return check_many_reads(argv[2]);
    } else if (strcmp(op, "write") == 0) {
        return check_write(argv[2]);
    } else {
        return 2;
    }
    return 0;
}
