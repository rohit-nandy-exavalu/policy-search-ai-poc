"""
Application-specific exceptions.

Instead of exposing low-level HTTPX/network errors to our route layer,
we translate them into exceptions meaningful to our application.
"""


class DownstreamServiceError(Exception):
    """Raised when Policy Admin returns an unexpected error."""

    pass


class DownstreamTimeoutError(Exception):
    """Raised when Policy Admin exceeds our configured timeout."""

    pass
