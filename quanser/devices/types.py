import array as arr

class RangingMeasurements:
    """A structure to hold ranging measurements.

    Parameters
    ----------
    distance : float[]
        The distances in metres.
    distance_sigma : float[]
        Estimates of the standard deviation in the current distance measurement.
    heading : float[]
        The headings in radians (will be zero for 1D ranging sensors).
    quality : int[]
        Indications of the quality of the measurement (0 to 100%).
    length : int
        The number of valid measurements in each array.

    Examples
    --------
    Create a holder for ranging measurements.

    >>> from quanser.devices.types import RangingMeasurements
    >>> measurement = RangingMeasurements(num_measurements)

    Create a ranging measurement holder containing values.

    >>> from quanser.devices.types import RangingMeasurements
    >>> measurement = RangingMeasurements(720, 10.0, 0.2, 0.0, 50)

    """
    def __init__(self, num_measurements = 0, distance = 0.0, distance_sigma = 0.0, heading = 0.0, quality = 0):
        """Creates a RangingMeasurements structure, allocating arrays initialized to the given default values
        for each field in the structure.

        Parameters
        ----------
        num_measurements: int
            The number of elements to allocate in the arrays for each field of the structure.
        distance : float
            The distance in metres to which to initialize the array elements of the distance field.
             The default value is 0.0.
        distance_sigma : float
            The estimate of the standard deviation in the current distance measurement to which to initialize
            the array elements of the distance_sigma field. The default value is 0.0.
        heading : float
            The heading in radians (will be zero for 1D ranging sensors) to which to initialize
            the array elements of the heading field. The default value is 0.0.
        quality : int
            The indication of the quality of the measurement (0 to 100%) to which to initialize
            the array elements of the heading field. The default value is 0.

        Examples
        --------
        Create a holder for num_measurements ranging measurements.

        >>> from quanser.devices.types import RangingMeasurements
        >>> num_measurements = 7200
        >>> measurements = RangingMeasurements(num_measurements)

        Create a ranging measurement holder containing non-zero values.

        >>> from quanser.devices.types import RangingMeasurements
        >>> num_measurements = 7200
        >>> measurements = RangingMeasurements(num_measurements, 10.0, 0.2, 0.0, 50)

        Create an empty holder for ranging measurements and then allocate numpy
        arrays for each of the fields of interest.

        >>> from quanser.devices.types import RangingMeasurements
        >>> import numpy as np
        >>> measurement = RangingMeasurements()
        >>> num_measurements = 7200
        >>> measurement.distance = np.array([0] * num_measurements, dtype=np.single)
        >>> measurement.heading = np.array([0] * num_measurements, dtype=np.single)

        """
        if (num_measurements == 0):
            self.distance = None
            self.distance_sigma = None
            self.heading = None
            self.quality = None
        else:
            self.distance = arr.array('f', [distance] * num_measurements)
            self.distance_sigma = arr.array('f', [distance_sigma] * num_measurements)
            self.heading = arr.array('f', [heading] * num_measurements)
            self.quality = arr.array('i', [quality] * num_measurements)

        self.length = 0
