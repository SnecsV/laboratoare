
# teste/test_decode.py
from arsenal.forensics.decode import desfa


def test_base64():
    strat, b = desfa("U2FsdXQ=")
    assert strat == "base64"
    assert b == b"Salut"


def test_base64_invalid():
    try:
        desfa("abc")
    except ValueError as exc:
        assert str(exc) == "sir Base64 invalid"
    else:
        raise AssertionError("desfa trebuia sa respinga Base64 invalid")


def test_unknown_encoding_is_returned_as_text():
    strat, b = desfa("!!!!")
    assert strat == "necunoscut"
    assert b == b"!!!!"


def test_input_invalid():
    try:
        desfa(None)
    except TypeError as exc:
        assert str(exc) == "desfa asteapta un sir de caractere"
    else:
        raise AssertionError("desfa trebuia sa respinga un input care nu este sir")
