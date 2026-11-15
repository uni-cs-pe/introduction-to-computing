"""Comprueba lo que los apuntes afirman sobre los programas de la semana 12."""
import pathlib
import re
import subprocess
import tempfile
import unittest

HERE = pathlib.Path(__file__).parent
BUILD = HERE / "build"
FLAGS = ["-Wall", "-Wextra", "-std=c17"]
SANITIZE = ["-g", "-fsanitize=address,undefined"]


def execute(command, stdin=""):
    done = subprocess.run(
        command, input=stdin, cwd=HERE, encoding="utf-8", errors="replace",
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=10,
    )
    return done.stdout, done.returncode


def run(program, stdin=""):
    """Ejecuta un programa de build/; devuelve su salida (con errores) y su estado."""
    return execute([str(BUILD / program)], stdin)


def build_source(source, *extra):
    """Compila un archivo; devuelve los mensajes, el estado y el ejecutable."""
    out = pathlib.Path(tempfile.mkdtemp()) / pathlib.Path(source).stem
    done = subprocess.run(
        ["gcc", *FLAGS, *extra, source, "-o", str(out)], cwd=HERE, encoding="utf-8",
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
    )
    return done.stdout.replace("‘", "'").replace("’", "'"), done.returncode, out


class CleanCompile(unittest.TestCase):
    def test_examples_have_no_warnings(self):
        for source in sorted(HERE.glob("*.c")):
            with self.subTest(source=source.name):
                done = subprocess.run(
                    ["gcc", *FLAGS, "-Werror", "-fsyntax-only", str(source)],
                    text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                )
                self.assertEqual(done.returncode, 0, done.stdout)

    def test_no_pointer_to_struct_in_the_examples(self):
        # La semana no enseña punteros a struct: todo pasa por valor o en un arreglo.
        for source in list(HERE.glob("*.c")) + list((HERE / "errors").glob("*.c")):
            if source.name == "check_students.c":
                continue
            with self.subTest(source=source.name):
                self.assertNotRegex(source.read_text(encoding="utf-8"), r"struct \w+ \*|->")


class Structs(unittest.TestCase):
    def test_first_struct(self):
        self.assertEqual(run("first_struct")[0],
                         "Ana: 14 9 17\nDespués del cambio: 12\nNuevo nombre: Beatriz\n"
                         "sizeof(struct student) = 32\n")

    def test_assignment_copies_the_array_field(self):
        self.assertEqual(run("struct_copy"), ("Ana: 14 9 17\nEna: 20 9 17\n", 0))

    def test_parameter_is_a_copy_but_array_field_alone_is_not(self):
        self.assertEqual(run("struct_param"),
                         ("En la función: 0\nAna: 14 9 17\nAna: 16 9 17\nAna: 0 9 17\n", 0))

    def test_array_of_structs(self):
        self.assertEqual(run("struct_array"), (
            "Ana: 13.33\nBruno: 9.67\nCarla: 11.00\nMejor: Ana\n"
            "Sin Bruno:\nAna: 13.33\nCarla: 11.00\n"
            "Con la primera nota en 0:\nAna: 8.67\nCarla: 7.33\n", 0))

    def test_padding_may_make_it_bigger(self):
        output, _ = run("struct_size")
        sizes = dict(re.findall(r"sizeof\(struct (\w+)\) = (\d+)", output))
        self.assertGreaterEqual(int(sizes["mixed"]), 6)
        self.assertGreaterEqual(int(sizes["sorted"]), 6)
        # Mismos campos, otro orden: el tamaño puede ser otro.
        self.assertGreaterEqual(int(sizes["mixed"]), int(sizes["sorted"]))

    def test_parallel_arrays_bug_mixes_people(self):
        messages, status, binary = build_source("errors/parallel_bug.c")
        self.assertEqual((messages, status), ("", 0))
        self.assertEqual(execute([str(binary)])[0], "Ana: 14\nBruno: 11\n")

    def test_compile_errors(self):
        cases = {
            "errors/compare_structs.c": "invalid operands to binary ==",
            "errors/assign_name.c": "assignment to expression with array type",
            "errors/no_struct_word.c": "unknown type name 'student'",
        }
        for source, message in cases.items():
            with self.subTest(source=source):
                messages, status, _ = build_source(source)
                self.assertNotEqual(status, 0)
                self.assertIn(message, messages)


class Files(unittest.TestCase):
    def test_data_is_as_the_notes_say(self):
        text = (HERE / "estudiantes.txt").read_text(encoding="utf-8")
        self.assertEqual(len(text.splitlines()), 8)
        self.assertEqual((HERE / "estudiantes_vacio.txt").stat().st_size, 0)

    def test_show_file(self):
        output, status = run("show_file", "estudiantes.txt\n")
        self.assertEqual(status, 0)
        self.assertTrue(output.startswith("1: Ana 14 9 17\n"))
        self.assertTrue(output.endswith("8: Gisela 10 11 12\nTotal: 8 líneas\n"))

    def test_show_empty_file(self):
        self.assertEqual(run("show_file", "estudiantes_vacio.txt\n"), ("Total: 0 líneas\n", 0))

    def test_show_missing_file(self):
        output, status = run("show_file", "no_hay.txt\n")
        self.assertEqual(status, 1)
        self.assertTrue(output.startswith("no_hay.txt: "))

    def test_write_mode_empties_and_append_mode_keeps(self):
        note = BUILD / "nota.txt"
        note.write_text("texto viejo\n", encoding="utf-8")
        self.assertEqual(run("write_note"), ("", 0))
        self.assertEqual(note.read_text(encoding="utf-8"), "Nota final: 15\n")
        self.assertEqual(run("write_note"), ("", 0))
        self.assertEqual(note.read_text(encoding="utf-8"), "Nota final: 15\n")
        self.assertEqual(run("append_note"), ("", 0))
        self.assertEqual(run("append_note"), ("", 0))
        self.assertEqual(note.read_text(encoding="utf-8"),
                         "Nota final: 15\nOtra línea\nOtra línea\n")

    def test_feof_loop_repeats_the_last_line(self):
        messages, status, binary = build_source("errors/feof_loop.c")
        self.assertEqual((messages, status), ("", 0))
        output = execute([str(binary)])[0].splitlines()
        expected = (HERE / "compras.txt").read_text(encoding="utf-8").splitlines()
        self.assertEqual(output, expected + expected[-1:])

    def test_unchecked_fopen_is_caught_with_sanitizers(self):
        messages, status, binary = build_source("errors/no_check.c", *SANITIZE)
        self.assertEqual((messages, status), ("", 0))
        output, code = execute([str(binary)])
        self.assertNotEqual(code, 0)
        self.assertIn("AddressSanitizer: SEGV", output)

    def test_fclose_writes_what_was_pending(self):
        # La primera línea depende de la biblioteca: solo se exige la segunda.
        _, status, binary = build_source("errors/no_close.c")
        self.assertEqual(status, 0)
        output = execute([str(binary)])[0].splitlines()
        self.assertEqual(output[-1], "El archivo tiene: Nota: 15")


class Parsing(unittest.TestCase):
    def test_sscanf_results(self):
        output, status = run("parse_fields")
        self.assertEqual(status, 0)
        results = [int(line.split()[0]) for line in output.splitlines()]
        self.assertEqual(results, [4, 4, 3, 1, 2, 5, 1, -1])

    def test_long_lines(self):
        self.assertEqual(run("long_line"), (
            'Línea 1: "una linea corta"\n'
            "Línea 2: no cabe en 16 bytes, se descarta\n"
            'Línea 3: "otra corta"\n', 0))


class Receipt(unittest.TestCase):
    def test_receipt_of_the_notes(self):
        target = BUILD / "boleta_prueba.txt"
        output, status = run("receipt", f"compras.txt\n{target}\n")
        self.assertEqual((output, status), ("Línea 4: mal formada, se omite\nProductos: 4\n", 0))
        self.assertEqual(target.read_text(encoding="utf-8"), (
            "arroz 2 x 4.50 = 9.00\nleche 6 x 3.80 = 22.80\npan 10 x 0.50 = 5.00\n"
            "atún 3 x 5.90 = 17.70\nTotal: S/ 54.50\n"))

    def test_missing_input_keeps_the_old_receipt(self):
        target = BUILD / "boleta_vieja.txt"
        target.write_text("anterior\n", encoding="utf-8")
        output, status = run("receipt", f"no_hay.txt\n{target}\n")
        self.assertEqual(status, 1)
        self.assertTrue(output.startswith("no_hay.txt: "))
        self.assertEqual(target.read_text(encoding="utf-8"), "anterior\n")


if __name__ == "__main__":
    unittest.main()
