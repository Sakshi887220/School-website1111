import collections
import math
import os

# We need this class as all operations in games are basically vector operations
# This class is based on collections library
class vector(collections.Sequence):
    """Two-dimensional vector.
    Vectors can be modified in-place or we can return the copy of vector
    v = vector(0, 1)
    """
    # Decimal digits after point
    # object class attribute
    PRECISION = 6
    # We can increase the speed using this way
    __slots__ = ('_x', '_y', '_hash')
    #We have used _x because _ is just naming convention variable name starting with _ means they are local variables
    # Names starting with __ and ending with __ are special variables as you have learned in the previous class
    # Constructor function
    def __init__(self, x, y):
        """Initialize vector with coordinates: x, y.
        v = vector(1, 2)
        v.x = 1
        v.y = 2
        """
        self._hash = None   # hash is the just a value stored in computer and it is uinque for each vector
        self._x = round(x, self.PRECISION)
        self._y = round(y, self.PRECISION)
        """
        Round a number to a given precision in decimal digits (default 0 digits). This returns an int when called with one argument, otherwise the same type as the number. ndigits may be negative.
        """
    # Advantage of property opeartor
    """
    Suppose we create a instance of vector class and we want change x coordinate of it.

    If we do object.x = new_value, only the x value will change but we need to change every value depending on x.
    Values depending on x:

    Suppose we introduce in new variable mod that is simply (x^2 + y^2)
    if we do self.mod = self.x^2  + self.y^2
    and then create a object of vector class
    v = vector(3,4)
    so, mod = 5

    but then we changed x to 0. Will mod change to 4? Answer is NO because 
    mod was initialized when we created object v and now does not change with changing value of x.

    What we can do to solve this problem :
        Rather than making mod as variable we make it a function that returns mod value when we call it on our vector object.
        v.mod()

    using @property we don't need to use object.x() we can call using object.x

    """
    #=======================================================================
    @property
    def x(self):
        """X-axis component of vector.
        v = vector(1, 2)
        if we call v.x it return 1
        if we assign v.x = 3 then call v.x it becomes 3
        """
        return self._x
    # Now we don't need to call self._x we can call self.x
    # x.setter is used to set new value of _x.
    @x.setter
    def x(self, value):
        # Hash value is none means no x is assigned.
        if self._hash is not None:
            raise ValueError('cannot set x after hashing')
        self._x = round(value, self.PRECISION)
    #=========================================================================
    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        if self._hash is not None:
            raise ValueError('cannot set y after hashing')
        self._y = round(value, self.PRECISION)
    #========================================================================
    #Setting hash value for a vector
    def __hash__(self):
        """
        v.__hash__() -> hash(v)
        v = vector(1, 2)
        h = hash(v)
        v.x = 2
        Traceback (most recent call last):
            ...
        ValueError: cannot set x after hashing
        """
        if self._hash is None:
            pair = (self.x, self.y)
            self._hash = hash(pair)
        return self._hash
    #=========================================================================
    # Returns a length of a vector object
    def __len__(self):
        """v.__len__() -> len(v)
        lenght of a vector is always 2
        """
        return 2
    #=========================================================================
    def __getitem__(self, index):
        """v.__getitem__(v, i) -> v[i]
        v = vector(3, 4)
        v[0] = 3
        v[1] = 4
        v[2]
        Traceback (most recent call last):
            ...
        IndexError
        """
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        else:
            raise IndexError
    #========================================================================
    def copy(self):
        """Return copy of vector.
        v = vector(1, 2)
        w = v.copy()
        v is not w. w is a copy of v means changing w won't change v.
        """
        return vector(self.x, self.y)
    #========================================================================
    # Return true if the given other obeject is equal to the our vector.
    def __eq__(self, other):
        """
        v.__eq__(w) -> v == w
        v = vector(1, 2)
        w = vector(1, 2)
        v == w = True
        """
        #Return whether an object is an instance of a class or of a subclass thereof
        if isinstance(other, vector):
            return self.x == other.x and self.y == other.y
        return NotImplemented
    #========================================================================
    # Return true is the given other obeject is not equal to the our vector.
    def __ne__(self, other):
        """
        v.__ne__(w) -> v != w
        v = vector(1, 2)
        w = vector(3, 4)
        v != w = True
        """
        if isinstance(other, vector):
            return self.x != other.x or self.y != other.y
        return NotImplemented
    #========================================================================
    
    # VECTOR OPERATIONS
    

    #======================== A D D I T I O N =====================
    # Changes the current vector object by adding another vector
    def __iadd__(self, other):
        """v.__iadd__(w) -> v += w
        v = vector(1, 2)
        w = vector(3, 4)
        v += w
        v become vector(4, 6)
        v += 1
        v becomes vector(5, 7)
        """
        if self._hash is not None:
            raise ValueError('cannot add vector after hashing')
        elif isinstance(other, vector):
            self.x += other.x
            self.y += other.y
        else:
            self.x += other
            self.y += other
        return self
        # Note it returns the same object.
    #========================================================================
    # Returns the copy of the vector after adding current and new object
    def __add__(self, other):
        """v.__add__(w) -> v + w
        v = vector(1, 2)
        w = vector(3, 4)
        v + w
        vector(4, 6)
        v + 1
        vector(2, 3)
        2.0 + v
        vector(3.0, 4.0)
        """
        copy = self.copy()
        return copy.__iadd__(other)

    __radd__ = __add__
    # we can assign functions also __radd__ is a copy of __add__. 
    #========================================================================
    # This function is same as __iadd__ function
    def move(self, other):
        """Move vector by other (in-place).
        v = vector(1, 2)
        w = vector(3, 4)
        v.move(w)
        v becomes vector(4, 6)
        v.move(3)
        v becomes vector(7, 9)
        """
        self.__iadd__(other)



    #========================S U B T R A C T I O N=====================
    # Changes the current vector object by subtracting another vector
    def __isub__(self, other):
        """v.__isub__(w) -> v -= w
        v = vector(1, 2)
        w = vector(3, 4)
        v -= w
        v becomes vector(-2, -2)
        v -= 1
        v becomes vector(-3, -3)
        """
        if self._hash is not None:
            raise ValueError('cannot subtract vector after hashing')
        elif isinstance(other, vector):
            self.x -= other.x
            self.y -= other.y
        else:
            self.x -= other
            self.y -= other
        return self
        # Note that same object is returned 
    #=========================================================================
    # Returns the copy of the vector after subtracting current and new object
    def __sub__(self, other):
        """v.__sub__(w) -> v - w
        v = vector(1, 2)
        w = vector(3, 4)
        v - w
        vector(-2, -2)
        v - 1
        vector(0, 1)
        """
        copy = self.copy()
        return copy.__isub__(other)


    
    #=================== M U L T I P L I C A T I O N ====================
    # Changes the current vector object by multipling another vector
    def __imul__(self, other):
        """v.__imul__(w) -> v *= w
        v = vector(1, 2)
        w = vector(3, 4)
        v *= w
        v becomes vector(3, 8)
        v *= 2
        v becomes vector(6, 16)
        """
        if self._hash is not None:
            raise ValueError('cannot multiply vector after hashing')
        elif isinstance(other, vector):
            self.x *= other.x
            self.y *= other.y
        else:
            self.x *= other
            self.y *= other
        return self
        # Note that same object is returned
    #=========================================================================
    # Returns the copy of the vector after multiplying current and new object
    def __mul__(self, other):
        """v.__mul__(w) -> v * w
        v = vector(1, 2)
        w = vector(3, 4)
        v * w = vector(3, 8)
        v * 2 = vector(2, 4)
        3.0 * v = vector(3.0, 6.0)
        """
        copy = self.copy()
        return copy.__imul__(other)

    __rmul__ = __mul__
    #=========================================================================
    # This function is same as __imul__
    def scale(self, other):
        """Scale vector by other (in-place).
        v = vector(1, 2)
        w = vector(3, 4)
        v.scale(w)
        v becomes vector(3, 8)
        v.scale(0.5)
        v becomes vector(1.5, 4.0)
        """
        self.__imul__(other)


    #======================D I V I S I O N==================================
    # Changes the current vector object by dividing by  another vector
    def __itruediv__(self, other):
        """v.__itruediv__(w) -> v /= w
        v = vector(2, 4)
        w = vector(4, 8)
        v /= w
        v becomes vector(0.5, 0.5)
        v /= 2
        v becomes vector(0.25, 0.25)
        """
        if self._hash is not None:
            raise ValueError('cannot divide vector after hashing')
        elif isinstance(other, vector):
            self.x /= other.x
            self.y /= other.y
        else:
            self.x /= other
            self.y /= other
        return self
    # Returns the copy of the vector after dividing current and new object
    def __truediv__(self, other):
        """v.__truediv__(w) -> v / w
        v = vector(1, 2)
        w = vector(3, 4)
        w / v = vector(3.0, 2.0)
        v / 2 = vector(0.5, 1.0)
        """
        copy = self.copy()
        return copy.__itruediv__(other)

    #=============== OTHER FUNCTIONS ====================================
    # Returns a copy of negative of given vector
    def __neg__(self):
        """v.__neg__() -> -v
        v = vector(1, 2)
        -v is vector(-1, -2)
        """
        copy = self.copy()
        copy.x = -copy.x
        copy.y = -copy.y
        return copy
    #=======================================================================
    # Returns the modulus of vector
    def __abs__(self):
        """v.__abs__() -> abs(v)
        v = vector(3, 4)
        abs(v) = 5.0
        """
        return (self.x ** 2 + self.y ** 2) ** 0.5
    #=======================================================================
    # Rotates a vector counter clock wise with origin as the centre of rotation
    def rotate(self, angle):
        """Rotate vector counter-clockwise by angle (in-place).
        v = vector(1, 2)
        v.rotate(90)
        v == vector(-2, 1)
        True

        """
        if self._hash is not None:
            raise ValueError('cannot rotate vector after hashing')
        radians = angle * math.pi / 180.0
        cosine = math.cos(radians)
        sine = math.sin(radians)
        x = self.x
        y = self.y
        self.x = x * cosine - y * sine
        self.y = y * cosine + x * sine
    # This method returns the representation of a vector object
    def __repr__(self):
        """v.__repr__() -> repr(v)
        v = vector(1, 2)
        repr(v)
        'vector(1, 2)'
        """
        type_self = type(self)
        name = type_self.__name__
        return '{}({!r}, {!r})'.format(name, self.x, self.y)


def floor(value, size, offset=200):
    """Floor of `value` given `size` and `offset`.

    The floor function is best understood with a diagram of the number line::

         -200  -100    0    100   200
        <--|--x--|-----|--y--|--z--|-->

    The number line shown has offset 200 denoted by the left-hand tick mark at
    -200 and size 100 denoted by the tick marks at -100, 0, 100, and 200. The
    floor of a value is the left-hand tick mark of the range where it lies. So
    for the points show above: ``floor(x)`` is -200, ``floor(y)`` is 0, and
    ``floor(z)`` is 100.

    floor(10, 100) = 0.0
    floor(120, 100) = 100.0
    floor(-10, 100) = -100.0
    floor(-150, 100) = -200.0
    floor(50, 167) = -33.0
    """
    return float(((value + offset) // size) * size - offset)


