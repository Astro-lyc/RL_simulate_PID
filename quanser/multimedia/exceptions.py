from quanser.common import GenericError


class MediaError(GenericError):
    """A media exception derived from ``GenericError``.

    Example
    -------
    >>> from quanser.multimedia import VideoCapture, MediaError
    >>> capture = VideoCapture()
    >>> try:
    ...     capture.read()  # Capture is not open, so raises an exception.
    ... except MediaError as e:
    ...     print(e.get_error_message())  # Handle media errors.
    ...

    """
    pass
