"""
This module contains custom types for dealing with n-bit binary numbers.
Author: Griffin Skudder
Company: Vector Systems Ltd.
Email: gskudder@vectorsystems.co.nz
"""


class NBitInteger:
    """
    An n-bit two's complement binary integer type.
    Use slicing syntax to modify individual _bits. Index 0 is the most significant bit.
    Slicing with negative numbers is supported. However as the integer has a fixed length I can't see a use-case.
    Where a string representation is needed a base-10 number will be given.
    Changing the integer being represented via properties is also possible. Assign an integer to self.number to do this.
    The number of bits can be changed via a property. Assign a positive, non-zero integer to self.bits to do this.
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
    An NBitInteger cannot have a length of zero. This applies to slicing as well. Therefore the slice [12:6] is invalid
    and will throw a ValueError. However, a slice of [12:6:-1] is valid and will reverse the bits.
    The methods append and prepend are available.
    """

    def __init__(self, number, bits, signed=True):
        self._signed = bool(signed)
        if bits <= 0:
            raise ValueError("Bits must be greater than zero.")
        self._bits = bits
        if self._signed:
            self._max = 2 ** self.bits // 2 - 1
            self._min = self._max * -1 + 1
        else:
            self._max = 2 ** self.bits - 1
            self._min = 0
        number = int(number)
        if number > self._max:
            raise OverflowError
        elif number < self._min:
            raise OverflowError
        self.number = number

    @property
    def bits(self):
        return self._bits

    @bits.setter
    def bits(self, value):
        int(value)
        if value <= 0:
            raise ValueError("Bits must be greater zero.")
        self._bits = value
        if self._signed:
            self._max = 2 ** self.bits // 2 - 1
            self._min = self._max * -1 + 1
        else:
            self._max = 2 ** self.bits - 1
            self._min = 0
        self.number = int(self.bit_string(), 2)

    @property
    def signed(self):
        return self._signed

    @signed.setter
    def signed(self, value):
        value = bool(value)
        if value:
            max = 2 ** self.bits // 2 - 1
            min = self._max * -1 + 1
        else:
            max = 2 ** self.bits - 1
            min = 0
        if self.number > max:
            raise OverflowError
        elif self.number < min:
            raise OverflowError
        self._signed = value

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
        if self._signed:
            if self.number > self._max:
                self.number -= 2 ** self.bits
            elif self.number < self._min:
                self.number += 2 ** self.bits
        else:
            if self.number > self._max:
                raise OverflowError
            elif self.number < self.min:
                raise OverflowError

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
        if self._signed:
            if self.number > self._max:
                self.number -= 2 ** self.bits
            elif self.number < self._min:
                self.number += 2 ** self.bits
        else:
            if self.number > self._max:
                raise OverflowError
            elif self.number < self.min:
                raise OverflowError

    def append(self, value):
        """
        Append a new least-significant bit to the integer.
        :param value:
        :return:
        """
        self.bits += 1
        self.number <<= 1
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
        if isinstance(key, slice):
            range_tuple = key.indices(self.bits)
            key = range(range_tuple[0], range_tuple[1], range_tuple[2])
        elif isinstance(key, int):
            key = range(key, key + 1)
        else:
            raise ValueError

        if len(key) < 1:
            raise ValueError("This slice {key} would return an integer with 0 bits.".format(key=str(key)))

        if (key.start < 0 and self.bits - key.start < 0) or (key.start > self.bits - 1) or \
                (key.stop < 0 and self.bits - key.stop < 0) or key.stop > self.bits:
            raise IndexError

        return_value = NBitInteger(0, 1)
        first_run = True
        for i in key:
            if i < 0:
                i += self.bits
            mask = 1 << self.bits - 1 - i
            # By performing a bitwise AND operation on this mask and a number we can determine if the bit at offset
            # i is True or False
            if first_run:
                if self.number & mask:
                    return_value._set_bit(0)
                first_run = False
            elif self.number & mask:
                return_value.append(True)
            else:
                return_value.append(False)
        return return_value

    def __setitem__(self, key, value):
        if isinstance(key, slice):
            range_tuple = key.indices(self.bits)
            key = range(range_tuple[0], range_tuple[1], range_tuple[2])
        elif isinstance(key, int):
            key = range(key, key + 1)
        else:
            raise ValueError

        if (key.start < 0 and self.bits - key.start < 0) or (key.start > self.bits - 1) or \
                (key.stop < 0 and self.bits - key.stop < 0) or key.stop > self.bits:
            raise IndexError

        for i in key:
            if i < 0:
                i += self.bits
            if value:
                self._set_bit(self.bits - 1 - i)
            else:
                self._clear_bit(self.bits - 1 - i)

    def __index__(self):
        return self.number

    def __str__(self):
        return str(self.number)

    def __repr__(self):
        return "NBitInteger(" + str(self.number) + ", " + str(self.bits) + ")"

    def __int__(self):
        return self.number

    def __bool__(self):
        return bool(self.number)
