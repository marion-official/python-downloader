import re
import os


class FileName:
    """
    the file written on disk
    """
    def __init__(self, file_name: str):
        """
        Initialise the FileName object splitting the file name into base and extenstions
        """

        if not isinstance(file_name, str):
            raise TypeError("filename must be a string")

        # Save the filename
        self.filename: str = file_name

        # Split the file name in extension and base name
        self.base, self.ext = os.path.splitext(file_name)
        self.match = re.match(r'(.*)_(\d*)', self.base)

        self._parse_base()

    def _parse_base(self):
        """
        Initialize the Filename object splitting the file name and finding the counter
        """
        if self.match:
            self.name: str = self.match.group(1)
            self.version: int = int(self.match.group(2)) if self.match.group(2) else 0

        else:
            self.version: int = 0
            self.name: str = self.base

    def get_version(self) -> int:
        """
        Get the current version
        """
        return self.version

    def get_filename(self) -> str:
        """
        Get the current filename
        """
        return self.filename

    def increase_version(self, value: int = 1) -> None:
        """
        Increase the version of value (default 1)
        """
        self.version += value
        if self.version > 0:
            self.filename = f"{self.name}_{self.version}{self.ext}"
        else:
            self.filename = f"{self.name}{self.ext}"
