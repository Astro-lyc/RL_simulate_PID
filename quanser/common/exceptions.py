class GenericError(Exception):
    """A generic exception.

    Parameters
    ----------
    error_code : int
        The Quanser error code.

    Attributes
    ----------
    error_code : int
        The Quanser error code.

    """

    def __init__(self, error_code):
        self.error_code = error_code

    def get_error_message(self, locale=None, buffer_size=-1):
        """Returns an error message corresponding to the Quanser error code."""
        import quanser.common.utilities
        return quanser.common.utilities.get_error_message(locale, self.error_code, buffer_size)
