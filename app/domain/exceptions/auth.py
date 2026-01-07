class InvalidCredentials(Exception):
    """Username or password is incorrect (generic)."""

class InvalidToken(Exception):
    """The provided token is invalid."""
    
class AdminRequired(Exception):
    """Admin privileges are required to perform this action."""