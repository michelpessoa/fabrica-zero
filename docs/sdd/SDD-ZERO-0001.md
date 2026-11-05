---
id: SDD-ZERO-0001
type: SDD
title: "Pacote temperatura: converter(valor, de, para) entre Celsius, Fahrenheit e Kelvin"
status: approved
project: "ZERO"
owner: "Michel Pessoa"
created: "2026-11-05"
updated: "2026-11-05"
relates_to: []
source_docs: []
consumption_instructions: "Leia a SDD inteira antes de implementar. Não implemente se o status não for approved."
sizing: small
supersedes: null
superseded_by: null
tags: [fabrica-descoberta]
---

# Pacote temperatura: converter(valor, de, para) entre Celsius, Fahrenheit e Kelvin

## Resumo executivo

Biblioteca Python pequena, só com a biblioteca padrão, que expõe a função converter(valor, de, para) no pacote temperatura para converter temperaturas entre 'C', 'F' e 'K'. O resultado é um float sem arredondamento. Valores abaixo do zero absoluto e unidades desconhecidas levantam ValueError; valores que não são int nem float (inclusive bool e None) levantam TypeError.

## Decisão(ões) de arquitetura aplicável(is)

Sem ADR: SDD nascida da descoberta da fábrica, sem documento de origem. Pacote temperatura com um único módulo temperatura/__init__.py, que define e exporta converter. Internamente, o valor é convertido da unidade de origem para Kelvin e depois de Kelvin para a unidade de destino. Os testes ficam em tests/test_converter.py e usam unittest da biblioteca padrão, rodados com python3 -m unittest discover -s tests -v. Requer Python 3.11 ou maior.

## Requisitos consolidados

| RF-ID | Requisito | Critério de aceite (EARS) | Arquivos |
|---|---|---|---|
| RF01 | Converter um valor numérico entre as unidades 'C', 'F' e 'K' com converter(valor, de, para), retornando float sem arredondamento. | Quando o usuário chamar converter(valor, de, para) com valor int ou float válido e de/para em 'C', 'F' ou 'K', o sistema deve retornar um float com o valor convertido pelas fórmulas padrão, sem arredondamento. | `temperatura/__init__.py`, `tests/test_converter.py` |
| RF02 | Rejeitar com ValueError valores abaixo do zero absoluto na unidade de origem e unidades desconhecidas. | Se o valor estiver abaixo do zero absoluto na unidade de origem (-273.15 C, -459.67 F, 0 K) ou se de ou para não for 'C', 'F' ou 'K', o sistema deve lançar ValueError. | `temperatura/__init__.py`, `tests/test_converter.py` |
| RF03 | Rejeitar com TypeError valores que não sejam int nem float, inclusive bool e None. | Se o valor passado a converter não for int nem float, ou for bool ou None, o sistema deve lançar TypeError. | `temperatura/__init__.py`, `tests/test_converter.py` |

## Especificação técnica consolidada

Assinatura: converter(valor, de, para) -> float. Unidades aceitas: exatamente 'C', 'F' e 'K'. Fórmulas: C para K: c + 273.15; F para K: (f - 32) * 5 / 9 + 273.15; K para C: k - 273.15; K para F: (k - 273.15) * 9 / 5 + 32. Mesma unidade de origem e destino retorna float(valor). Validação, nesta ordem: 1) se valor for bool ou não for instância de int ou float, TypeError; 2) se de ou para não estiver em {'C','F','K'}, ValueError; 3) se valor for menor que o zero absoluto da unidade de origem (C: -273.15, F: -459.67, K: 0), ValueError; o próprio zero absoluto é aceito. Sem arredondamento do resultado. temperatura/__init__.py deve incluir converter em __all__.

## Critérios de aceite / definição de pronto

| # | Critério (origem: RF-ID / contrato) | Comando de verificação | Resultado esperado | Perfil esperado |
|---|---|---|---|---|
| 1 | RF01: conversões entre C, F e K retornam float com os valores esperados | `python3 -c "from math import isclose as i; from temperatura import converter as c; assert type(c(100,'C','F')) is float; assert i(c(100,'C','F'),212); assert i(c(0,'C','K'),273.15); assert i(c(212,'F','K'),373.15); assert i(c(373.15,'K','F'),212)"` | Exit 0 sem AssertionError | automatizado |
| 2 | RF02: valor abaixo do zero absoluto e unidade desconhecida lançam ValueError | `python3 -c "import unittest; from temperatura import converter as c; r = unittest.TestCase().assertRaises; r(ValueError,c,-300,'C','F'); r(ValueError,c,-500,'F','C'); r(ValueError,c,-5,'K','C'); r(ValueError,c,10,'X','C'); r(ValueError,c,10,'C','X'); c(0,'K','C')"` | Exit 0: todos os casos lançam ValueError e 0 K é aceito | automatizado |
| 3 | RF03: valor que não é int nem float, inclusive bool e None, lança TypeError | `python3 -c "import unittest; from temperatura import converter as c; r = unittest.TestCase().assertRaises; r(TypeError,c,'10','C','F'); r(TypeError,c,None,'C','F'); r(TypeError,c,True,'C','F'); r(TypeError,c,False,'K','C')"` | Exit 0: todos os casos lançam TypeError | automatizado |
| 4 | Regressão: suíte inteira de testes unittest | `python3 -m unittest discover -s tests -v` | Exit 0 com todos os testes OK | automatizado |

## Instruções específicas para a IA implementadora

Toque só nos arquivos listados. Use só a biblioteca padrão do Python 3.11+; não adicione dependências externas (nada de pytest, numpy etc.). Use unittest, com testes em tests/test_converter.py rodando por python3 -m unittest discover -s tests -v. Não arredonde resultados. Não aceite bool como número. Não aceite unidades em minúsculas nem nomes por extenso: só 'C', 'F' e 'K'. Não crie outras funções públicas além de converter.

## Verificação de escopo (nada a mais, nada a menos)

- [ ] Todo requisito consolidado acima tem código correspondente.
- [ ] Todo arquivo tocado aparece nesta SDD.
- [ ] Nenhuma abstração, config, feature flag ou refactor extra.

## Evidência de verificação (preencher antes de status `implemented`)

**Verificador independente:** sim

| # | Comando rodado | Saída (resumo) | Sensor | Passou? | Assertion (file:line) | Perfil usado |
|---|---|---|---|---|---|---|

## Rastreabilidade

| Campo | Valor |
|---|---|
| source_docs | nenhum (descoberta da fábrica) |
