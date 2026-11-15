"""Vuelve a correr los comandos que aparecen en los apuntes y en las diapositivas
y comprueba que el código citado existe de verdad en esta carpeta."""
import pathlib
import re
import subprocess
import unittest

HERE = pathlib.Path(__file__).parent
ROOT = HERE.parent.parent
NOTES = ROOT / "notes" / "week-06.md"
SLIDES = ROOT / "slides" / "week-06.tex"
# Antes de un bloque cuyos números cambian con la implementación de C o con la hora.
# De esos bloques solo se exige la forma: lo mismo, salvo los números.
VARIES = "<!-- depende de la implementación -->"


def normalize(text):
    # Según el idioma del entorno, gcc usa comillas tipográficas o rectas.
    return text.replace("‘", "'").replace("’", "'")


def shape(text):
    """Una salida con los números tapados y los espacios juntos."""
    return re.sub(r"\s+", " ", re.sub(r"\d+", "N", text)).strip()


def run_shell(command):
    done = subprocess.run(
        ["bash", "-c", command], cwd=HERE, text=True,
        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=60,
    )
    return normalize(done.stdout)


def strip_lines(text):
    return "\n".join(line.rstrip() for line in text.splitlines()).rstrip("\n")


def split_commands(lines):
    """Parte un bloque de terminal en pares (comando, líneas de salida)."""
    pairs = []
    for line in lines:
        if line.startswith("$ "):
            pairs.append((line[2:], []))
        elif pairs:
            pairs[-1][1].append(normalize(line.rstrip()))
    return pairs


def note_blocks(language):
    """Devuelve (líneas, varía) de cada bloque de los apuntes."""
    blocks, current, flagged, previous = [], None, False, ""
    for raw in NOTES.read_text(encoding="utf-8").splitlines():
        line = re.sub(r"^> ?", "", raw)
        if current is None:
            if line.strip() == "```" + language:
                current, flagged = [], previous.strip() == VARIES
            elif line.strip():
                previous = line
        elif line.strip() == "```":
            blocks.append((current, flagged))
            current = None
        else:
            current.append(line)
    return blocks


def slide_blocks(environments):
    text = SLIDES.read_text(encoding="utf-8")
    pattern = r"\\begin\{(?:%s)\}[^\n]*\n(.*?)\\end\{(?:%s)\}" % (environments, environments)
    return [match.group(1).splitlines() for match in re.finditer(pattern, text, re.S)]


def known_code_lines():
    lines = set()
    for source in list(HERE.glob("*.c")) + list((HERE / "errors").glob("*.c")):
        lines.update(line.strip() for line in source.read_text(encoding="utf-8").splitlines())
    return lines


class NotesAreTrue(unittest.TestCase):
    @unittest.skipUnless(NOTES.exists(), "faltan los apuntes")
    def test_terminal_blocks_in_notes(self):
        checked = 0
        for lines, flagged in note_blocks("text"):
            if not lines or not lines[0].startswith("$ "):
                continue
            for command, expected in split_commands(lines):
                actual = strip_lines(run_shell(command))
                checked += 1
                with self.subTest(command=command):
                    if flagged:
                        self.assertEqual(shape(actual), shape("\n".join(expected)))
                    else:
                        self.assertEqual(actual, "\n".join(expected).rstrip("\n"))
        self.assertGreater(checked, 15)

    @unittest.skipUnless(NOTES.exists(), "faltan los apuntes")
    def test_code_blocks_in_notes_exist(self):
        known = known_code_lines()
        for lines, _ in note_blocks("c"):
            for line in lines:
                if line.strip() and line.strip() != "...":
                    with self.subTest(line=line):
                        self.assertIn(line.strip(), known)

    @unittest.skipUnless(NOTES.exists(), "faltan los apuntes")
    def test_estimate_table(self):
        """Los valores dependen de la implementación, pero la tabla debe ser coherente."""
        rows = re.findall(r"^\| (\d+|Peor error) \| (\d\.\d{4}) \| (\d\.\d{4}) \| (\d\.\d{4}) \|$",
                          NOTES.read_text(encoding="utf-8"), re.M)
        self.assertEqual(len(rows), 6)
        estimates = [[float(x) for x in row[1:]] for row in rows[:5]]
        worst = [float(x) for x in rows[5][1:]]
        for column in range(3):
            value = max(abs(row[column] - 1 / 6) for row in estimates)
            self.assertAlmostEqual(worst[column], value, delta=0.0001)
        self.assertGreater(worst[0], worst[1])
        self.assertGreater(worst[1], worst[2])

    @unittest.skipUnless(NOTES.exists(), "faltan los apuntes")
    def test_toy_generator_table(self):
        text = NOTES.read_text(encoding="utf-8")
        section = text.split("### Un generador de juguete")[1].split("### ")[0]
        rows = re.findall(r"^\| (\d) \| (\d+) \| (\d+) \| (\d+) \|$", section, re.M)
        self.assertEqual(len(rows), 5)
        for _, before, product, after in rows:
            self.assertEqual(5 * int(before) + 3, int(product))
            self.assertEqual(int(product) % 16, int(after))
        produced = run_shell("echo 7 | build/toy_generator").split()
        self.assertEqual(produced[:5], [row[3] for row in rows])

    @unittest.skipUnless(NOTES.exists(), "faltan los apuntes")
    def test_for_parts_table(self):
        """Cuenta de verdad cada parte del for de la tabla, con n = 3."""
        n = 3
        counts = dict.fromkeys(["row_init", "row_test", "row_inc", "col_init",
                                "col_test", "body", "col_inc"], 0)
        counts["row_init"] += 1
        row = 1
        while True:
            counts["row_test"] += 1
            if not row <= n:
                break
            counts["col_init"] += 1
            col = 1
            while True:
                counts["col_test"] += 1
                if not col <= n:
                    break
                counts["body"] += 1
                counts["col_inc"] += 1
                col += 1
            counts["row_inc"] += 1
            row += 1
        self.assertEqual(list(counts.values()), [1, 4, 3, 3, 12, 9, 9])
        text = NOTES.read_text(encoding="utf-8")
        for part, value in [("`row <= n`", 4), ("`col <= n`", 12), ("`int col = 1`", 3)]:
            self.assertRegex(text, re.escape(part) + r" \| [^|]+ \| " + str(value) + r" \|")


class SlidesAreTrue(unittest.TestCase):
    @unittest.skipUnless(SLIDES.exists(), "faltan las diapositivas")
    def test_terminal_blocks_in_slides(self):
        for block in slide_blocks("terminal|terminalchica|salidalarga"):
            for command, expected in split_commands(block):
                actual = [line.rstrip() for line in run_shell(command).splitlines()]
                position = 0
                # Una diapositiva puede omitir líneas, pero no cambiarlas ni reordenarlas.
                for line in expected:
                    line = line.strip()
                    if not line:
                        continue
                    with self.subTest(command=command, line=line):
                        found = [i for i in range(position, len(actual)) if actual[i].strip() == line]
                        self.assertTrue(found, f"no aparece en la salida real: {line}")
                        if found:
                            position = found[0] + 1

    @unittest.skipUnless(SLIDES.exists(), "faltan las diapositivas")
    def test_varying_blocks_in_slides(self):
        # corrida: salida cuyos números dependen de la implementación o de la hora.
        for block in slide_blocks("corrida"):
            for command, expected in split_commands(block):
                with self.subTest(command=command):
                    self.assertEqual(shape(run_shell(command)), shape("\n".join(expected)))

    @unittest.skipUnless(SLIDES.exists() and NOTES.exists(), "faltan archivos")
    def test_estimates_match_the_notes(self):
        rows = re.findall(r"^\| (?:\d+|Peor error) \| (\d\.\d{4}) \| (\d\.\d{4}) \| (\d\.\d{4}) \|$",
                          NOTES.read_text(encoding="utf-8"), re.M)
        slides = SLIDES.read_text(encoding="utf-8")
        for row in rows:
            for value in row:
                with self.subTest(value=value):
                    self.assertIn(value, slides)

    @unittest.skipUnless(SLIDES.exists(), "faltan las diapositivas")
    def test_code_blocks_in_slides_exist(self):
        known = known_code_lines()
        for block in slide_blocks("codigo|codigochico|codigomini"):
            for line in block:
                if line.strip() and line.strip() != "...":
                    with self.subTest(line=line):
                        self.assertIn(line.strip(), known)


if __name__ == "__main__":
    unittest.main()
