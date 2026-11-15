# Semana 13: búsqueda, ordenamiento y eficiencia. Se usa dentro del entorno del curso.
#
#   make           compila los programas de la clase en build/
#   make test      corre las pruebas de los ejemplos y de los apuntes
#   make test-lab  prueba su laboratorio (lab/*.c); falla hasta que lo terminen
#   make measure   mide su lab/sorting.c, con -O2 y sin sanitizers
#   make clean     borra lo generado
#
# Para medir tiempos se compila aparte, en build/fast/, con -O2 y sin sanitizers: los
# sanitizers hacen más lento el programa, y sin optimizar se mediría otra cosa.
#
# Los programas de errors/ tienen errores a propósito. No se compilan con make:
# los compilan las pruebas, y ustedes, con los comandos de los apuntes.
#
# check_searching.c y check_sorting.c son parte de las pruebas: llaman a las funciones
# de su laboratorio. Para enlazarlos, el main del laboratorio se compila con otro nombre.

CC = gcc
BASEFLAGS = -Wall -Wextra -std=c17
CFLAGS = $(BASEFLAGS) -g -fsanitize=address,undefined
FASTFLAGS = $(BASEFLAGS) -O2
BUILD = build
PROGRAMS = linear_search binary_search binary_trace count_search growth selection_sort \
           qsort_demo factorial
FAST_PROGRAMS = sort_times sort_then_search

.PHONY: all lab test test-lab measure clean

all: $(PROGRAMS:%=$(BUILD)/%) $(FAST_PROGRAMS:%=$(BUILD)/fast/%)

$(BUILD)/%: %.c | $(BUILD)
	$(CC) $(CFLAGS) $< -o $@

$(BUILD)/fast/%: %.c | $(BUILD)/fast
	$(CC) $(FASTFLAGS) $< -o $@

$(BUILD) $(BUILD)/fast $(BUILD)/lab $(BUILD)/solution:
	mkdir -p $@

$(BUILD)/lab/%: lab/%.c | $(BUILD)/lab
	$(CC) $(CFLAGS) $< -o $@

$(BUILD)/solution/%: solution/%.c | $(BUILD)/solution
	$(CC) $(CFLAGS) $< -o $@

# Las mismas reglas para las dos carpetas: $(1) es lab o solution.
define CHECKS
$(BUILD)/$(1)/check_searching: check_searching.c $(1)/searching.c | $(BUILD)/$(1)
	$(CC) $(CFLAGS) -Dmain=student_main -c $(1)/searching.c -o $(BUILD)/$(1)/searching.o
	$(CC) $(CFLAGS) check_searching.c $(BUILD)/$(1)/searching.o -o $$@

$(BUILD)/$(1)/check_sorting: check_sorting.c $(1)/sorting.c | $(BUILD)/$(1)
	$(CC) $(CFLAGS) -Dmain=student_main -c $(1)/sorting.c -o $(BUILD)/$(1)/sorting.o
	$(CC) $(CFLAGS) check_sorting.c $(BUILD)/$(1)/sorting.o -o $$@

$(BUILD)/$(1)/check_sorting_fast: check_sorting.c $(1)/sorting.c | $(BUILD)/$(1)
	$(CC) $(FASTFLAGS) -Dmain=student_main -c $(1)/sorting.c -o $(BUILD)/$(1)/sorting_fast.o
	$(CC) $(FASTFLAGS) check_sorting.c $(BUILD)/$(1)/sorting_fast.o -o $$@

$(BUILD)/$(1)/sorting_fast: $(1)/sorting.c | $(BUILD)/$(1)
	$(CC) $(FASTFLAGS) $$< -o $$@
endef
$(eval $(call CHECKS,lab))
$(eval $(call CHECKS,solution))

LAB_FILES = searching sorting check_searching check_sorting check_sorting_fast

lab: $(LAB_FILES:%=$(BUILD)/lab/%)

# Si existe solution/, también se comprueba la solución del laboratorio.
test: all
	@if [ -d solution ]; then $(MAKE) --no-print-directory \
	  $(LAB_FILES:%=$(BUILD)/solution/%); fi
	python3 -m unittest discover -p 'test_*.py'

test-lab: all lab
	LAB_DIR=lab python3 -m unittest -v test_lab

measure: $(BUILD)/lab/sorting_fast
	@echo "N, segundos de selección, segundos de qsort:"
	@echo 10000 20000 40000 80000 | $(BUILD)/lab/sorting_fast

clean:
	rm -rf $(BUILD) __pycache__
