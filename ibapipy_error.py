"""Common base class for all exceptions in the ibapipy package."""


class IBAPIPyError(Exception):
    """Common base class for all exceptions in the ibapipy package."""

    def __init__(self, message, inner=None):
        """Initialize a new instance of an IBAPIPyError.

        Keyword arguments:
        message -- string describing the error
        inner   -- inner-exception (default: None)

        """
        Exception.__init__(self)
        self.message = '' if message is None else message
        self.inner = inner

    def __str__(self):
        """Called by the str() built-in function and by the print statement
        to compute the "informal" string representation of this object.

        """
        return repr(self.message)
