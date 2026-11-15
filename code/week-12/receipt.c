// Lee una lista de compras y escribe una boleta. Un programa de principio a fin.
// Cada línea de la lista tiene: producto precio cantidad.
#include <stdio.h>

#define NAME_SIZE 20
#define PATH_SIZE 128
#define LINE_SIZE 64
#define MAX_ITEMS 20
#define READ_END 0
#define READ_OK 1
#define READ_TOO_LONG 2

struct item {
    char name[NAME_SIZE];
    double price;
    int quantity;
};

int remove_newline(char s[]) {
    for (int i = 0; s[i] != '\0'; i++) {
        if (s[i] == '\n') {
            s[i] = '\0';
            return 1;
        }
    }
    return 0;
}

int read_line(FILE *file, char line[], int size) {
    if (fgets(line, size, file) == NULL) {
        return READ_END;
    }
    if (remove_newline(line)) {
        return READ_OK;
    }
    int c = fgetc(file);
    if (c == '\n' || c == EOF) {
        return READ_OK;
    }
    while (c != '\n' && c != EOF) {
        c = fgetc(file);
    }
    return READ_TOO_LONG;
}

// Si la línea es válida, guarda el producto en items[pos] y devuelve 1. Si no, devuelve 0.
int parse_item(const char line[], struct item items[], int pos) {
    struct item it;
    char extra[2];
    int fields = sscanf(line, "%19s %lf %d %1s", it.name, &it.price, &it.quantity, extra);
    if (fields != 3 || it.price < 0 || it.quantity <= 0) {
        return 0;
    }
    items[pos] = it;
    return 1;
}

// Devuelve cuántos productos leyó, o -1 si no pudo abrir el archivo.
int read_items(const char path[], struct item items[], int capacity) {
    FILE *file = fopen(path, "r");
    if (file == NULL) {
        perror(path);
        return -1;
    }

    char line[LINE_SIZE];
    int count = 0;
    int number = 0;
    int result = read_line(file, line, LINE_SIZE);
    while (result != READ_END) {
        number++;
        if (count == capacity) {
            fprintf(stderr, "Demasiados productos: solo se leen %d\n", capacity);
            break;
        }
        if (result == READ_OK && parse_item(line, items, count)) {
            count++;
        } else {
            fprintf(stderr, "Línea %d: mal formada, se omite\n", number);
        }
        result = read_line(file, line, LINE_SIZE);
    }
    fclose(file);
    return count;
}

// Escribe la boleta. Devuelve 1 si pudo, 0 si no.
int write_receipt(const char path[], const struct item items[], int n) {
    FILE *file = fopen(path, "w");
    if (file == NULL) {
        perror(path);
        return 0;
    }

    double total = 0.0;
    for (int i = 0; i < n; i++) {
        double subtotal = items[i].price * items[i].quantity;
        fprintf(file, "%s %d x %.2f = %.2f\n", items[i].name, items[i].quantity,
                items[i].price, subtotal);
        total = total + subtotal;
    }
    fprintf(file, "Total: S/ %.2f\n", total);

    if (fclose(file) != 0) {
        perror(path);
        return 0;
    }
    return 1;
}

int main(void) {
    char input[PATH_SIZE];
    char output[PATH_SIZE];
    if (fgets(input, PATH_SIZE, stdin) == NULL || fgets(output, PATH_SIZE, stdin) == NULL) {
        fprintf(stderr, "Faltan los nombres de los archivos\n");
        return 1;
    }
    remove_newline(input);
    remove_newline(output);

    struct item items[MAX_ITEMS];
    int n = read_items(input, items, MAX_ITEMS);
    if (n < 0) {
        return 1;
    }
    if (n == 0) {
        fprintf(stderr, "%s: no hay productos\n", input);
        return 1;
    }
    if (!write_receipt(output, items, n)) {
        return 1;
    }
    printf("Productos: %d\n", n);
    return 0;
}
