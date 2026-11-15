# Semana 4: decisiones y lógica. Se usa dentro del entorno del curso.
#
#   make           compila los programas de la clase en build/
#   make test      corre las pruebas de los ejemplos y de los apuntes
#   make test-lab  prueba su laboratorio (lab/*.c); falla hasta que lo terminen
#   make clean     borra lo generado
#
# Los programas de errors/ tienen errores a propósito. No se compilan con make:
# los compilan las pruebas, y ustedes, con los comandos de los apuntes.

CC = gcc
CFLAGS = -Wall -Wextra -std=c17 -g -fsanitize=address,undefined
LDLIBS = -lm
BUILD = build
PROGRAMS = discount parity max_of_three mention relational truthy precedence \
           truth_table de_morgan short_circuit read_in_range compare_double \
           month_days combo vowel gates full_adder adder4
LAB_PROGRAMS = grade leap_year calculator

.PHONY: all lab test test-lab clean

all: $(PROGRAMS:%=$(BUILD)/%)

$(BUILD)/%: %.c | $(BUILD)
	$(CC) $(CFLAGS) $< -o $@ $(LDLIBS)

$(BUILD)/lab/%: lab/%.c | $(BUILD)/lab
	$(CC) $(CFLAGS) $< -o $@ $(LDLIBS)

$(BUILD)/solution/%: solution/%.c | $(BUILD)/solution
	$(CC) $(CFLAGS) $< -o $@ $(LDLIBS)

$(BUILD) $(BUILD)/lab $(BUILD)/solution:
	mkdir -p $@

lab: $(LAB_PROGRAMS:%=$(BUILD)/lab/%)

# Si existe solution/, también se comprueba la solución del laboratorio.
test: all
	@if [ -d solution ]; then $(MAKE) --no-print-directory \
	  $(LAB_PROGRAMS:%=$(BUILD)/solution/%); fi
	python3 -m unittest discover -p 'test_*.py'

test-lab: all lab
	LAB_DIR=lab python3 -m unittest -v test_lab

clean:
	rm -rf $(BUILD) __pycache__
