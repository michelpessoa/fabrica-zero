import unittest
from math import isclose

import temperatura
from temperatura import converter


class TestRF01(unittest.TestCase):
    def test_retorna_float(self):
        self.assertIs(type(converter(100, "C", "F")), float)

    def test_valores(self):
        self.assertTrue(isclose(converter(100, "C", "F"), 212))
        self.assertTrue(isclose(converter(0, "C", "K"), 273.15))
        self.assertTrue(isclose(converter(212, "F", "K"), 373.15))
        self.assertTrue(isclose(converter(373.15, "K", "F"), 212))
        self.assertTrue(isclose(converter(273.15, "K", "C"), 0, abs_tol=1e-9))
        self.assertTrue(isclose(converter(32, "F", "C"), 0, abs_tol=1e-9))

    def test_mesma_unidade(self):
        for u in "CFK":
            r = converter(10, u, u)
            self.assertIs(type(r), float)
            self.assertEqual(r, 10.0)
        self.assertEqual(converter(1.2345678, "C", "C"), 1.2345678)

    def test_sem_arredondamento(self):
        self.assertEqual(converter(0, "C", "K"), 0 + 273.15)
        self.assertEqual(converter(1, "C", "F"), (1 + 273.15 - 273.15) * 9 / 5 + 32)
        self.assertNotEqual(converter(1, "F", "C"), round(converter(1, "F", "C"), 2))


class TestRF02(unittest.TestCase):
    def test_abaixo_zero_absoluto(self):
        with self.assertRaises(ValueError):
            converter(-300, "C", "F")
        with self.assertRaises(ValueError):
            converter(-500, "F", "C")
        with self.assertRaises(ValueError):
            converter(-5, "K", "C")
        with self.assertRaises(ValueError):
            converter(-273.16, "C", "K")
        with self.assertRaises(ValueError):
            converter(-459.68, "F", "K")
        with self.assertRaises(ValueError):
            converter(-300, "C", "C")

    def test_unidade_desconhecida(self):
        for de, para in [("X", "C"), ("C", "X"), ("c", "F"), ("C", "f"),
                         ("Celsius", "K"), ("", "C"), (None, "C")]:
            with self.assertRaises(ValueError):
                converter(10, de, para)

    def test_zero_absoluto_aceito(self):
        self.assertEqual(converter(0, "K", "C"), -273.15)
        self.assertIs(type(converter(-273.15, "C", "K")), float)
        self.assertIs(type(converter(-459.67, "F", "K")), float)
        self.assertEqual(converter(0, "K", "K"), 0.0)

    def test_ordem_validacao(self):
        with self.assertRaises(TypeError):
            converter("x", "X", "Y")
        with self.assertRaises(ValueError):
            converter(-1000, "X", "C")


class TestRF03(unittest.TestCase):
    def test_tipos_invalidos(self):
        for v in ("10", None, True, False, [1], 1 + 2j):
            with self.assertRaises(TypeError):
                converter(v, "C", "F")
        with self.assertRaises(TypeError):
            converter(False, "K", "C")
        with self.assertRaises(TypeError):
            converter(True, "C", "C")



class TestFormulas(unittest.TestCase):
    def test_all(self):
        self.assertIn("converter", temperatura.__all__)

    def test_formulas_exatas(self):
        self.assertEqual(converter(10, "C", "K"), 10 + 273.15)
        self.assertEqual(converter(50, "F", "K"), (50 - 32) * 5 / 9 + 273.15)
        self.assertEqual(converter(300, "K", "C"), 300 - 273.15)
        self.assertEqual(converter(300, "K", "F"), (300 - 273.15) * 9 / 5 + 32)

    def test_retorna_float_todos_pares(self):
        for de in "CFK":
            for para in "CFK":
                self.assertIs(type(converter(300, de, para)), float)

    def test_fronteiras_zero_absoluto_todas_unidades(self):
        for v, u in ((-273.15, "C"), (-459.67, "F"), (0, "K")):
            for para in "CFK":
                self.assertIs(type(converter(v, u, para)), float)

    def test_acima_do_zero_absoluto_aceito_e_abaixo_rejeitado(self):
        for v, u in ((-273.14, "C"), (-459.66, "F"), (0.001, "K")):
            converter(v, u, "K")
        for v, u in ((-273.16, "C"), (-459.68, "F"), (-0.001, "K")):
            with self.assertRaises(ValueError):
                converter(v, u, "C")

    def test_zero_absoluto_na_origem_nao_no_destino(self):
        # só a unidade de origem é validada
        self.assertEqual(converter(0, "K", "F"), (0 - 273.15) * 9 / 5 + 32)


if __name__ == "__main__":
    unittest.main()
