from typing import assert_type

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
    assert n == 5 - 2**15
    
def test_unsigned_slicing():
    n = NBitInteger(5, 16, signed=False)
    n[0] = True
    assert n == 5 + 2**15

def test_slicing_out_of_range():
    with pytest.raises(IndexError):
        n = NBitInteger(5, 16, signed=True)
        n[16] = False

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
    assert_type(new_val, NBitInteger)

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
    assert_type(new_val, NBitInteger)
