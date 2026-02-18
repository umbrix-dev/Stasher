"""All custom errors for Stasher."""


class IsAFileError(Exception):
    """Raised when a path is a file."""

    pass


class PathExistsError(Exception):
    """Raised when a path entry already exists."""

    pass


class DirectoryNameError(Exception):
    """Raised when a directory uses forbidden naming."""

    pass


class StashExistsError(Exception):
    """Raised when a stash already exists."""

    pass


class StashNotFoundError(Exception):
    """Raised when a stash was not found."""

    pass


class NoEntrysError(Exception):
    """Raised when no path entries exist."""

    pass
