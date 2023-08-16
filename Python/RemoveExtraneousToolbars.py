import snappy
import snappy.util
from Snap.Core.EntityModel import *

import os

"""
This script removes toolbar pages that have no language-corresponding regular pages in the page set.
"""

def removePage(page):
    """
    This function deletes a page from the page set.
    """
    operation = page.PageSet.FactoryAddRemovePageOperation(page, "")
    operation.ExecuteAndInvert()
    operation.Persist()


for path in snappy.util.argPageSetsPaths():
    with PageSet(path) as pageSet:

        # Figure out which languages in the page set are valid.
        # We assume that if a (non-toolbar) page has its language
        # explicitly set then that's intentional.
        validLanguages = set((pageSet.Language, ))

        for page in pageSet.AllPages():
            
            if page.PageType == PageType.ToolBar:
                continue # skip toolbar pages
            
            if not page.Language:
                continue # skip NULL language pages
            
            if page.Language == 'neut' or page.Language == 'rw_RW':
                continue # skips neutral language paages and hack Rwanda Access-IT pages
            
            validLanguages.add(page.Language)

        # make a list of all of the toolbar pages that aren't represented by validLanguages
        toolbarsToRemove = [page for page in pageSet.AllPages() if page.PageType == PageType.ToolBar and page.Language not in validLanguages and page.Language != 'rw_RW'] # considering (hack) Rwandan toolbar OK

        if toolbarsToRemove:
            filename = os.path.basename(path)
            print(f'{filename}: {validLanguages}')
            print(f'\tremoving toolbars: {[toolbar.Language for toolbar in toolbarsToRemove]}')
            
            for toolbar in toolbarsToRemove:
                removePage(toolbar)
