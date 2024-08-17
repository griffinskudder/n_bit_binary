import pytest

from n_bit_binary import NBitInteger


def test_default_init():
    n = NBitInteger(5, 16)
    assert n == 5
    assert len(n) == 16
    assert n.signed
    assert n.bits == 16


def test_unsigned_init():
    n = NBitInteger(5, 16, signed=False)
    assert n == 5
    assert len(n) == 16
    assert not n.signed
    assert n.bits == 16


def test_zero_length_init():
    with pytest.raises(ValueError):
        NBitInteger(0, 0, signed=True)


def test_init_out_of_range():
    with pytest.raises(OverflowError):
        NBitInteger(128, 8, signed=True)

    with pytest.raises(OverflowError):
        NBitInteger(-1, 8, signed=False)


def test_signed_slicing():
    n = NBitInteger(5, 16)
    n[0] = True
    assert n == 5 - 2 ** 15


def test_unsigned_slicing():
    n = NBitInteger(5, 16, signed=False)
    n[0] = True
    assert n == 5 + 2 ** 15


def test_set_slice():
    n = NBitInteger(5, 16)
    n[0:16] = False
    assert n == 0
    n[0:len(n)] = True
    assert n == -1


def test_slicing_out_of_range():
    with pytest.raises(IndexError):
        n = NBitInteger(5, 16, signed=True)
        n[16] = False
    with pytest.raises(ValueError):
        n["a"] = False


def test_negative_index():
    n = NBitInteger(5, 16, signed=True)
    n[-1] = False
    assert n == 4


def test_overflow():
    with pytest.raises(OverflowError):
        n = NBitInteger(5, 8, signed=True)
        n.number = 128

    with pytest.raises(OverflowError):
        n = NBitInteger(5, 8, signed=False)
        n.number = -1


def test_setting_number():
    n = NBitInteger(5, 16, signed=True)
    n.number = -1
    assert n == -1


def test_addition():
    n = NBitInteger(5, 16)
    new_val = n + 5
    assert new_val == 10
    assert isinstance(new_val, NBitInteger)


def test_setting_length():
    n = NBitInteger(5, 16, signed=False)
    n.bits = 3
    assert n.bits == 3
    assert n == 5
    n = NBitInteger(5, 16, signed=True)
    n.bits = 4
    assert n.bits == 4
    assert n == 5


def test_setting_length_to_0():
    n = NBitInteger(5, 16, signed=False)
    with pytest.raises(ValueError):
        n.bits = 0


def test_setting_length_overflow():
    n = NBitInteger(128, 8, signed=False)
    with pytest.raises(OverflowError):
        n.bits = 7
    n = NBitInteger(-127, 8, signed=True)
    with pytest.raises(OverflowError):
        n.bits = 7


def test_setting_signed():
    n = NBitInteger(5, 16, signed=True)
    n.signed = False
    assert n == 5
    assert not n.signed
    n = NBitInteger(5, 16, signed=False)
    n.signed = True
    assert n == 5
    assert n.signed


def test_setting_signed_overflow():
    n = NBitInteger(-1, 16, signed=True)
    with pytest.raises(OverflowError):
        n.signed = False
    n = NBitInteger(128, 8, signed=False)
    with pytest.raises(OverflowError):
        n.signed = True


def test_subtraction():
    n = NBitInteger(5, 16)
    new_val = n - 5
    assert new_val == 0
    assert isinstance(new_val, NBitInteger)


def test_getting_slice():
    n = NBitInteger(254, 8, signed=False)
    assert n[-1] == 0
    assert isinstance(n[-1], NBitInteger)
    assert n[0] == -1
    assert isinstance(n[0], NBitInteger)
    assert n[0:1] == -1
    assert isinstance(n[0:1], NBitInteger)
    assert n[0:2] == 3
    assert isinstance(n[0:2], NBitInteger)
    assert n[6:8] == 6
    assert isinstance(n[6:8], NBitInteger)


def test_slice_boundaries():
    n = NBitInteger(254, 8, signed=False)
    with pytest.raises(ValueError):
        n["a"]
    with pytest.raises(ValueError):
        n[:-0]
    with pytest.raises(ValueError):
        n[8::]


def test_repr():
    n = NBitInteger(5, 16, signed=True)
    n1 = eval(repr(n))
    assert n == n1
    assert n.bits == n1.bits
    assert n.signed == n1.signed


def test_str():
    n = NBitInteger(5, 16, signed=True)
    assert str(n) == "5"


def test_bool():
    n = NBitInteger(5, 16, signed=True)
    assert bool(n)
    n = NBitInteger(0, 16, signed=False)
    assert not bool(n)


def test_multiply():
    n = NBitInteger(5, 16, signed=True)
    assert n * 5 == 25
    assert isinstance(n * 5, NBitInteger)
