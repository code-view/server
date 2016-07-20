from warnings import warn
from .base import *

try:
    from .local import *
except ImportError:
    warn('Default config used.')
