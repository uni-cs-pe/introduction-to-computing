# Semana 11: biblioteca de cadenas y matrices. Se usa dentro del entorno del curso.
#
#   make           compila los programas de la clase en build/
#   make test      corre las pruebas de los ejemplos y de los apuntes
#   make test-lab  prueba su laboratorio (lab/*.c); falla hasta que lo terminen
#   make clean     borra lo generado
#
# Los programas de errors/ tienen errores a propósito. No se compilan con make:
# los compilan las pruebas, y ustedes, con los comandos de los apuntes.
#
# check_lab.c es parte de las pruebas: llama a las funciones de words.c y grades.c.
# Para enlazarlos, el main de cada archivo se compila con otro nombre.

CC = gcc
CFLAGS = -Wall -Wextra -std=c17 -g -fsanitize=address,undefined
BUILD = build
PROGRAMS = lengths compare strncpy_bytes safe_copy append find_text matrix_layout \
           grades_table matrix_param names matrix_add

.PHONY: all lab test test-lab clean

all: $(PROGRAMS:%=$(BUILD)/%)

$(BUILD)/%: %.c | $(BUILD)
	$(CC) $(CFLAGS) $< -o $@

$(BUILD) $(BUILD)/lab $(BUILD)/solution:
	mkdir -p $@

$(BUILD)/lab/% : lab/%.c | $(BUILD)/lab
	$(CC) $(CFLAGS) $< -o $@

$(BUILD)/solution/% : solution/%.c | $(BUILD)/solution
	$(CC) $(CFLAGS) $< -o $@

$(BUILD)/lab/check_lab: check_lab.c lab/words.c lab/grades.c | $(BUILD)/lab
	$(CC) $(CFLAGS) -Dmain=words_main -c lab/words.c -o $(BUILD)/lab/words.o
	$(CC) $(CFLAGS) -Dmain=grades_main -c lab/grades.c -o $(BUILD)/lab/grades.o
	$(CC) $(CFLAGS) check_lab.c $(BUILD)/lab/words.o $(BUILD)/lab/grades.o -o $@

$(BUILD)/solution/check_lab: check_lab.c solution/words.c solution/grades.c | $(BUILD)/solution
	$(CC) $(CFLAGS) -Dmain=words_main -c solution/words.c -o $(BUILD)/solution/words.o
	$(CC) $(CFLAGS) -Dmain=grades_main -c solution/grades.c -o $(BUILD)/solution/grades.o
	$(CC) $(CFLAGS) check_lab.c $(BUILD)/solution/words.o $(BUILD)/solution/grades.o -o $@

LAB_FILES = words grades check_lab

lab: $(LAB_FILES:%=$(BUILD)/lab/%)

# Si existe solution/, también se comprueba la solución del laboratorio.
test: all
	@if [ -d solution ]; then $(MAKE) --no-print-directory \
	  $(LAB_FILES:%=$(BUILD)/solution/%); fi
	python3 -m unittest discover -p 'test_*.py'

test-lab: all lab
	LAB_DIR=lab python3 -m unittest -v test_lab

clean:
	rm -rf $(BUILD) __pycache__
