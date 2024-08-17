# n_bit_binary

A small module which defines a class for working with n-bit signed or unsigned 
integers.  
Useful for changing specific bits in an integer as it supports slicing.

## Installation

`pip install n_bit_binary`

## Usage

### Constructing a Binary Integer

The constructor for `NBitInteger` takes three arguments:

- `number`: an integer which is used to set the initial value of the class.
- `bits`: an integer which sets the size of the class in bits
- `signed`: (optional) defaults to `True`, determines whether the represented 
number is signed.

```python
from n_bit_binary import NBitInteger

# signed
n = NBitInteger(-32, 8)

print(n) # -32
print(n.bits) # 8
print(n.signed) # True
print(n.bit_string()) # 11100000

# unsigned
n = NBitInteger(255, 8, signed=False)

print(n) # 255
print(n.bits) # 8
print(n.signed) # False
print(n.bit_string()) # 11111111
```

### Manipulating a Binary Integer

Each bit can be accessed using an its index, where `0` is the most significant 
bit.

```python
from n_bit_binary import NBitInteger

n = NBitInteger(1, 8) # signed

print(n) # 1
print(n.bit_string()) # 00000001

n[0] = True
print(n) # -127
print(n.bit_string()) # 10000001
```
