# Semana 15: inteligencia artificial y ética. Se usa dentro del entorno del curso.
#
#   make           compila los programas de la clase en build/
#   make test      corre las pruebas de los ejemplos y de los apuntes
#   make test-lab  prueba su laboratorio (lab/suspect.c y lab/tests.c); falla hasta que lo terminen
#   make clean     borra lo generado
#
# Los programas de esta semana no son para escribirlos: sirven para seguir a mano
# las ideas del capítulo.
#
# El laboratorio usa varios archivos. Repartir un programa así se aprende en cursos
# posteriores: aquí lo hace make. Con -Dmain=student_main, el main de tests.c se
# compila con otro nombre, y run_checks.c corre cada grupo de pruebas por separado.
# Se enlazan dos versiones: con su suspect.c corregido y con suspect_original.c.

CC = gcc
CFLAGS = -Wall -Wextra -std=c17 -g -fsanitize=address,undefined
BUILD = build
PROGRAMS = spam_models neuron network next_token

.PHONY: all lab test test-lab clean

all: $(PROGRAMS:%=$(BUILD)/%)

$(BUILD)/%: %.c | $(BUILD)
	$(CC) $(CFLAGS) $< -o $@

$(BUILD) $(BUILD)/lab $(BUILD)/solution:
	mkdir -p $@

# Las funciones del original, con las pruebas del laboratorio (sirve para ver que los bugs existen).
$(BUILD)/check_original: check_suspect.c suspect_original.c | $(BUILD)
	$(CC) $(CFLAGS) check_suspect.c suspect_original.c -o $@

define LAB_RULES
$(BUILD)/$(1)/check_suspect: check_suspect.c $(1)/suspect.c | $(BUILD)/$(1)
	$(CC) $(CFLAGS) check_suspect.c $(1)/suspect.c -o $$@

$(BUILD)/$(1)/tests_fixed: run_checks.c $(1)/tests.c $(1)/suspect.c | $(BUILD)/$(1)
	$(CC) $(CFLAGS) -Dmain=student_main -c $(1)/tests.c -o $(BUILD)/$(1)/tests.o
	$(CC) $(CFLAGS) run_checks.c $(BUILD)/$(1)/tests.o $(1)/suspect.c -o $$@

$(BUILD)/$(1)/tests_original: run_checks.c $(1)/tests.c suspect_original.c | $(BUILD)/$(1)
	$(CC) $(CFLAGS) -Dmain=student_main -c $(1)/tests.c -o $(BUILD)/$(1)/tests.o
	$(CC) $(CFLAGS) run_checks.c $(BUILD)/$(1)/tests.o suspect_original.c -o $$@

$(BUILD)/$(1)/tests: $(1)/tests.c $(1)/suspect.c | $(BUILD)/$(1)
	$(CC) $(CFLAGS) $(1)/tests.c $(1)/suspect.c -o $$@
endef

$(eval $(call LAB_RULES,lab))
$(eval $(call LAB_RULES,solution))

LAB_FILES = check_suspect tests_fixed tests_original tests

lab: $(LAB_FILES:%=$(BUILD)/lab/%)

# Si existe solution/, también se comprueba la solución del laboratorio.
test: all $(BUILD)/check_original
	@if [ -d solution ]; then $(MAKE) --no-print-directory \
	  $(LAB_FILES:%=$(BUILD)/solution/%); fi
	python3 -m unittest discover -p 'test_*.py'

test-lab: all lab
	LAB_DIR=lab python3 -m unittest -v test_lab

clean:
	rm -rf $(BUILD) __pycache__
