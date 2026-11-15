# Semana 2: variables y programas secuenciales. Se usa dentro del entorno del
# curso (Codespaces o env/run.sh).
#
#   make           compila los ejemplos de los apuntes en build/
#   make test      compila y prueba los ejemplos, y la solución si existe solution/
#   make test-lab  prueba su laboratorio (lab/); falla hasta que lo terminen
#   make clean     borra lo generado
#
# Los programas de broken/ tienen errores a propósito: make no los compila.
# Los apuntes muestran qué dice gcc sobre cada uno.

CC = gcc
CFLAGS = -Wall -Wextra -std=c17 -g -fsanitize=address,undefined
LDLIBS = -lm
BUILD = build
PROGRAMS = balance not_a_formula swap_values sizes arithmetic division \
           conversions char_codes printf_formats read_grade final_grade \
           final_grade_bug read_check leftover char_trap char_fixed \
           igv_price change math_demo diagonal compound_interest \
           division_by_zero double_by_zero
LAB_PROGRAMS = celsius predict time_split type_sizes

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
	python3 -m unittest -v test_examples test_lab

test-lab: all lab
	LAB_DIR=lab python3 -m unittest -v test_lab

clean:
	rm -rf $(BUILD) __pycache__
