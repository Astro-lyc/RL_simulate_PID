from quanser.common import GenericError


class StreamError(GenericError):
    """A stream exception derived from ``GenericError``.

    Example
    -------
    Read data from the first two analog input channels until the user aborts via a keyboard interrupt or there is an
    exception, such as loss of communication.

    >>> from quanser.communications import Stream, StreamError
    >>> stream = Stream()
    >>> stream.connect("tcpip://localhost:5000", False, 64, 64)
    >>> try:
    ...     stream.close()
    ...     stream.flush()  # Raises an exception: Cannot use a stream after it is closed.
    ... except StreamError as e:
    ...     print(e.get_error_message())  # Handle stream errors.
    ...

    """
    pass
