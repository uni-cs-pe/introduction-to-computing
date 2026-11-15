"""Comprueba lo que los apuntes afirman sobre los programas de la semana 14."""
import pathlib
import socket
import subprocess
import sys
import tempfile
import unittest

from running_server import HERE, free_port, tool, web_server

BUILD = HERE / "build"
FLAGS = ["-Wall", "-Wextra", "-std=c17"]
SANITIZE = ["-g", "-fsanitize=address,undefined"]


def execute(command, stdin=""):
    done = subprocess.run(
        command, input=stdin, cwd=HERE, encoding="utf-8", errors="replace",
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=120,
    )
    return done.stdout, done.returncode


def run_c(program, stdin=""):
    return execute([str(BUILD / program)], stdin)


def run_python(script, stdin=""):
    return execute([sys.executable, script], stdin)


def build(source, *extra):
    out = pathlib.Path(tempfile.mkdtemp()) / pathlib.Path(source).stem
    messages, code = execute(["gcc", *FLAGS, *extra, source, "-o", str(out)])
    return messages, code, out


class LateError(unittest.TestCase):
    def test_python_only_finds_it_when_the_line_runs(self):
        self.assertEqual(run_python("errors/late_error.py", "5\n"), ("positivo\n", 0))
        output, code = run_python("errors/late_error.py", "-1\n")
        self.assertEqual(code, 1)
        self.assertIn("TypeError", output)


class CleanCode(unittest.TestCase):
    def test_c_has_no_warnings(self):
        for source in sorted(HERE.glob("*.c")) + sorted((HERE / "errors").glob("*.c")):
            with self.subTest(source=source.name):
                messages, code, _ = build(str(source.relative_to(HERE)))
                self.assertEqual((messages, code), ("", 0))


class PrimesInBothLanguages(unittest.TestCase):
    KNOWN = {-5: 0, 0: 0, 1: 0, 2: 1, 3: 2, 4: 2, 10: 4, 48: 15, 49: 15, 100: 25, 1000: 168,
             10000: 1229}

    def test_both_count_the_known_number_of_primes(self):
        for limit, count in self.KNOWN.items():
            expected = (f"Hay {count} primos hasta {limit}\n", 0)
            with self.subTest(limit=limit):
                self.assertEqual(run_c("primes", f"{limit}\n"), expected)
                self.assertEqual(run_python("primes.py", f"{limit}\n"), expected)

    def test_the_timing_input_gives_the_count_in_the_notes(self):
        self.assertEqual(run_c("primes_fast", (HERE / "limit.txt").read_text()),
                         ("Hay 78498 primos hasta 1000000\n", 0))

    def test_invalid_input(self):
        self.assertEqual(run_c("primes", "abc\n"), ("Entrada inválida\n", 1))
        output, code = run_python("primes.py", "abc\n")
        self.assertEqual(code, 1)
        self.assertIn("ValueError", output)


class Differences(unittest.TestCase):
    def test_division(self):
        self.assertEqual(run_c("division"), ("3\n3.5\n", 0))
        self.assertEqual(run_python("division.py"), ("3.5\n3\n", 0))

    def test_text_length(self):
        self.assertEqual(run_c("text_length"), ("4\n", 0))
        self.assertEqual(run_python("text_length.py"), ("3\n4\n", 0))

    def test_factorial_in_c_overflows_at_13(self):
        self.assertEqual(run_c("factorial", "12\n"), ("12! = 479001600\n", 0))
        output, _ = run_c("factorial", "13\n")
        self.assertIn("signed integer overflow", output)

    def test_factorial_in_python_is_exact(self):
        self.assertEqual(run_python("factorial.py", "13\n"), ("13! = 6227020800\n", 0))
        self.assertEqual(run_python("factorial.py", "25\n"),
                         ("25! = 15511210043330985984000000\n", 0))

    def test_python_limits_printing_very_long_integers(self):
        output, code = run_python("factorial.py", "2000\n")
        self.assertEqual(code, 1)
        self.assertIn("Exceeds the limit (4300 digits)", output)

    def test_index_out_of_range(self):
        _, _, checked = build("errors/index_out.c", *SANITIZE)
        output, _ = execute([str(checked)], "7\n")
        self.assertIn("index 7 out of bounds", output)
        self.assertIn("stack-buffer-overflow", output)
        _, _, unchecked = build("errors/index_out.c")
        self.assertEqual(execute([str(unchecked)], "2\n"), ("17\n", 0))
        output, code = run_python("errors/index_out.py", "7\n")
        self.assertEqual(code, 1)
        self.assertIn("IndexError: list index out of range", output)

    def test_negative_index_is_valid_in_python_only(self):
        self.assertEqual(run_python("errors/index_out.py", "-1\n"), ("20\n", 0))
        _, _, checked = build("errors/index_out.c", *SANITIZE)
        output, _ = execute([str(checked)], "-1\n")
        self.assertIn("index -1 out of bounds", output)

    def test_sort_programs_agree(self):
        for n in [1, 2, 1000, 5000]:
            with self.subTest(n=n):
                values = sorted((i * 7919) % 100003 for i in range(n))
                expected = (f"menor: {values[0]}, mayor: {values[-1]}\n", 0)
                self.assertEqual(run_c("selection_sort", f"{n}\n"), expected)
                self.assertEqual(run_python("sort_library.py", f"{n}\n"), expected)

    def test_sort_size_gives_the_result_in_the_notes(self):
        self.assertEqual(run_python("sort_library.py", (HERE / "sort_size.txt").read_text()),
                         ("menor: 0, mayor: 100001\n", 0))

    def test_bytecode_tool_runs(self):
        output, code = run_python("show_bytecode.py")
        self.assertEqual(code, 0)
        self.assertIn("BINARY_OP", output)

    def test_int_size_tool_runs(self):
        output, code = run_python("int_size.py")
        self.assertEqual(code, 0)
        small, big = [int(line) for line in output.split()]
        self.assertGreater(big, small)


def raw_request(port, text):
    """Manda bytes tal cual por una conexión y devuelve todo lo que responde el servidor."""
    with socket.create_connection(("127.0.0.1", port), timeout=10) as connection:
        connection.sendall(text.encode("ascii"))
        answer = b""
        while chunk := connection.recv(4096):
            answer += chunk
    return answer


def get(port, path):
    return raw_request(port, f"GET {path} HTTP/1.1\r\nHost: x\r\nConnection: close\r\n\r\n")


class Server(unittest.TestCase):
    def check(self, answer, status, body):
        head, _, actual_body = answer.partition(b"\r\n\r\n")
        lines = head.decode("ascii").split("\r\n")
        self.assertEqual(lines[0], status)
        self.assertEqual(actual_body.decode("utf-8"), body)
        self.assertIn(f"Content-Length: {len(body.encode('utf-8'))}", lines)

    def test_routes(self):
        with web_server() as port:
            self.check(get(port, "/saludo"), "HTTP/1.1 200 OK", "Buenos días, Perú\n")
            self.check(get(port, "/saludo?x=1"), "HTTP/1.1 200 OK", "Buenos días, Perú\n")
            self.check(get(port, "/nada"), "HTTP/1.1 404 Not Found", "No existe esa página\n")
            self.check(get(port, "/error"), "HTTP/1.1 500 Internal Server Error",
                       "Algo falló dentro del servidor\n")
            self.assertIn(b"<h1>Hola desde el servidor</h1>", get(port, "/"))

    def test_a_request_is_only_text(self):
        with web_server() as port:
            answer = raw_request(port, "GET /saludo HTTP/1.1\r\nHost: x\r\nConnection: close\r\n\r\n")
        self.assertTrue(answer.startswith(b"HTTP/1.1 200 OK\r\n"))

    def test_messages_at_start(self):
        port = free_port()
        with tool("server.py", str(port)) as server:
            self.assertEqual(server.banner,
                             f"Servidor en http://127.0.0.1:{port}/ (Ctrl+C para detener)\n")
        with web_server() as target:
            spy_port = free_port()
            with tool("spy.py", str(spy_port), str(target)) as spy:
                self.assertEqual(spy.banner, f"Espía en el puerto {spy_port}, reenvía al {target}\n")

    def test_busy_port_gives_a_message(self):
        with web_server() as port:
            output, code = execute([sys.executable, "server.py", str(port)])
        self.assertEqual(code, 1)
        self.assertIn(f"No se pudo abrir el puerto {port}", output)


class Eavesdropping(unittest.TestCase):
    """El espía ve la cookie en HTTP. En HTTPS ve el nombre, pero no la ruta ni la cookie."""

    def spy_on(self, url_scheme, target_port, host, *curl_options):
        spy_port = free_port()
        with tool("spy.py", str(spy_port), str(target_port)) as spy:
            answer, code = execute(
                ["curl", "-s", "-H", "Cookie: sesion=abc123", *curl_options,
                 f"{url_scheme}://{host}:{spy_port}/saludo"])
            self.assertEqual((answer, code), ("Buenos días, Perú\n", 0))
            spy.terminate()
            return spy.stdout.read()

    def test_http_shows_everything(self):
        with web_server() as port:
            seen = self.spy_on("http", port, "127.0.0.1")
        self.assertIn("GET /saludo HTTP/1.1", seen)
        self.assertIn("Cookie: sesion=abc123", seen)
        self.assertIn("HTTP/1.1 200 OK", seen)

    def test_https_hides_path_and_cookie(self):
        done = subprocess.run(["make", "--no-print-directory", "cert"], cwd=HERE,
                              capture_output=True, text=True)
        self.assertEqual(done.returncode, 0, done.stderr)
        with web_server("--tls") as port:
            seen = self.spy_on("https", port, "localhost", "--cacert", "build/cert.pem")
        self.assertIn("localhost", seen)
        for secret in ["/saludo", "sesion", "abc123", "Buenos", "HTTP/1.1 200"]:
            with self.subTest(secret=secret):
                self.assertNotIn(secret, seen)

    def test_without_trusting_the_certificate_curl_refuses(self):
        done = subprocess.run(["make", "--no-print-directory", "cert"], cwd=HERE, capture_output=True)
        self.assertEqual(done.returncode, 0)
        with web_server("--tls") as port:
            output, code = execute(["curl", "-s", "-S", f"https://localhost:{port}/saludo"])
        self.assertEqual(code, 60)
        self.assertIn("self-signed certificate", output)



if __name__ == "__main__":
    unittest.main()
