# Semana 10: arreglos en funciones y cadenas. Se usa dentro del entorno del curso.
#
#   make           compila los programas de la clase en build/
#   make test      corre las pruebas de los ejemplos y de los apuntes
#   make test-lab  prueba su laboratorio (lab/*.c); falla hasta que lo terminen
#   make clean     borra lo generado
#
# Los programas de errors/ tienen errores a propósito. No se compilan con make:
# los compilan las pruebas, y ustedes, con los comandos de los apuntes.
#
# check_strings.c es parte de las pruebas: llama a las funciones de my_strings.c.
# Para enlazarlos, el main de my_strings.c se compila con otro nombre. Se compila con
# -fsigned-char para que make test-lab dé lo mismo en todas las máquinas.

CC = gcc
CFLAGS = -Wall -Wextra -std=c17 -g -fsanitize=address,undefined
BUILD = build
PROGRAMS = sum_array bonus same_address const_param vector string_bytes cut_string \
           my_strlen count_lowercase read_word read_line read_name age_name copy_text

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

$(BUILD)/lab/check_strings: check_strings.c lab/my_strings.c | $(BUILD)/lab
	$(CC) $(CFLAGS) -fsigned-char -Dmain=student_main -c lab/my_strings.c -o $(BUILD)/lab/my_strings.o
	$(CC) $(CFLAGS) -fsigned-char check_strings.c $(BUILD)/lab/my_strings.o -o $@

$(BUILD)/solution/check_strings: check_strings.c solution/my_strings.c | $(BUILD)/solution
	$(CC) $(CFLAGS) -fsigned-char -Dmain=student_main -c solution/my_strings.c -o $(BUILD)/solution/my_strings.o
	$(CC) $(CFLAGS) -fsigned-char check_strings.c $(BUILD)/solution/my_strings.o -o $@

LAB_FILES = my_strings greet check_strings

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
