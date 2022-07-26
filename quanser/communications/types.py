class Timeout:
    """A structure to hold timeout information for the stream's `poll` function.

    Parameters
    ----------
    seconds : int
        The seconds portion of the timeout.
    nanoseconds : int
        The nanoseconds portion of the timeout.
    is_absolute : boolean
        Indicates whether the timeout is a relative timeout or an absolute timeout.

    Examples
    --------
    Create a 20-second timeout

    >>> from quanser.communications.stream import Timeout
    >>> timeout = Timeout(20)

    Create a 2000-nanosecond timeout

    >>> from quanser.communications.stream import Timeout
    >>> timeout = Timeout(nanoseconds=2000)

    Create a 1.02 second absolute timeout

    >>> from quanser.communications.stream import Timeout
    >>> timeout = Timeout(1, 20000000, True)

    """
    def __init__(self, seconds=0, nanoseconds=0, is_absolute=False):
        self.seconds = seconds
        self.nanoseconds = nanoseconds
        self.is_absolute = is_absolute
