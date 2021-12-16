# flake8: NOQA
import sys
import os

project_root_path = os.path.join(os.path.dirname(__file__), "..")
sys.path.insert(0, os.path.abspath(project_root_path))

import app
