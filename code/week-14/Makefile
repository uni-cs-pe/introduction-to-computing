# Semana 14: internet y una mirada a Python. Se usa dentro del entorno del curso.
#
#   make           compila los programas de la clase en build/
#   make test      corre las pruebas de los ejemplos y de los apuntes
#   make test-lab  prueba su laboratorio (lab/http_status.c); falla hasta que lo terminen
#   make cert      crea un certificado de prueba para python3 server.py --tls
#   make clean     borra lo generado
#
# build/primes y build/selection_sort llevan sanitizers, y por eso son lentos. Para medir
# tiempos están build/primes_fast y build/selection_sort_fast: -O2 y sin sanitizers.
# Los programas de errors/ se compilan a mano, con los comandos de los apuntes.

CC = gcc
CFLAGS = -Wall -Wextra -std=c17 -g -fsanitize=address,undefined
FAST = -Wall -Wextra -std=c17 -O2
BUILD = build
PROGRAMS = primes division text_length factorial selection_sort

.PHONY: all lab test test-lab cert clean

all: $(PROGRAMS:%=$(BUILD)/%) $(BUILD)/primes_fast $(BUILD)/selection_sort_fast

$(BUILD)/%: %.c | $(BUILD)
	$(CC) $(CFLAGS) $< -o $@

$(BUILD)/%_fast: %.c | $(BUILD)
	$(CC) $(FAST) $< -o $@

$(BUILD) $(BUILD)/lab $(BUILD)/solution:
	mkdir -p $@

$(BUILD)/lab/% : lab/%.c | $(BUILD)/lab
	$(CC) $(CFLAGS) $< -o $@

$(BUILD)/solution/% : solution/%.c | $(BUILD)/solution
	$(CC) $(CFLAGS) $< -o $@

lab: $(BUILD)/lab/http_status

# El certificado solo sirve para las pruebas en esta computadora.
cert: | $(BUILD)
	openssl req -x509 -newkey rsa:2048 -nodes -days 30 -subj "/CN=localhost" \
	  -addext "subjectAltName=DNS:localhost" \
	  -keyout $(BUILD)/key.pem -out $(BUILD)/cert.pem 2> /dev/null

# Si existe solution/, también se comprueba la solución del laboratorio.
test: all
	@if [ -d solution ]; then $(MAKE) --no-print-directory $(BUILD)/solution/http_status; fi
	python3 -m unittest discover -p 'test_*.py'

test-lab: all lab
	LAB_DIR=lab python3 -m unittest -v test_lab

clean:
	rm -rf $(BUILD) __pycache__
