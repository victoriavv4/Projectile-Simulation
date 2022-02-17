import math
import astropy.coordinates
import numpy as np


def spherical_to_components(magnitude, bearing, trajectory):
    return astropy.coordinates.spherical_to_cartesian(magnitude, math.radians(trajectory), math.radians(bearing))


def components_to_spherical(x, y, z):
    magnitude, trajectory, bearing = astropy.coordinates.cartesian_to_spherical(x, y, z)

    return magnitude, math.degrees(bearing.to_value()), math.degrees(trajectory.to_value())


def add_spherical_vectors(magnitude1, bearing1, trajectory1, magnitude2, bearing2, trajectory2):
    x1, y1, z1 = spherical_to_components(magnitude1, bearing1, trajectory1)
    x2, y2, z2 = spherical_to_components(magnitude2, bearing2, trajectory2)
    return components_to_spherical(x1 + x2, y1 + y2, z1 + z2)


x = (add_spherical_vectors(3, 7, 12, 5, 2, 0))
y = (add_spherical_vectors(2, 4, 5, 7, 6, 8))
#print(x)
#print(y)

new = np.array(x) + np.array(y)
print(new)
