class InvalidNumberError(Exception):
    """
    Raised when an invalid number (in the range 32776..65535 inclusive)
    is encountered.
    """
    pass


class EmptyStackError(Exception):
    """Raised when attempting to pop an element from an empty stack."""
    pass
