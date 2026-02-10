from pathlib import Path


def safemake(paths: dict[Path, bool]) -> None:
    """Safely create files/directorys if they dont exist"""
    for path, isFile in paths.items():
        if isFile:
            try:
                path.touch()
            except FileExistsError:
                pass
        else:
            try:
                path.mkdir()
            except FileExistsError:
                pass
