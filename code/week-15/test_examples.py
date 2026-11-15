"""Comprueba lo que los apuntes afirman sobre los programas de la semana 15.

Los resultados esperados se recalculan aquí, con los datos del código, de forma independiente.
"""
import pathlib
import re
import subprocess
import tempfile
import unittest

HERE = pathlib.Path(__file__).parent
BUILD = HERE / "build"
FLAGS = ["-Wall", "-Wextra", "-std=c17"]
SANITIZE = ["-g", "-fsanitize=address,undefined"]


def execute(command, stdin="", cwd=HERE):
    done = subprocess.run(
        command, input=stdin, cwd=cwd, encoding="utf-8", errors="replace",
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=20,
    )
    return done.stdout, done.returncode


def run(program, stdin=""):
    return execute([str(BUILD / program)], stdin)


def build_source(source, *extra):
    """Compila un archivo; devuelve los mensajes, el estado y el ejecutable."""
    out = pathlib.Path(tempfile.mkdtemp()) / pathlib.Path(source).stem
    output, code = execute(["gcc", *FLAGS, *extra, source, "-o", str(out)])
    return output, code, out


def mail_data(name):
    """Lee del código fuente los pares (palabras, etiqueta) del arreglo indicado."""
    source = (HERE / "spam_models.c").read_text(encoding="utf-8")
    block = re.search(r"struct mail %s\[\w+\] = \{(.*?)\n    \};" % name, source, re.S).group(1)
    return [(int(a), int(b)) for a, b in re.findall(r"\{(\d+), (\d+)\}", block)]


def threshold_errors(mails, u):
    return sum(1 for words, spam in mails if int(words >= u) != spam)


def memorizer_errors(train, mails):
    errors = 0
    for words, spam in mails:
        closest = min(range(len(train)), key=lambda i: (abs(train[i][0] - words), i))
        errors += train[closest][1] != spam
    return errors


class CleanCompile(unittest.TestCase):
    def test_examples_have_no_warnings(self):
        for source in sorted(HERE.glob("*.c")) + sorted((HERE / "errors").glob("*.c")):
            with self.subTest(source=source.name):
                output, code = execute(["gcc", *FLAGS, "-Werror", "-fsyntax-only", str(source)])
                self.assertEqual(code, 0, output)


class SpamModels(unittest.TestCase):
    def setUp(self):
        self.train = mail_data("train")
        self.test = mail_data("test")
        self.output, self.code = run("spam_models")

    def test_runs(self):
        self.assertEqual(self.code, 0)
        self.assertEqual((len(self.train), len(self.test)), (11, 8))

    def test_error_table_matches_the_data(self):
        for u in range(10):
            self.assertIn(f"u = {u}: {threshold_errors(self.train, u)}\n", self.output)

    def test_learned_threshold_has_the_fewest_errors(self):
        errors = [threshold_errors(self.train, u) for u in range(10)]
        self.assertIn(f"Umbral aprendido: {errors.index(min(errors))}\n", self.output)
        self.assertEqual(errors.index(min(errors)), 4)

    def row(self, name):
        line = next(l for l in self.output.splitlines() if l.startswith(name) and "/" in l)
        return re.findall(r"(\d+)/\d+", line.replace("(u = 2)", ""))

    def test_summary_matches_the_data(self):
        expected = {
            "Regla a mano": (threshold_errors(self.train, 2), threshold_errors(self.test, 2)),
            "Umbral aprendido": (threshold_errors(self.train, 4), threshold_errors(self.test, 4)),
            "Memorizador": (memorizer_errors(self.train, self.train),
                            memorizer_errors(self.train, self.test)),
        }
        for name, (train, test) in expected.items():
            with self.subTest(model=name):
                self.assertEqual(self.row(name), [str(train), str(test)])

    def test_the_memorizer_overfits(self):
        # Lo que dicen los apuntes: el mejor en entrenamiento es el peor en prueba.
        self.assertEqual(memorizer_errors(self.train, self.train), 0)
        self.assertGreater(memorizer_errors(self.train, self.test),
                           threshold_errors(self.test, 4))


class Neuron(unittest.TestCase):
    def setUp(self):
        self.output, self.code = run("neuron")
        self.rows = [tuple(int(x) for x in re.findall(r"-?\d+", line))
                     for line in self.output.splitlines() if "(" in line]

    def test_each_row_follows_the_rule(self):
        self.assertEqual(self.code, 0)
        w_words, w_links, base = 0, 0, 0
        for _, words, links, score, answer, label, new_words, new_links, new_base in self.rows:
            self.assertEqual(score, w_words * words + w_links * links + base)
            self.assertEqual(answer, int(score > 0))
            change = label - answer
            w_words += change * words
            w_links += change * links
            base += change
            self.assertEqual((new_words, new_links, new_base), (w_words, w_links, base))

    def test_last_round_has_no_errors(self):
        self.assertIn("Vueltas: 3. Errores en la última: 0\n", self.output)
        for row in self.rows[-4:]:
            self.assertEqual(row[4], row[5])
        self.assertEqual(self.rows[-1][-3:], (1, 1, -2))


class Network(unittest.TestCase):
    def test_truth_table_is_xor(self):
        output, code = run("network")
        self.assertEqual(code, 0)
        rows = [line.split() for line in output.splitlines() if re.match(r"[01] [01]", line)]
        self.assertEqual(len(rows), 4)
        for row in rows:
            a, b, first, second, result = (int(x) for x in row)
            self.assertEqual(first, int(a or b))
            self.assertEqual(second, int(not (a and b)))
            self.assertEqual(result, int(a != b))

    def test_no_single_neuron_in_the_range(self):
        count = 0
        for w_a in range(-3, 4):
            for w_b in range(-3, 4):
                for base in range(-3, 4):
                    fire = lambda a, b: int(w_a * a + w_b * b + base > 0)
                    count += all(fire(a, b) == int(a != b) for a in (0, 1) for b in (0, 1))
        output, _ = run("network")
        self.assertIn(f"{count} de 343 combinaciones", output)
        self.assertEqual(count, 0)


class NextToken(unittest.TestCase):
    def setUp(self):
        self.lines = (HERE / "corpus.txt").read_text(encoding="utf-8").splitlines()

    def counts_after(self, word):
        found = {}
        for line in self.lines:
            tokens = line.split()
            for a, b in zip(tokens, tokens[1:]):
                if a == word:
                    found[b] = found.get(b, 0) + 1
        return found

    def test_counts_come_from_the_corpus(self):
        for word in ["es", "la", "de", "publicó", "sobre", "en"]:
            found = self.counts_after(word)
            total = sum(found.values())
            output, code = run("next_token", word + "\n")
            self.assertEqual(code, 0)
            first = output.splitlines()[0]
            for following, count in found.items():
                with self.subTest(word=word, following=following):
                    self.assertIn(f"{following} {count}/{total}", first)

    def answer(self, prompt):
        output, code = run("next_token", prompt + "\n")
        self.assertEqual(code, 0)
        return output.splitlines()[1]

    def test_same_answer_true_or_false(self):
        self.assertEqual(self.answer("la capital de perú es"), "la capital de perú es lima .")
        self.assertEqual(self.answer("la capital de chile es"), "la capital de chile es lima .")
        self.assertEqual(self.answer("la capital de ecuador es"), "la capital de ecuador es lima .")
        self.assertIn("la capital de chile es santiago .", self.lines)
        self.assertFalse(any("ecuador" in line for line in self.lines))

    def test_invented_citation_is_not_in_the_corpus(self):
        made_up = self.answer("quispe publicó")
        self.assertEqual(made_up, "quispe publicó un artículo sobre redes en 2019 .")
        self.assertNotIn(made_up, self.lines)
        self.assertIn(self.answer("flores publicó"), self.lines)

    def test_no_data(self):
        self.assertEqual(self.answer("ecuador"), "ecuador [sin datos]")

    def test_blank_lines_are_skipped(self):
        self.assertEqual(run("next_token", "\n   \n")[0], "")

    def test_missing_corpus_is_reported(self):
        output, code = execute([str(BUILD / "next_token")], cwd=tempfile.mkdtemp())
        self.assertEqual(code, 1)
        self.assertIn("corpus.txt", output)


class TheOriginalHasTheBugs(unittest.TestCase):
    def call(self, *args):
        return execute([str(BUILD / "check_original"), *args])

    def test_passes_the_simple_cases(self):
        self.assertEqual(self.call("prime", "7")[0], "1\n")
        self.assertEqual(self.call("prime", "8")[0], "0\n")
        self.assertEqual(self.call("max", "14", "9", "17")[0], "17\n")
        self.assertEqual(self.call("copy", "5", "hola")[0], "[hola]\n")

    def test_fails_at_the_edges(self):
        self.assertEqual(self.call("prime", "9")[0], "1\n")
        self.assertEqual(self.call("max", "-4", "-2", "-9")[0], "0\n")
        output, code = self.call("copy", "3", "hola")
        self.assertNotEqual(code, 0)
        self.assertIn("AddressSanitizer: stack-buffer-overflow", output)


class Transcripts(unittest.TestCase):
    TEXT = (HERE / "lab" / "transcripts.md").read_text(encoding="utf-8")

    def test_each_one_is_labelled_as_an_example(self):
        self.assertIn("No son la salida real de ningún asistente", self.TEXT)
        headings = [l for l in self.TEXT.splitlines() if l.startswith("## ")]
        self.assertEqual(len(headings), 3)
        for heading in headings:
            self.assertIn("ejemplo escrito para la actividad", heading)

    def test_the_code_in_the_text_is_the_code_in_the_folder(self):
        known = set()
        for source in (HERE / "lab" / "transcripts").glob("*.c"):
            known.update(l.strip() for l in source.read_text(encoding="utf-8").splitlines())
        for block in re.findall(r"```c\n(.*?)```", self.TEXT, re.S):
            for line in block.splitlines():
                with self.subTest(line=line):
                    self.assertIn(line.strip(), known | {""})

    def run_transcript(self, name):
        output, code, program = build_source(f"lab/transcripts/{name}.c", *SANITIZE)
        self.assertEqual((output, code), ("", 0))
        return execute([str(program)])

    def test_a_passes_its_own_test_and_has_a_bug(self):
        self.assertEqual(self.run_transcript("count_passing"), ("Pruebas pasadas\n", 0))
        output, code, program = build_source("errors/passing_border.c", *SANITIZE)
        self.assertEqual((output, code), ("", 0))
        output, code = execute([str(program)])
        self.assertNotEqual(code, 0)
        self.assertIn("Assertion `count_passing(border, 3) == 2' failed", output)

    def test_b_is_correct_where_it_can_be_checked(self):
        self.assertEqual(self.run_transcript("count_char"), ("Pruebas pasadas\n", 0))
        source = (HERE / "lab" / "transcripts" / "count_char.c").read_text(encoding="utf-8")
        self.assertIn('assert(count_char("banana", \'a\') == 3);', source)
        checked = source.replace('assert(count_char("banana", \'a\') == 3);', """
            assert(count_char("", 'a') == 0);
            assert(count_char("xyz", 'a') == 0);
            assert(count_char("ab", 'a') == 1);
            assert(count_char("ba", 'a') == 1);
            assert(count_char("aaa", 'a') == 3);
        """)
        with tempfile.TemporaryDirectory() as folder:
            path = pathlib.Path(folder) / "checked.c"
            path.write_text(checked, encoding="utf-8")
            output, code, program = build_source(str(path), *SANITIZE)
            self.assertEqual((output, code), ("", 0))
            self.assertEqual(execute([str(program)]), ("Pruebas pasadas\n", 0))

    def test_c_does_not_compile(self):
        output, code, _ = build_source("lab/transcripts/reverse_text.c", *SANITIZE)
        self.assertNotEqual(code, 0)
        self.assertIn("implicit declaration of function", output)
        self.assertIn("strrev", output)

    def test_the_gcc_output_in_the_text_is_real(self):
        output, _, _ = build_source("lab/transcripts/reverse_text.c", *SANITIZE)
        normalized = output.replace("‘", "'").replace("’", "'").strip()
        text = self.TEXT.replace("‘", "'").replace("’", "'")
        self.assertIn(normalized, text)


class LastChar(unittest.TestCase):
    def test_works_with_hola_and_is_caught_with_the_empty_string(self):
        output, code, program = build_source("errors/last_char.c", *SANITIZE)
        self.assertEqual((output, code), ("", 0))
        done = subprocess.run([str(program)], encoding="utf-8", errors="replace",
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=10)
        self.assertTrue(done.stdout.startswith("a\n"))
        self.assertNotEqual(done.returncode, 0)
        self.assertIn("AddressSanitizer", done.stderr)


if __name__ == "__main__":
    unittest.main()
