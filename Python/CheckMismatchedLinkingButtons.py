import snappy
import snappy.util
from Snap.Core.EntityModel import *

import os

"""
This script lists all of the linking buttons with
labels that don't match the title of the linked page.
"""

for path in snappy.util.argPageSetsPaths():
    with PageSet(path) as pageSet:

        filename = os.path.basename(path)
        print(f'\n{filename}')

        for page in pageSet.AllPages():
            for button in page.Buttons:
                linkedPage = button.LinkedPage()
                if linkedPage:
                    if linkedPage.Title != button.Label:
                        print(f'[{page.Title}]\t{button.Label} -> {linkedPage.Title}')
        
