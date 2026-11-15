"""Pruebas del laboratorio. LAB_DIR dice dónde está el código: lab o solution."""
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

from running_server import HERE, web_server

LAB_DIR = os.environ.get("LAB_DIR", "solution")


def run(stdin):
    done = subprocess.run(
        [str(HERE / "build" / LAB_DIR / "http_status")], input=stdin.encode("utf-8"),
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=10,
    )
    return done.stdout.decode("utf-8", "replace"), done.returncode


def summary(code, headers, body_bytes):
    return (f"código: {code}\nclase: {code // 100}xx\nencabezados: {headers}\n"
            f"cuerpo: {body_bytes} bytes\n", 0)


NOT_HTTP = ("No es una respuesta HTTP\n", 1)


@unittest.skipUnless((HERE / LAB_DIR).is_dir(), f"no existe {LAB_DIR}/")
class StatusLine(unittest.TestCase):
    def test_no_warnings(self):
        done = subprocess.run(
            ["gcc", "-Wall", "-Wextra", "-std=c17", "-Werror", "-fsyntax-only",
             str(HERE / LAB_DIR / "http_status.c")],
            text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
        )
        self.assertEqual(done.returncode, 0, done.stdout)

    def test_valid_codes(self):
        cases = {"HTTP/1.1 200 OK": 200, "HTTP/1.1 404 Not Found": 404,
                 "HTTP/1.0 500 Internal Server Error": 500, "HTTP/2 301 ": 301,
                 "HTTP/3 200": 200, "HTTP/1.1 100 Continue": 100, "HTTP/1.1 599 x": 599}
        for line, code in cases.items():
            with self.subTest(line=line):
                self.assertEqual(run(line + "\r\n\r\n"), summary(code, 0, 0))

    def test_codes_out_of_range(self):
        for line in ["HTTP/1.1 99 x", "HTTP/1.1 600 x", "HTTP/1.1 0 x", "HTTP/1.1 -200 x"]:
            with self.subTest(line=line):
                self.assertEqual(run(line + "\r\n\r\n"), NOT_HTTP)

    def test_not_a_status_line(self):
        for line in ["hola", "hola 200", "GET / HTTP/1.1", "HTTP 200 OK", "http/1.1 200 OK",
                     "HTTP/1.1 abc", "HTTP/1.1", "", "200"]:
            with self.subTest(line=line):
                self.assertEqual(run(line + "\r\n\r\n"), NOT_HTTP)

    def test_long_version_does_not_overflow(self):
        self.assertEqual(run("HTTP/" + "1" * 200 + "x 200 OK\r\n\r\n"), NOT_HTTP)

    @unittest.skipUnless(shutil.which("valgrind"), "no hay valgrind")
    def test_sscanf_result_is_checked(self):
        # Sin revisar lo que devuelve sscanf, se usa un code que nadie asignó. Su valor puede caer
        # fuera de rango por casualidad, así que se le pregunta a valgrind y no a la salida.
        with tempfile.TemporaryDirectory() as folder:
            program = os.path.join(folder, "http_status")
            subprocess.run(["gcc", "-std=c17", "-g", "-O0", str(HERE / LAB_DIR / "http_status.c"),
                            "-o", program], check=True, capture_output=True)
            for line in ["HTTP/1.1 abc\r\n\r\n", "HTTP/1.1\r\n\r\n", "hola\r\n\r\n"]:
                with self.subTest(line=line):
                    done = subprocess.run(
                        ["valgrind", "-q", "--error-exitcode=99", program], input=line.encode(),
                        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=60,
                    )
                    self.assertNotEqual(done.returncode, 99, done.stdout.decode("utf-8", "replace"))

    def test_empty_input(self):
        self.assertEqual(run(""), ("La entrada está vacía\n", 1))


@unittest.skipUnless((HERE / LAB_DIR).is_dir(), f"no existe {LAB_DIR}/")
class Parts(unittest.TestCase):
    def test_headers_and_body(self):
        self.assertEqual(run("HTTP/1.1 200 OK\r\nA: 1\r\nB: 2\r\n\r\nhola\r\nmundo\n"),
                         summary(200, 2, 12))

    def test_example_in_the_notes(self):
        self.assertEqual(run("HTTP/1.1 404 Not Found\r\nA: 1\r\n\r\nhola\n"), summary(404, 1, 5))

    def test_no_body(self):
        self.assertEqual(run("HTTP/1.1 404 Not Found\r\nA: 1\r\n\r\n"), summary(404, 1, 0))

    def test_no_headers(self):
        self.assertEqual(run("HTTP/1.1 200 OK\r\n\r\nabc"), summary(200, 0, 3))

    def test_blank_line_inside_the_body_is_body(self):
        self.assertEqual(run("HTTP/1.1 200 OK\r\nA: 1\r\n\r\nx\r\n\r\ny\n"), summary(200, 1, 7))

    def test_header_like_line_in_the_body_is_body(self):
        self.assertEqual(run("HTTP/1.1 200 OK\r\nA: 1\r\n\r\nB: 2\r\n"), summary(200, 1, 6))

    def test_lines_ending_in_newline_only(self):
        self.assertEqual(run("HTTP/1.1 500 x\nA: 1\nB: 2\nC: 3\n\nz"), summary(500, 3, 1))

    def test_no_blank_line_at_all(self):
        # Sin línea vacía, todo lo que hay son encabezados y el cuerpo queda en 0.
        self.assertEqual(run("HTTP/1.1 200 OK\r\nA: 1\r\nB: 2\r\n"), summary(200, 2, 0))

    def test_body_longer_than_the_buffer(self):
        for size in [255, 256, 1000, 5000]:
            with self.subTest(size=size):
                body = "x" * (size - 1) + "\n"
                self.assertEqual(run("HTTP/1.1 200 OK\r\nA: 1\r\n\r\n" + body),
                                 summary(200, 1, size))

    def test_multibyte_body_counts_bytes(self):
        self.assertEqual(run("HTTP/1.1 200 OK\r\n\r\nBuenos días, Perú\n"), summary(200, 0, 20))


@unittest.skipUnless((HERE / LAB_DIR).is_dir(), f"no existe {LAB_DIR}/")
class WithTheServer(unittest.TestCase):
    def fetch(self, port, path):
        done = subprocess.run(["curl", "-si", f"http://127.0.0.1:{port}{path}"],
                              stdout=subprocess.PIPE, timeout=10)
        return done.stdout.decode("utf-8")

    def test_real_responses(self):
        # El servidor manda cuatro encabezados: Server, Date, Content-Type y Content-Length.
        with web_server() as port:
            self.assertEqual(run(self.fetch(port, "/saludo")), summary(200, 4, 20))
            self.assertEqual(run(self.fetch(port, "/nada")), summary(404, 4, 22))
            self.assertEqual(run(self.fetch(port, "/error")), summary(500, 4, 32))


class GivenPrograms(unittest.TestCase):
    """Python no se evalúa: solo se comprueba que lo que les damos corre."""

    def test_primes_in_c_and_python_agree(self):
        c_program = subprocess.run([str(HERE / "build" / "primes")], input="1000\n",
                                   capture_output=True, text=True, timeout=30)
        python = subprocess.run([sys.executable, str(HERE / "primes.py")], input="1000\n",
                                capture_output=True, text=True, timeout=30)
        self.assertEqual(c_program.stdout, "Hay 168 primos hasta 1000\n")
        self.assertEqual(python.stdout, c_program.stdout)


if __name__ == "__main__":
    unittest.main()
