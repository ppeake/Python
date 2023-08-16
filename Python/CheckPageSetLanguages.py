import snappy
import snappy.util
from Snap.Core.EntityModel import *
from Snap.Core.Common import PageSetQueries

import os
import sys
import glob

"""
This script prints all of the languages referenced by page set(s).
"""

    
for path in snappy.util.argPageSetsPaths():
    with PageSet(path) as pageSet:

        languages = list(PageSetQueries.GetPageSetLanguages(pageSet))
        filename = os.path.basename(path)
        print(f'{filename}: {languages}')
