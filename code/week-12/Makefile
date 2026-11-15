# Semana 12: struct y archivos. Se usa dentro del entorno del curso.
#
#   make           compila los programas de la clase en build/
#   make test      corre las pruebas de los ejemplos y de los apuntes
#   make test-lab  prueba su laboratorio (lab/process_students.c); falla hasta que lo terminen
#   make clean     borra lo generado
#
# Los programas de errors/ tienen errores a propósito. No se compilan con make:
# los compilan las pruebas, y ustedes, con los comandos de los apuntes.
#
# check_students.c es parte de las pruebas: llama a las funciones de process_students.c.
# Para enlazarlos, el main de process_students.c se compila con otro nombre.

CC = gcc
CFLAGS = -Wall -Wextra -std=c17 -g -fsanitize=address,undefined
BUILD = build
PROGRAMS = first_struct struct_copy struct_param struct_array struct_size show_file \
           write_note append_note parse_fields long_line receipt

.PHONY: all lab test test-lab clean

all: $(PROGRAMS:%=$(BUILD)/%)

$(BUILD)/%: %.c | $(BUILD)
	$(CC) $(CFLAGS) $< -o $@

$(BUILD) $(BUILD)/lab $(BUILD)/solution:
	mkdir -p $@

$(BUILD)/lab/process_students: lab/process_students.c | $(BUILD)/lab
	$(CC) $(CFLAGS) $< -o $@

$(BUILD)/solution/process_students: solution/process_students.c | $(BUILD)/solution
	$(CC) $(CFLAGS) $< -o $@

$(BUILD)/lab/check_students: check_students.c lab/process_students.c | $(BUILD)/lab
	$(CC) $(CFLAGS) -Dmain=student_main -c lab/process_students.c -o $(BUILD)/lab/process_students.o
	$(CC) $(CFLAGS) check_students.c $(BUILD)/lab/process_students.o -o $@

$(BUILD)/solution/check_students: check_students.c solution/process_students.c | $(BUILD)/solution
	$(CC) $(CFLAGS) -Dmain=student_main -c solution/process_students.c -o $(BUILD)/solution/process_students.o
	$(CC) $(CFLAGS) check_students.c $(BUILD)/solution/process_students.o -o $@

LAB_FILES = process_students check_students

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
