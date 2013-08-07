
# See http://kennethreitz.org/repository-structure-and-python/

import os
import sys
sys.path.insert(0, os.path.abspath('..'))

import zoopla
from zoopla.api_v1 import validate_argument as validate_argument_api_v1
from zoopla.api_v1 import _ApiVersion1
