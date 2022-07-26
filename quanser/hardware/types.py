MAX_STRING_LENGTH = 2147483647


class Version:
    """A structure to hold version information returned from HIL's `get_version` function.

    Parameters
    ----------
    size : int
        The size of the HILVersion structure.
    major : int
        The major version number of the HIL SDK.
    minor : int
        The minor version number of the HIL SDK.
    release : int
        The release version number of the HIL SDK.
    build : int
        The build version number of the HIL SDK.

    Attributes
    ----------
    size : int
        The size of the HILVersion structure.
    major : int
        The major version number of the HIL SDK.
    minor : int
        The minor version number of the HIL SDK.
    release : int
        The release version number of the HIL SDK.
    build : int
        The build version number of the HIL SDK.

    Examples
    --------
    >>> from quanser.hardware.hil import HIL
    >>> version = HIL.get_version()

    """
    def __init__(self, size, major, minor, release, build):
        self.size = size
        self.major = major
        self.minor = minor
        self.release = release
        self.build = build
