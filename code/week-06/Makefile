# Semana 6: ciclos anidados y números aleatorios. Se usa dentro del entorno del curso.
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
PROGRAMS = rectangle times_table count_runs staircase divisors toy_generator \
           rand_max seed time_seed range die_counts dice_exact dice_seven
LAB_PROGRAMS = triangle primes dice_estimate

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
