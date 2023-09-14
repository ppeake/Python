import snappy
import snappy.util
from Snap.Core.EntityModel import *
from Snap.Core.Common import PageSetQueries

import os
from fnmatch import fnmatch
import json




"""
This script finds any regular or grammar buttons that do not have a symbol
"""


#buttonExceptions = [] # list of button labels to ignore
#pageExceptions = ['Cuadro de mandos (Windows)','Siri - Configurar','Actions: A-Z','Descriptors: A-Z', 'Acciones: A-Z','Descriptores: A-Z', 'Date', 'More Dates','Apoyos'] #list of pages to ignore
#pageExceptionPatterns = ['Message Bar*','Google*','Asistente*', 'Siri*', 'Cuadro*', 'Alexa*'] #list of page patterns to ignore (accepts wildcards using *)

def checkPatternNotInString(string, patternList):
    """
    Returns False if string matches any pattern in patternList
    """
    for pattern in patternList:
        if fnmatch(string, pattern):
            return False
    return True


for path in snappy.util.argPageSetsPaths():
    noSymbolList = []
    with PageSet(path) as pageSet:

        filename = os.path.basename(path)
        print(f'\n\n{filename}\nBUTTONS WITH NO SYMBOL')

        #Load exceptions file if one exists
        contentIdentifier = pageSet.ContentIdentifier
        contentIdentifier = contentIdentifier.replace('/', '-')
        exceptionsPath = './exceptions.FindButtonsWithoutSymbols/' + contentIdentifier + '.json'
        exceptionsPath = os.path.abspath(exceptionsPath)
        if os.path.exists(exceptionsPath):
            with open(exceptionsPath, 'r', encoding='utf-8') as f:
                exceptions = json.load(f)
                buttonExceptions = exceptions['buttonExceptions']
                pageExceptions = exceptions['pageExceptions']
                pageExceptionPatterns = exceptions['pageExceptionPatterns']
        else:
            buttonExceptions = []
            pageExceptions = []
            pageExceptionPatterns = []
        pages = pageSet.AllPages()
        for page in pages:
            buttons = page.Buttons
            for button in buttons:
                #only include regular and grammar buttons
                if button.ContentType.ToString() in ['Regular', 'Grammar']:
                    #get label and symbol for each button
                    label = button.Label
                    symbolId = button.SymbolId()
                    if symbolId == None and label != None and label not in buttonExceptions and page.Title not in pageExceptions and checkPatternNotInString(page.Title, pageExceptionPatterns):
                        noSymbolList.append((page.Title, label))
        for item in sorted(noSymbolList, key=lambda x: x[0]): #sort by page title
            print(f'{item[0]} : {item[1]}')

