"""
This module contains custom types for dealing with n-bit binary numbers.
Author: Griffin Skudder
Company: Vector Systems Ltd.
Email: gskudder@vectorsystems.co.nz
"""


class NBitInteger:
    """
    An n-bit two's complement binary integer type.
    Use slicing syntax to modify individual _bits. Index 0 is the least significant bit.
    Slicing with negative numbers is supported. However as the integer has a fixed length I can't see a use-case.
    Where a string representation is needed a base-10 number will be given.
    Changing the integer being represented via properties is also possible. Assign an integer to self.number to do this.
    The number of bits can be changed via a property. Assign a positive, non-zero integer to self.bits to do this.
    WARNING: Reducing the number of bits may cause data loss.
    Be sure you understand two's complement before you do this.
    For example:
    n = NBitInteger(5, 16)
    # n can now be represented as 0000000000000101 or 5
    n[15] = True
    # n can now be represented as 1000000000000101 or -32763
    n[0] = False
    # n can now be represented as 1000000000000100 or -32764
    n[-1] = False
    # n can now be represented as 0000000000000100 or 4
    n.number = 6
    # n can now be represented as 0000000000000110 or 6
    n.bits = 8
    # n can now be represented as 00000110 or 6
    """

    def __init__(self, number, bits):
        self.number = int(number)
        self._bits = bits
        self._max = 2 ** self.bits // 2 - 1
        self._min = self._max * -1 + 1

    @property
    def bits(self):
        return self._bits

    @bits.setter
    def bits(self, value):
        int(value)
        if value <= 0:
            raise ValueError("Bits must be greater zero.")
        self._bits = value
        self._max = 2 ** self.bits // 2 - 1
        self._min = self._max * -1 + 1
        self.number = int(self.bit_string(), 2)

    def _set_bit(self, offset):
        """
        Set bit at position offset.
        :param offset: Must be an integer. 0 is LSB.
        :return:
        """
        int(offset)
        if offset < 0:
            offset += self.bits
        if offset > (self.bits - 1) or offset < 0:
            raise IndexError
        mask = 1 << offset
        self.number |= mask
        if self.number > self._max:
            self.number -= 2 ** self.bits
        elif self.number < self._min:
            self.number += 2 ** self.bits

    def _clear_bit(self, offset):
        """
        Clear bit at position offset.
        :param offset: Must be an integer. 0 is LSB.
        :return:
        """
        int(offset)
        if offset < 0:
            offset += self.bits
        if offset > (self.bits - 1) or offset < 0:
            raise IndexError
        mask = ~(1 << offset)
        self.number &= mask
        if self.number > self._max:
            self.number -= 2 ** self.bits
        elif self.number < self._min:
            self.number += 2 ** self.bits

    def bit_string(self):
        """
        :return: String - Big-endian bit string representation.
        """
        s = ""
        for i in reversed(range(self.bits)):
            s += str(int(bool(self.number & (1 << i))))
        return s

    def __len__(self):
        return self.bits

    def __getitem__(self, key):
        if not isinstance(key, int) and not isinstance(key, slice):
            raise ValueError
        if isinstance(key, slice):
            if key.step is None:
                key = range(key.start, key.stop)
            else:
                key = range(key.start, key.stop, key.step)
        else:
            key = range(key, key + 1)
        if key.start < 0:
            if self.bits - key.start < 0:
                raise IndexError
        if key.start > self.bits - 1:
            raise IndexError
        elif key.stop < 0:
            if self.bits - key.stop < 0:
                raise IndexError
        if key.stop > self.bits:
            raise IndexError
        new_number = NBitInteger(0, self.bits)
        for i in key:
            if i < 0:
                i += self.bits
            if i > (self.bits - 1) or i < 0:
                raise IndexError
            mask = 1 << i
            if self.number & mask:
                new_number._set_bit(i)
            else:
                new_number._clear_bit(i)
        return new_number

    def __setitem__(self, key, value):
        if not isinstance(key, int) and not isinstance(key, slice):
            raise ValueError
        if isinstance(key, slice):
            if key.step is not None and key.stop > key.start:
                key = range(key.start, key.stop, key.step)
            elif key.step is None and key.stop > key.start:
                key = range(key.start, key.stop)
            else:
                key = range(key.start, key.stop, -1)
        else:
            key = range(key, key + 1)
        if key.start < 0:
            if self.bits - key.start < 0:
                raise IndexError
        if key.start > self.bits - 1:
            raise IndexError
        elif key.stop < 0:
            if self.bits - key.stop < 0:
                raise IndexError
        if key.stop > self.bits:
            raise IndexError
        for i in key:
            if i < 0:
                i += self.bits
            if i > (self.bits - 1) or i < 0:
                raise IndexError
            if bool(value):
                self._set_bit(i)
            else:
                self._clear_bit(i)

    def __index__(self):
        return self.number

    def __str__(self):
        return str(self.number)

    def __repr__(self):
        return "NBitInteger(" + str(self.number) + ", " + str(self.bits) + ")"

    def __int__(self):
        return self.number
