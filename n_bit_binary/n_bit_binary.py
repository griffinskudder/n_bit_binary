"""
This module contains custom types for dealing with n-bit binary numbers.
Author: Griffin Skudder

Copyright 2024 Griffin Skudder

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import sys

if sys.version_info.minor < 5:
    SupportsInt = object
else:
    from typing import SupportsInt


class NBitInteger(SupportsInt):
    """
    An n-bit two's complement binary integer type.
    Use slicing syntax to modify individual _bits. Index 0 is the most
    significant bit.
    Slicing with negative numbers is supported. However, as the integer has a
    fixed length I can't see a use-case.
    Where a string representation is needed a base-10 number will be given.
    Changing the integer being represented via properties is also possible.
    Assign an integer to self.number to do this.
    The number of bits can be changed via a property. Assign a positive,
    non-zero integer to self.bits to do this.
    WARNING: Reducing the number of bits may cause data loss.
    Be sure you understand two's complement before you do this.
    For example:
    n = NBitInteger(5, 16)
    # n can now be represented as 0000000000000101 or 5
    n[0] = True
    # n can now be represented as 1000000000000101 or -32763
    n[15] = False
    # n can now be represented as 1000000000000100 or -32764
    n[-1] = True
    # n can now be represented as 1000000000000101 or -32763
    n.number = 6
    # n can now be represented as 0000000000000110 or 6
    n.bits = 8
    # n can now be represented as 00000110 or 6
    An NBitInteger cannot have a length of zero. This applies to slicing as
    well. Therefore the slice [12:6] is invalid and will throw a ValueError.
    However, a slice of [12:6:-1] is valid and will reverse the bits.
    The methods append and prepend are available.
    """

    def __init__(self, number, bits, signed=True):
        self._signed = bool(signed)
        if bits <= 0:
            raise ValueError("Bits must be greater than zero.")
        self._bits = bits
        if self._signed:
            self._max = 2 ** self.bits // 2 - 1
            self._min = self._max * -1
        else:
            self._max = 2 ** self.bits
            self._min = 0
        number = int(number)
        if number > self._max:
            raise OverflowError
        elif number < self._min:
            raise OverflowError
        self._number = number

    @property
    def number(self):
        return self._number

    @number.setter
    def number(self, value):
        int(value)
        if value > self._max:
            raise OverflowError
        elif value < self._min:
            raise OverflowError
        self._number = value

    @property
    def bits(self):
        return self._bits

    @bits.setter
    def bits(self, value):
        int(value)
        if value <= 0:
            raise ValueError("Bits must be greater zero.")
        if self._signed:
            temp_max = 2 ** value // 2 - 1
            temp_min = temp_max * -1 + 1
        else:
            temp_max = 2 ** value - 1
            temp_min = 0
        bit_string = self.bit_string()
        temp_value = int(bit_string, 2)
        if temp_value > temp_max or temp_value < temp_min:
            raise OverflowError
        self._bits = value
        self._max = temp_max
        self._min = temp_min
        self._number = int(self.bit_string(), 2)

    @property
    def signed(self):
        return self._signed

    @signed.setter
    def signed(self, value):
        value = bool(value)
        if value:
            temp_max = 2 ** self.bits // 2 - 1
            temp_min = self._max * -1 + 1
        else:
            temp_max = 2 ** self.bits - 1
            temp_min = 0
        if self._number > temp_max:
            raise OverflowError
        elif self._number < temp_min:
            raise OverflowError
        self._signed = value

    def append(self, value):
        """
        Append a new least-significant bit to the integer.
        :param value:
        :return:
        """
        self.bits += 1
        self._number <<= 1
        if value:
            self._set_bit(0)
        else:
            self._clear_bit(0)

    def prepend(self, value):
        """
        Prepend a new most-significant bit to the integer.
        :param value:
        :return:
        """
        self.bits += 1
        if value:
            self._set_bit(self.bits - 1)
        else:
            self._clear_bit(self.bits - 1)


    def _set_bit(self, offset: int):
        """
        Set bit at position offset.
        :param offset: Must be an integer. 0 is LSB.
        :return:
        """
        offset = int(offset)
        mask = 1 << offset
        self._number |= mask
        if self._signed and self._number > self._max:
            self._number -= 2 ** self.bits

    def _clear_bit(self, offset: int):
        """
        Clear bit at position offset.
        :param offset: Must be an integer. 0 is LSB.
        :return:
        """
        offset = int(offset)
        mask = ~(1 << offset)
        self._number &= mask

    def bit_string(self):
        """
        :return: String - Big-endian bit string representation.
        """
        s = ""
        for i in reversed(range(self.bits)):
            s += str(int(bool(self._number & (1 << i))))
        return s

    def __len__(self):
        return self.bits

    def __getitem__(self, key):
        if isinstance(key, slice):
            range_tuple = key.indices(self.bits)
            key = range(range_tuple[0], range_tuple[1], range_tuple[2])
        elif isinstance(key, int):
            key = range(key, key + 1)
        else:
            raise ValueError

        if len(key) < 1:
            raise ValueError(
                "This slice {key} would return an integer with 0 bits.".format(
                    key=str(key)))

        return_value = NBitInteger(0, 1)
        first_run = True
        for i in key:
            if i < 0:
                i += self.bits
            mask = 1 << self.bits - 1 - i
            # By performing a bitwise AND operation on this mask and a number
            # we can determine if the bit at offset
            # i is True or False
            if first_run:
                if self._number & mask:
                    return_value._set_bit(0)
                first_run = False
            elif self._number & mask:
                return_value.append(1)
            else:
                return_value.append(0)
        return return_value

    def __setitem__(self, key, value):
        if isinstance(key, slice):
            range_tuple = key.indices(self.bits)
            key = range(range_tuple[0], range_tuple[1], range_tuple[2])
        elif isinstance(key, int):
            key = range(key, key + 1)
        else:
            raise ValueError

        if (key.start < 0 and self.bits - key.start < 0) or (
                key.start > self.bits - 1
        ) or (
                key.stop < 0 and self.bits - key.stop < 0
        ) or key.stop > self.bits:
            raise IndexError

        for i in key:
            if i < 0:
                i += self.bits
            if value:
                self._set_bit(self.bits - 1 - i)
            else:
                self._clear_bit(self.bits - 1 - i)

    def __index__(self):
        return self._number

    def __str__(self):
        return str(self._number)

    def __repr__(self):
        return "NBitInteger(" + str(self._number) + ", " + str(self.bits) + ")"

    def __int__(self):
        return self._number

    def __bool__(self):
        return bool(self._number)

    def __lt__(self, value):
        return self._number < value

    def __gt__(self, value):
        return self._number > value

    def __le__(self, value):
        return self._number <= value

    def __ge__(self, value):
        return self._number >= value

    def __eq__(self, value):
        return self._number == value

    def __add__(self, other):
        return NBitInteger(self.number + other, signed=self.signed,
                           bits=self.bits)

    def __sub__(self, other):
        return NBitInteger(self.number - other, signed=self.signed,
                           bits=self.bits)

    def __mul__(self, other):
        return NBitInteger(self.number * other, signed=self.signed,
                           bits=self.bits)

    def __floordiv__(self, other):
        return NBitInteger(self.number // other, signed=self.signed,
                           bits=self.bits)

    def __truediv__(self, other):
        return NBitInteger(self.number / other, signed=self.signed,
                           bits=self.bits)

    def __mod__(self, other):
        return NBitInteger(self.number % other, signed=self.signed,
                           bits=self.bits)

    def __pow__(self, power):
        return NBitInteger(self.number ** power, signed=self.signed,
                           bits=self.bits)

    def __lshift__(self, other):
        return NBitInteger(self.number << other, signed=self.signed,
                           bits=self.bits)

    def __rshift__(self, other):
        return NBitInteger(self.number >> other, signed=self.signed,
                           bits=self.bits)

    def __and__(self, other):
        return NBitInteger(self.number & other, signed=self.signed,
                           bits=self.bits)

    def __xor__(self, other):
        return NBitInteger(self.number ^ other, signed=self.signed,
                           bits=self.bits)

    def __or__(self, other):
        return NBitInteger(self.number | other, signed=self.signed,
                           bits=self.bits)

    def __radd__(self, other):
        return NBitInteger(self.number + other, signed=self.signed,
                           bits=self.bits)

    def __rsub__(self, other):
        return NBitInteger(self.number - other, signed=self.signed,
                           bits=self.bits)

    def __rmul__(self, other):
        return NBitInteger(self.number * other, signed=self.signed,
                           bits=self.bits)

    def __rfloordiv__(self, other):
        return NBitInteger(self.number // other, signed=self.signed,
                           bits=self.bits)

    def __rtruediv__(self, other):
        return NBitInteger(self.number / other, signed=self.signed,
                           bits=self.bits)

    def __rmod__(self, other):
        return NBitInteger(self.number % other, signed=self.signed,
                           bits=self.bits)

    def __rpow__(self, power):
        return NBitInteger(self.number ** power, signed=self.signed,
                           bits=self.bits)

    def __rlshift__(self, other):
        return NBitInteger(self.number << other, signed=self.signed,
                           bits=self.bits)

    def __rrshift__(self, other):
        return NBitInteger(self.number >> other, signed=self.signed,
                           bits=self.bits)

    def __rand__(self, other):
        return NBitInteger(self.number & other, signed=self.signed,
                           bits=self.bits)

    def __rxor__(self, other):
        return NBitInteger(self.number ^ other, signed=self.signed,
                           bits=self.bits)

    def __ror__(self, other):
        return NBitInteger(self.number | other, signed=self.signed,
                           bits=self.bits)

    def __neg__(self):
        if self.signed:
            return NBitInteger(
                -self.number,
                signed=self.signed,
                bits=self.bits
            )
        else:
            if -self.number < 0:
                return NBitInteger(-self.number, signed=True, bits=self.bits)

    def __pos__(self):
        return NBitInteger(+self.number, signed=self.signed, bits=self.bits)

    def __abs__(self):
        return NBitInteger(
            abs(self.number),
            signed=self.signed,
            bits=self.bits
        )

    def __invert__(self):
        return NBitInteger(~self.number, signed=self.signed, bits=self.bits)

    def __float__(self):
        return float(self._number)

    def __complex__(self):
        return complex(self._number)
