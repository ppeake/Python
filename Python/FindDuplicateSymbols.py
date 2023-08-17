import snappy
import snappy.util
from Snap.Core.EntityModel import *

import os
from collections import defaultdict


"""
This script finds symbols in a page set that
are associated with more than one button label.
Older version from Shea --  FindDuplicateLabelsOrSymbols.py checks for both symbols and labels, 
and tracks pages of different languages separately
"""

for path in snappy.util.argPageSetsPaths():
    with PageSet(path) as pageSet:

        filename = os.path.basename(path)
        print(f'\n\n{filename}')

        tuples = pageSet.ButtonSymbols()
        
        d = defaultdict(set)
        for t in tuples:
            d[t[1]].add(t[0])

        duplicates = [(i[0], list(i[1])) for i in d.items() if len(i[1]) > 1]
        
        if duplicates:
            print(f'{len(duplicates)} symbols associated with more than one button label\n')
            for symId, labels in duplicates:
                print(f'\n{symId}:')
                for label in sorted(labels):
                    print(f'\t{label}')
