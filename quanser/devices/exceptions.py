from quanser.common import GenericError


class DeviceError(GenericError):
    """A device exception derived from ``GenericError``.

    Example
    -------
    Attempt to use an unopened LIDAR device.

    >>> from quanser.devices import RPLIDAR, RangingMeasurementMode, RangingMeasurements, DeviceError
    >>> lidar = RPLIDAR()
    >>> try:
    ...     measurements = RangingMeasurements(720)
    ...     lidar.read(RangingMeasurementMode.NORMAL, 1.0, measurements)
    ...     # ...
    ... except DeviceError as e:
    ...     print(e.get_error_message())
    ...

    """
    pass
