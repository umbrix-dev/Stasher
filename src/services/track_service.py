import os
import json
from pathlib import Path


import platformdirs


from core.errors import IsAFileError, PathExistsError


class TrackService:
    """The main service for tracking."""
    
    def __init__(self) -> None:
        """Define paths."""
        self.user_data_dir = Path(platformdirs.user_data_dir())
        self.root_dir = self.user_data_dir / "stasher"
        
        
    def track_path(self) -> None:
        """Track a path."""
        
        