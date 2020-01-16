''' all controllers for various collections of database '''
import os
# Glob is a library for Unix style pathname pattern expansion
# It allows us to find all the python controller filepaths
# For example users.py
import glob
__all__ = [os.path.basename(f)[:-3]
    for f in glob.glob(os.path.dirname(__file__) + "/*.py")]