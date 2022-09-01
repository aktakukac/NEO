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

"""
from helpers import cd_to_datetime, datetime_to_str


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
    def __init__(self, designation, hazardous, name=None, diameter=None):
        """Create a new `NearEarthObject`.
        parameters:
        designation - non-empty string for designation
        name - optional string (string or None value) for the name of the
        object
        diameter - optional float (float or float('nan')) for the diameter
        hazardous - bool for wether is dangerous object

        """
        self.designation = designation

        if name:
            self.name = name
        else:
            self.name = None

        if diameter:
            self.diameter = diameter
        else:
            self.diameter = float('nan')

        self.hazardous = hazardous

        self.approaches = []

    @property
    def fullname(self):
        """Return a representation of the full name of this NEO."""

        if self.name:
            return self.designation + " (" + self.name + ")"
        else:
            return self.designation

    def __str__(self):
        """Return `str(self)`."""

        my_str = ''
        if self.hazardous:
            my_str = 'is'
        else:
            my_str = 'is not'
        return f"NEO {self.fullname} has a diameter of {self.diameter:.3f} \
            and {my_str} potentially hazardous"

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of
        this object."""
        return f"NearEarthObject(designation={self.designation!r}, \
            name={self.name!r}, " \
               f"diameter={self.diameter:.3f}, hazardous={self.hazardous!r})"

    def serialize(self):
        my_dict = {
            'designation': self.designation,
            'name': self.name,
            'diameter_km': self.diameter,
            'potentially_hazardous': self.hazardous, }
        return my_dict


class CloseApproach:
    """A close approach to Earth by an NEO.

    A `CloseApproach` encapsulates information about the NEO's close approach
    to Earth, such as the date and time (in UTC) of closest approach, the
    nominal approach distance in astronomical units, and the relative approach
    velocity in kilometers per second.

    A `CloseApproach` also maintains a reference to its `NearEarthObject` -
    initially, this information (the NEO's primary designation) is saved in a
    private attribute, but the referenced NEO is eventually replaced in the
    `NEODatabase` constructor.

    """
    def __init__(self, time, distance, velocity, neo, _designation,):
        """Create a new `CloseApproach`.

        parameters:
        time - datetime of flyby
        distance - float of distance
        velocity - float of velocity
        neo - the object of flyby
        _designation - the designation of the neo of flyby
        """
        self.time = cd_to_datetime(time)

        self.distance = distance

        self.velocity = velocity

        self._designation = _designation

        self.neo = neo

    @property
    def time_str(self):
        """Return a formatted representation of this `CloseApproach`'s approach
        time.
        The value in `self.time` should be a Python `datetime` object. While a
        `datetime` object has a string representation, the default
        representation includes seconds - significant figures that don't exist
        in our input
        data set.

        The `datetime_to_str` method converts a `datetime` object to a
        formatted string that can be used in human-readable representations and
        in serialization to CSV and JSON files.
        """
        return datetime_to_str(self.time)

    def __str__(self):
        return f"On {self.time_str}, '{self.neo.fullname}' \
            approaches Earth at a distance of {self.distance:.2f} \
                au and a velocity of {self.velocity:.2f} km/s."

    def __repr__(self):
        return f"CloseApproach(time={self.time_str!r}, \
            distance={self.distance:.2f}, " \
               f"velocity={self.velocity:.2f}, neo={self.neo!r})"

    def serialize(self):
        my_dict = {
            'datetime_utc': datetime_to_str(self.time),
            'distance_au': self.distance,
            'velocity_km_s': self.velocity, }
        return my_dict
