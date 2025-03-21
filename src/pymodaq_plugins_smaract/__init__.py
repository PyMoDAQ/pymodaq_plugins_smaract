from pathlib import Path
from .utils import Config

from importlib.metadata import version, PackageNotFoundError

from pymodaq.utils.logger import set_logger, get_module_name

config = Config()
try:
    __version__ = version(__package__)
except PackageNotFoundError:
    __version__ = '0.0.0dev'



