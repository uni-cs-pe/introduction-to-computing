# Semana 1: qué es computar. Se usa dentro del entorno del curso.
#
#   make           compila los programas de la clase en build/
#   make test      corre las pruebas de la semana y comprueba la solución del laboratorio
#   make test-lab  prueba su laboratorio (lab/); falla hasta que lo terminen
#   make clean     borra lo generado
#
# Los programas de errors/ tienen errores a propósito: no se compilan con `make`.
# Las pruebas los compilan una por una y revisan lo que dice gcc.

CC = gcc
CFLAGS = -Wall -Wextra -std=c17 -g -fsanitize=address,undefined
BUILD = build
PROGRAMS = hola change_780 exit_code

.PHONY: all test test-lab clean

all: $(PROGRAMS:%=$(BUILD)/%)

$(BUILD)/%: %.c | $(BUILD)
	$(CC) $(CFLAGS) $< -o $@

$(BUILD):
	mkdir -p $@

test: all
	python3 -m unittest test_examples test_algorithms
	@if [ -d solution ]; then LAB_DIR=solution python3 -m unittest test_lab; fi

test-lab:
	LAB_DIR=lab python3 -m unittest test_lab

clean:
	rm -rf $(BUILD) __pycache__
