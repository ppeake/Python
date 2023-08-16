import snappy
import snappy.util
from Snap.Core.EntityModel import *
from Snap.Core.Common import PageSetQueries
from Tdx.LanguageModel.Core import LanguageUtilities

import os

"""
This script ensures that all of the languages referenced
by page set(s) conform to the Snap ISO format.
"""

for path in snappy.util.argPageSetsPaths():
    with PageSet(path) as pageSet:

        languages = list(PageSetQueries.GetPageSetLanguages(pageSet))
        nonConformingLanguageCodes = [l for l in languages if l != LanguageUtilities.ConformToIso(l)]
        filename = os.path.basename(path)

        if nonConformingLanguageCodes:
            print(f'\nERROR: {filename} {nonConformingLanguageCodes}\n')
        else:
            print(f'OK: {filename}')
