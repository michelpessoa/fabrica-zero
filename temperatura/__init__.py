"""Conversão de temperatura entre Celsius, Fahrenheit e Kelvin."""

__all__ = ["converter"]

_UNIDADES = {"C", "F", "K"}
_ZERO_ABSOLUTO = {"C": -273.15, "F": -459.67, "K": 0}


def _para_kelvin(valor, unidade):
    if unidade == "C":
        return valor + 273.15
    if unidade == "F":
        return (valor - 32) * 5 / 9 + 273.15
    return float(valor)


def _de_kelvin(k, unidade):
    if unidade == "C":
        return k - 273.15
    if unidade == "F":
        return (k - 273.15) * 9 / 5 + 32
    return k


def converter(valor, de, para):
    """Converte valor da unidade `de` para `para` ('C', 'F' ou 'K')."""
    if isinstance(valor, bool) or not isinstance(valor, (int, float)):
        raise TypeError("valor deve ser int ou float")
    if de not in _UNIDADES or para not in _UNIDADES:
        raise ValueError("unidade deve ser 'C', 'F' ou 'K'")
    if valor < _ZERO_ABSOLUTO[de]:
        raise ValueError("valor abaixo do zero absoluto")
    if de == para:
        return float(valor)
    return float(_de_kelvin(_para_kelvin(valor, de), para))
