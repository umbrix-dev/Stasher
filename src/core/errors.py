"""All custom errors for ThemeSwitcher."""


class IsAFileError(Exception):
    """Raised when a path is a file."""

    pass


class PathExistsError(Exception):
    """Raised when a path entry already exists."""

    pass


class DirectoryNameError(Exception):
    """Raised when a directory uses forbidden naming."""

    pass


class ThemeExistsError(Exception):
    """Raised when a theme already exists."""

    pass


class ThemeNotFoundError(Exception):
    """Raised when a theme was not found."""

    pass


class NoEntrysError(Exception):
    """Raised when no path entries exist."""

    pass
