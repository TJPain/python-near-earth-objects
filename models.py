"""Represent models for near-Earth objects and their close approaches.

The `NearEarthObject` class represents a near-Earth object. Each has a unique
primary designation, an optional unique name, an optional diameter, and a flag
for whether the object is potentially hazardous.

The `CloseApproach` class represents a close approach to Earth by an NEO. Each
has an approach datetime, a nominal approach distance, and a relative approach
velocity.

A `NearEarthObject` maintains a collection of its close approaches, and a
`CloseApproach` maintains a reference to its NEO.

The functions that construct these objects use information extracted from the
data files from NASA, so these objects should be able to handle all of the
quirks of the data set, such as missing names and unknown diameters.

You'll edit this file in Task 1.
"""
from helpers import cd_to_datetime, datetime_to_str
import math


class NearEarthObject:
    """A near-Earth object (NEO).

    An NEO encapsulates semantic and physical parameters about the object, such
    as its primary designation (required, unique), IAU name (optional),
    diameter in kilometers (optional - sometimes unknown), and whether it's
    marked as potentially hazardous to Earth.

    A `NearEarthObject` also maintains a collection of its close approaches -
    initialized to an empty collection, but eventually populated in the
    `NEODatabase` constructor.
    """

    def __init__(self, designation='', name=None, diameter=float('nan'), hazardous=False):
        """Create a new `NearEarthObject`.

        :param info: A dictionary of excess keyword arguments supplied to the
        constructor.
        """
        self.name = name if name != '' else None
        self.designation = designation
        self.diameter = float(diameter) if diameter != '' else float('nan')
        self.hazardous = True if hazardous == 'Y' else False

        # Create an empty initial collection of linked approaches.
        self.approaches = []

    @property
    def fullname(self):
        """Return a representation of the full name of this NEO."""
        if self.name:
            return f"{self.designation} ({self.name})"
        return f"{self.designation}"

    def __str__(self):
        """Return `str(self)`."""
        if not math.isnan(self.diameter):
            return f"NEO {self.fullname} has a diameter of " \
                   f"{self.diameter:.3f} km and " \
                   f"{'is' if self.hazardous else 'is not'} " \
                   f"potentially hazardous."
        return f"NEO {self.fullname}, " \
               f"{'is' if self.hazardous else 'is not'} potentially " \
               f"hazardous."

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation
        of this object."""
        return f"NearEarthObject(designation={self.designation!r},  " \
               f"name={self.name!r}, diameter={self.diameter:.3f}, " \
               f"hazardous={self.hazardous!r})"


class CloseApproach:
    """A close approach to Earth by an NEO.

    A `CloseApproach` encapsulates information about the NEO's close approach
    to Earth, such as the date and time (in UTC) of closest approach, the
    nominal approach distance in astronomical units, and the relative
    approach velocity in kilometers per second.

    A `CloseApproach` also maintains a reference to its `NearEarthObject` -
    initially, this information (the NEO's primary designation) is saved in a
    private attribute, but the referenced NEO is eventually replaced in the
    `NEODatabase` constructor.
    """

    def __init__(self, distance=0.0, velocity=0.0, time='0001-Jan-01 00:00', neo=None):
        """Create a new `CloseApproach`.

        :param info: A dictionary of excess keyword arguments supplied to
        the constructor.
        """

        self._designation = neo
        self.time = cd_to_datetime(time)
        self.distance = float(distance)
        self.velocity = float(velocity)

        # Create an attribute for the referenced NEO, originally None.
        self.neo = None

    @property
    def time_str(self):
        """Return a formatted representation of this `CloseApproach`'s
        approach time.

        The value in `self.time` should be a Python `datetime` object. While a
        `datetime` object has a string representation, the default
        representation includes seconds - significant figures that don't exist
        in our input data set.

        The `datetime_to_str` method converts a `datetime` object to a
        formatted string that can be used in human-readable representations and
        in serialization to CSV and JSON files.
        """
        if self.time:
            return datetime_to_str(self.time)
        return "an unknown date and time"

    @property
    def designation(self):
        """Designation getter"""
        return self._designation

    def __str__(self):
        """Return `str(self)`."""
        return f"At {self.time_str}, '{self.neo.fullname}' approached " \
               f"Earth at a distance of {self.distance:.2f} au and a " \
               f"velocity of {self.velocity:.2f} km/s."

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation
        of this object."""
        return f"CloseApproach(time={self.time_str!r}, " \
               f"distance={self.distance:.2f}, " \
               f"velocity={self.velocity:.2f}, " \
               f"neo={self.neo!r})"

    def serialize(self, extension):
        """Returns serialized data in CSV or JSON format
        :params: accepts CSV and JSON file formats
        :return: the data in a serialised dictionary
        """

        if extension not in ('csv', 'json'):
            raise ValueError(f"Invalid file extension")

        if extension == 'csv':
            data = {'datetime_utc': self.time_str,
                    'distance_au': self.distance,
                    'velocity_km_s': self.velocity,
                    'designation': self.neo.designation,
                    'name': self.neo.name,
                    'diameter_km': self.neo.diameter,
                    'potentially_hazardous': self.neo.hazardous
                    }

        else:
            data = {'datetime_utc': self.time_str,
                    'distance_au': self.distance,
                    'velocity_km_s': self.velocity,
                    'neo': {'designation': self.neo.designation,
                            'name': self.neo.name,
                            'diameter_km': self.neo.diameter,
                            'potentially_hazardous':
                            self.neo.hazardous
                            }
                    }

        return data
