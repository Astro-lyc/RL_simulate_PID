class VideoCaptureAttribute:
    """A video capture attribute."""

    def __init__(self, property_code, value, manual=False, is_enumeration=False):
        self.property_code = property_code
        """The video capture property code."""

        self.value = value
        """The value when the property is being set manually (either 0..100% or 1..N)."""

        self.manual = manual
        """``True`` if the property is being set manually; ``False`` if it is configured as automatic."""

        self.is_enumeration = is_enumeration
        """``True`` if the value is specified as `1..N`; ``False`` if it is specified as `0..100%`."""
