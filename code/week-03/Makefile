# Semana 3: bits y representación de datos. Se usa dentro del entorno del curso.
#
#   make           compila los programas de la clase en build/
#   make lab       compila su laboratorio (lab/*.c) en build/lab/
#   make test      corre las pruebas de los ejemplos y, si existe solution/, las del laboratorio
#   make test-lab  prueba su laboratorio (lab/); falla hasta que lo terminen
#   make clean     borra lo generado

CC = gcc
CFLAGS = -Wall -Wextra -std=c17 -g -fsanitize=address,undefined
LDLIBS = -lm
BUILD = build
PROGRAMS = to_binary from_binary bases sizes twos_complement overflow unsigned_wrap \
           float_sum fraction_to_binary float_limits compare_doubles money char_codes char_sign \
           read_bytes utf8_two_bytes
LAB_PROGRAMS = hex_202 int_overflow float_print

.PHONY: all lab test test-lab clean

all: $(PROGRAMS:%=$(BUILD)/%)

$(BUILD)/%: %.c | $(BUILD)
	$(CC) $(CFLAGS) -o $@ $< $(LDLIBS)

$(BUILD)/lab/%: lab/%.c | $(BUILD)/lab
	$(CC) $(CFLAGS) -o $@ $< $(LDLIBS)

$(BUILD)/solution/%: solution/%.c | $(BUILD)/solution
	$(CC) $(CFLAGS) -o $@ $< $(LDLIBS)

$(BUILD) $(BUILD)/lab $(BUILD)/solution:
	mkdir -p $@

lab: $(LAB_PROGRAMS:%=$(BUILD)/lab/%)

# Si existe solution/, también se comprueba la solución del laboratorio.
test: all
	python3 -m unittest -v test_examples
	@if [ -d solution ]; then \
	  $(MAKE) --no-print-directory $(LAB_PROGRAMS:%=$(BUILD)/solution/%) && \
	  LAB_DIR=solution python3 -m unittest -v test_lab; fi

test-lab: lab
	LAB_DIR=lab python3 -m unittest -v test_lab

clean:
	rm -rf $(BUILD) __pycache__
