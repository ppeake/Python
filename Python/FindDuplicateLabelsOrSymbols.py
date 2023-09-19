import snappy
import snappy.util
from Snap.Core.EntityModel import *
from Snap.Core.Common import PageSetQueries
import argparse
import sys
import os
from collections import defaultdict
from fnmatch import fnmatch
import json



#This script finds labels or symbols in a page set that are associated with more than one button.
#Duplicates are tracked separately for pages with different languages 

#Exception files for each page set are stored in a folder called "exceptions.FindDuplicateLabelsOrSymbols". The name of the exception file
#should be "[pageset_contentIdentifier].json"
#Exception files can specify button labels, page names, page name patterns, or button background colors to exclude from the duplicates check.


parser = argparse.ArgumentParser(description="Allow user to specify whether to check for duplicates of symbols, labels, or both.")

# Add arguments with optional flags
parser.add_argument("action", nargs="?", default="default_action", help="Specify an action")
parser.add_argument("--label", action="store_true", help="Check for duplicate labels")
parser.add_argument("--symbol", action="store_true", help="Check for duplicate symbols")

args = parser.parse_args()


def checkPatternNotInString(string, patternList):
    """
    Returns False if string matches any pattern in patternList
    """
    for pattern in patternList:
        if fnmatch(string, pattern):
            return False
    return True

def isNotException(button, page, exceptions):
    buttonExceptions = exceptions['buttonExceptions']
    pageExceptions = exceptions['pageExceptions']
    pageExceptionPatterns = exceptions['pageExceptionPatterns']
    bgColorExceptions = exceptions['bgColorExceptions']
    if (button.Label not in buttonExceptions and 
        page.Title not in pageExceptions and 
        checkPatternNotInString(page.Title, pageExceptionPatterns) and 
        button.BackgroundColor.Serialize() not in bgColorExceptions
    ):
        return True
    else:
        return False
    


for path in snappy.util.argPageSetsPaths():
    with PageSet(path) as pageSet:

        filename = os.path.basename(path)
        print(f'\n\n{filename}')

        #Load exceptions file if one exists
        contentIdentifier = pageSet.ContentIdentifier
        contentIdentifier = contentIdentifier.replace('/', '-')
        exceptionsPath = './exceptions.FindDuplicateLabelsOrSymbols/' + contentIdentifier + '.json'
        exceptionsPath = os.path.abspath(exceptionsPath)
        if os.path.exists(exceptionsPath):
            with open(exceptionsPath, 'r', encoding='utf-8') as f:
                exceptions = json.load(f)
        else:
            exceptions = {'buttonExceptions': [], 'pageExceptions': [], 'pageExceptionPatterns': [], 'bgColorExceptions': []}



        pages = pageSet.AllPages()
        #get all languages in pageset
        languages = list(PageSetQueries.GetPageSetLanguages(pageSet))
        #create a dictionary for each language of all of the labels used in the pageset and the buttons and pages they are used in
        labelDict = {language: defaultdict(set) for language in languages}
        #create a dictionary for each language of all of the symbols used in the pageset and the buttons and pages they are used in
        symbolDict = {language: defaultdict(set) for language in languages}
        for page in pages:
            if page.Language:
                if page.Language in ['rw_RW','neut']: #if pagel language is 'rw_RW' (AccessIT mouse page) or 'neut', use the page set language
                    currentLang = pageSet.Language
                elif page.Language not in languages:
                    currentLang = pageSet.Language
                    print(f'\n***\n{page.Title} has a language that does not match the page set language(s): {page.Language}\n***')
                    continue
                else:
                    currentLang = page.Language
            else:
                currentLang = pageSet.Language #if page language is None, use the page set language
            currentLabelDict = labelDict[currentLang] #store values in dictionary for currentLang
            currentSymbolDict = symbolDict[currentLang]
            buttons = page.Buttons
            for button in buttons:
                #only include regular and grammar buttons
                if button.ContentType.ToString() in ['Regular', 'Grammar']:
                    #get label & symbol for each button
                    label = button.Label
                    if button.Image:
                        symbol = button.SymbolId()
                    else:
                        symbol = None
                    if label != None and isNotException(button, page, exceptions):
                        currentLabelDict[label].add(page.Title)
                    if symbol != None and isNotException(button, page, exceptions):
                        currentSymbolDict[symbol].add((button.Label, page.Title))
        #create list for each language of labels used more than once
        labelDupes = {language: [] for language in languages}
        symbolDupes = {language: [] for language in languages}
        for lang in languages:
            labelDupes[lang] = [(i[0], list(i[1])) for i in labelDict[lang].items() if len(i[1]) > 1]
            symbolDupes[lang] = [(i[0], list(i[1])) for i in symbolDict[lang].items() if len(i[1]) > 1]
        if args.label or args.action == 'default_action':
            #print labels used more than once
            # Check if any of the label dictionary entries have non-empty lists
            duplicatesExist = any(len(list) > 0 for list in labelDupes.values())
            if duplicatesExist:
                print(f'\n***\nDUPLICATE LABELS\n***')
                for lang in languages:
                    print(f'\n***\n{lang}:\n***')
                    print(f'\n{len(labelDupes[lang])} labels used one more than one button label\n')
                    for label, pages in sorted(labelDupes[lang],key=lambda x: x[0]):
                        print(f'\n{label}:')
                        for page in sorted(pages):
                            print(f'\t{page}')
        if args.symbol:
            #print symbols used more than once
            # Check if any of the symbol dictionary entries have non-empty lists
            duplicatesExist = any(len(list) > 0 for list in symbolDupes.values())
            if duplicatesExist:
                print(f'\n***\nDUPLICATE SYMBOLS\n***')
                for lang in languages:
                    print(f'\n***\n{lang}:\n***')
                    print(f'\n{len(symbolDupes[lang])} symbols used one more than one button label\n')
                    for symbol, locations in sorted(symbolDupes[lang],key=lambda x: x[0]):
                        print(f'\n{symbol}:')
                        for loc in sorted(locations, key=lambda x: x[1]):
                            print(f'\t{loc}')

