import snappy
import snappy.util
from Snap.Core.EntityModel import *
from Tdx.LanguageModel.Core import LanguageUtilities

import os
from collections import defaultdict

"""
"""

outputFilename = 'duplicate_guids.txt'
outputFilename2 = 'duplicate_guids_by_page.txt'

# optionally ignore duplicates across regional variants for a given language
duplicatesWithinLanguageAreOK = True
pageSetNumPages = defaultdict(int)

def collectGuids(pageSetPaths = snappy.util.argPageSetsPaths()):
    """
    Returns a dictionary where keys are guids and values are dictionaries.
    The inner dictionary keys are 2-letter language codes and values
    are lists of (pageSet.ContentIdentifier, page.Title) tuples.

    The returned dictionary allows us to see which guids are used for which
    pages, grouped by 2-letter language code; it may be OK that we reuse guids
    for regional variants of the same page set (e.g., Germany German and Swiss German).
    """
    guids = defaultdict(lambda:defaultdict(list))
    for pageSetPath in pageSetPaths:
        with PageSet(pageSetPath) as pageSet:

            filename = os.path.basename(pageSetPath)
            print(filename)
            pageCount = 0
            
            regionAgnosticLanguage = LanguageUtilities.GetNeutralLanguage(pageSet.Language) # e.g., en_US -> en
            for page in pageSet.AllPages():
                pageCount += 1
                if page.PageType == PageType.Grid:
                    uniqueId = page.UniqueId.ToString()
                    pageInstance = (pageSet.ContentIdentifier, page.Title)
                    guids[uniqueId][regionAgnosticLanguage].append(pageInstance)
                else:
                    # ignore toolbar and message bar pages
                    # since these don't get imported
                    pass
            pageSetNumPages[pageSet.ContentIdentifier] = pageCount

    return guids



duplicatedGuidCount = 0
duplicatesByPage = defaultdict(set) #also collect duplicates organized by page set

with open(outputFilename, 'w', encoding='utf-8') as f:
    for guid, languageGroupings in collectGuids().items():
        
        if duplicatesWithinLanguageAreOK and len(languageGroupings) == 1:
            # Ignore guids where there is only one language grouping.
            # Duplicated guids are either non-existent or are only
            # duplicated across regional variants of a single language,
            # which may be OK.
            continue 

        duplicatedGuidCount += 1
        f.write(f'{guid} :\n')
        for regionAgnosticLanguage, pageInstances in languageGroupings.items():
            f.write(f'    {regionAgnosticLanguage} :\n')
            for pageInstance in sorted(pageInstances, key=lambda t:t[0]): # alpha sort by ContentIdentifier
                contentIdentifier, title = pageInstance
                f.write(f'        \'{contentIdentifier}\' : \'{title}\'\n')
                duplicatesByPage[contentIdentifier].add((title,guid))
        f.write('\n')

with open(outputFilename2, 'w', encoding='utf-8') as f:
    for contentIdentifier in duplicatesByPage:
        pageSetDuplicateCount = 0
        f.write(f'{contentIdentifier} :\n')
        for title, guid in sorted(duplicatesByPage[contentIdentifier], key=lambda t:t[0]): # alpha sort by title
            pageSetDuplicateCount += 1
            f.write(f'    \'{title}\' : \'{guid}\'\n')
        f.write(f'Found {pageSetDuplicateCount} duplicates out of {pageSetNumPages[contentIdentifier]} total pages in page set {title}\n\n')
        print(f'Found {pageSetDuplicateCount} duplicates out of {pageSetNumPages[contentIdentifier]} total pages in page set {contentIdentifier}')
