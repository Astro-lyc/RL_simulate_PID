from quanser.common import GenericError


class HILError(GenericError):
    """A hardware exception derived from ``GenericError``.

    Examples
    --------
    Read data from the first two analog input channels until the user aborts via a keyboard interrupt or there is an
    exception, such as loss of communication.

    Using array:

    >>> from array import array
    >>> from quanser.hardware import HIL, HILError
    >>> channels = array('d', [0, 1])
    >>> num_channels = len(channels)
    >>> buffer = array('d', [0.0] * num_channels)
    >>> card = HIL()
    >>> try:
    ...     card.open("q8_usb")
    ...     while True:
    ...         card.read_analog(channels, num_channels, buffer)
    ...         # Process data
    ... except HILError as e:
    ...     print(e.get_error_message())
    ... except KeyboardInterrupt:
    ...     print("Aborted by user.")
    ... finally:
    ...     if card.is_valid():
    ...         card.close()
    ...

    Using numpy:

    >>> import numpy as np
    >>> from quanser.hardware import HIL, HILError
    >>> channels = np.array([0, 1], dtype=np.uint32)
    >>> num_channels = len(channels)
    >>> buffer = np.zeros(num_channels, dtype=np.float64)
    >>> card = HIL()
    >>> try:
    ...     card.open("q8_usb")
    ...     while True:
    ...         card.read_analog(channels, num_channels, buffer)
    ...         # Process data
    ... except HILError as e:
    ...     print(e.get_error_message())
    ... except KeyboardInterrupt:
    ...     print("Aborted by user.")
    ... finally:
    ...     if card.is_valid():
    ...         card.close()
    ...

    """
    pass
