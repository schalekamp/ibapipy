"""Represents a tag value used for SMART combo routing."""


class TagValue:
    """Represents a tag value used for SMART combo routing."""

    def __init__(self, tag='', value=''):
        """Initialize a new instance of a TagValue.

        Keyword arguments:
        tag   -- tag
        value -- value

        """
        self.tag = tag
        self.value = value

    def __lt__(self, other):
        """Return True if this object is strictly less than the specified
        object; False, otherwise.

        Keyword arguments:
        other -- TagValue to compare to this TagValue

        """
        return self.tag < other.tag
