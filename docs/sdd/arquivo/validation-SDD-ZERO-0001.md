# Verificação — SDD-ZERO-0001

- **Veredito:** PASS
- **Diff verificado:** 2a307d5792d1a97d1a1aeca87334380fc781a964..13bb653a308f911bac3069bc6342f3dafbac440a
- **Verificador independente:** sim

| # | Comando rodado | Saída (resumo) | Sensor | Passou? | Assertion (file:line) | Perfil usado |
|---|---|---|---|---|---|---|
| 1 | `python3 -c "from math import isclose as i; from temperatura import converter as c; assert type(c(100,'C','F')) is float; assert i(c(100,'C','F'),212); assert i(c(0,'C','K'),273.15); assert i(c(212,'F','K'),373.15); assert i(c(373.15,'K','F'),212)"` | exit=0, sem saída | Mutação: em _de_kelvin, a fórmula K→F passou a somar 31 no lugar de 32 (temperatura/__init__.py:21). O comando do critério falhou com AssertionError (exit 1) e a suíte com failures=4. Com round() no lugar de float(), a suíte deu failures=4. Restaurado, exit 0. | Sim | tests/test_converter.py:13 | automatizado |
| 2 | `python3 -c "import unittest; from temperatura import converter as c; r = unittest.TestCase().assertRaises; r(ValueError,c,-300,'C','F'); r(ValueError,c,-500,'F','C'); r(ValueError,c,-5,'K','C'); r(ValueError,c,10,'X','C'); r(ValueError,c,10,'C','X'); c(0,'K','C')"` | exit=0, sem saída | Mutação: checagem do zero absoluto trocada por 'if False' (temperatura/__init__.py:31). Saída: 'AssertionError: ValueError not raised by converter' (exit 1), suíte com failures=2. Com '<=' no lugar de '<', errors=3. Sem validar 'para', failures=1. Restaurado, exit 0. | Sim | tests/test_converter.py:35 | automatizado |
| 3 | `python3 -c "import unittest; from temperatura import converter as c; r = unittest.TestCase().assertRaises; r(TypeError,c,'10','C','F'); r(TypeError,c,None,'C','F'); r(TypeError,c,True,'C','F'); r(TypeError,c,False,'K','C')"` | exit=0, sem saída | Mutação: retirado 'isinstance(valor, bool) or' (temperatura/__init__.py:27). Saída: 'AssertionError: TypeError not raised by converter' (exit 1), suíte com failures=1. Com a validação de tipo removida por inteiro, failures=1 e errors=1. Restaurado, exit 0. | Sim | tests/test_converter.py:70 | automatizado |
| 4 | `python3 -m unittest discover -s tests -v` | Ran 15 tests in 0.001s OK (exit=0) | A suíte falhou em todas as 7 mutações aplicadas acima (fórmula, round, zero absoluto removido, <=, sem validar 'para', bool aceito, sem TypeError). Depois do git checkout, voltou a 'OK'. | Sim | tests/test_converter.py:13 | automatizado |

## Descompassos encontrados

nenhum
