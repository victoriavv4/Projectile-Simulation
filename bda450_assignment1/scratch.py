import math
import astropy.coordinates

x = (1, 2, 3)
y = (3, 6, 2)
z = (3, 7, 9)

tuple1 = (1, 2, 3)
tuple2 = (4, 5, 6)

zipped = zip(tuple1, tuple2)
mapped = map(sum, zipped)
new = tuple(mapped)
print(new)
