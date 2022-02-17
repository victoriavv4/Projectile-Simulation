import matplotlib.pyplot as plt
import math
import astropy.coordinates



# Takes a 3D vector, and returns a tuple of the x, y, and z components
def spherical_to_components(magnitude, bearing, trajectory):
    return astropy.coordinates.spherical_to_cartesian(magnitude, math.radians(trajectory), math.radians(bearing))


# Takes the x, y, and z components of a 3D vector, and returns a tuple of magnitude, bearing, and trajectory
def components_to_spherical(x, y, z):
    magnitude, trajectory, bearing = astropy.coordinates.cartesian_to_spherical(x, y, z)

    return magnitude, math.degrees(bearing.to_value()), math.degrees(trajectory.to_value())


# Takes two 3D vectors (each specified by magnitude, bearing, and trajectory) and returns a
# tuple representing the sum of the two vectors
def add_spherical_vectors(magnitude1, bearing1, trajectory1, magnitude2, bearing2, trajectory2):
    x1, y1, z1 = spherical_to_components(magnitude1, bearing1, trajectory1)
    x2, y2, z2 = spherical_to_components(magnitude2, bearing2, trajectory2)

    return components_to_spherical(x1 + x2, y1 + y2, z1 + z2)
