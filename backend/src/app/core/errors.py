"""Application errors do not expose provider payloads or user data."""


class StateConflictError(Exception):
    """The expected revision differs from the stored revision."""


class ServiceUnavailableError(Exception):
    """A required provider or secure configuration is unavailable."""


class AuthenticationError(Exception):
    """An access token was missing or failed verification."""
