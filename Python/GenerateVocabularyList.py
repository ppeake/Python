import snappy
import snappy.util
from Snap.Core.EntityModel import *
from Snap.Core.Common import PageSetQueries
from io import StringIO
import os
import json
from collections import defaultdict
from fnmatch import fnmatch

"""
This script generates a list of all of the vocabulary included in a page set.
If page set contains multiple languages, each language will be listed separately

"""
def checkPatternNotInString(string, patternList):
    """
    Returns False if string matches any pattern in patternList
    """
    for pattern in patternList:
        if fnmatch(string, pattern):
            return False
    return True

def isNotException(button, page, exceptions): #takes a button object, page object , and dictionary containings tables of exceptions
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


def generateVocabList(path, output = None, organization = 'page'): #vocabulary can be listed by 'page' or 'label'
    pageSet = PageSet(path)
    filename = os.path.basename(path)
    print(f'\n\n{filename}')
    pages = pageSet.AllPages()
    #Load exceptions file if one exists
    contentIdentifier = pageSet.ContentIdentifier
    contentIdentifier = contentIdentifier.replace('/', '-')
    exceptionsPath = './exceptions.GenerateVocabularyList/' + contentIdentifier + '.json'
    exceptionsPath = os.path.abspath(exceptionsPath)
    if os.path.exists(exceptionsPath):
        with open(exceptionsPath, 'r', encoding='utf-8') as f:
            exceptions = json.load(f)
    else:
        exceptions = {'buttonExceptions': [], 'pageExceptions': [], 'pageExceptionPatterns': [], 'bgColorExceptions': []}     
    #get all languages in pageset
    languages = list(PageSetQueries.GetPageSetLanguages(pageSet))
    print(languages)
    numLanguages = len(languages)
    buffer = StringIO()
    #create dictionary of all of the labels used in the pageset and the buttons and pages they are used in
    labelDict = {language: defaultdict(set) for language in languages}
    pageDict = {language: defaultdict(set) for language in languages}
    for lang in languages:
        for page in pages:
            if page.PageType.value__ != 1:
                continue
            buttons = page.Buttons
            if page.Language:
                if page.Language in ['rw_RW','neut']: #if pagel language is 'rw_RW' (AccessIT mouse page) or 'neut', use the page set language
                    currentLang = pageSet.Language
                else:
                    currentLang = page.Language
            else:
                currentLang = pageSet.Language #if page language is not specified, use the page set language
            currentLabelDict = labelDict[currentLang] # store values in dictionary for currentLang
            currentPageDict = pageDict[currentLang]
            for button in buttons:
                #only include regular and grammar buttons, and check for exceptions
                if button.ContentType.ToString() in ['Regular', 'Grammar'] and isNotException(button,page,exceptions):
                    #get label for each button
                    label = button.Label
                    if label :
                        currentLabelDict[label].add(page.Title)
                        currentPageDict[page.Title].add(label)            

        if organization == 'page':
            currentDict = pageDict[lang]
            if numLanguages > 1:
                buffer.write(f'\n\n{lang}')
            numberWords = sum(len(list) for list in currentDict.values())
            buffer.write(f'\n\nTotal # of words: {numberWords}')
            for page, labels in sorted(currentDict.items(),key=lambda x: x[0]):
                buffer.write(f'\n\n{page}:')
                for label in sorted(labels):
                    buffer.write(f'\n\t{label}')
        elif organization == 'label':
            currentDict = labelDict[lang]
            if numLanguages > 1:
                buffer.write(f'\n\n{lang}')
            numberWords = len(currentDict.items())
            buffer.write(f'\n\nTotal # of words: {numberWords}')
            for label, pageList in sorted(currentDict.items(),key=lambda x: x[0]):
                pageList_str = ', '.join(sorted(pageList))
                buffer.write(f'\n{label}: {pageList_str}')
    if output: #print to console
        with open(output, 'w', encoding="utf-8") as file:
            file.write(buffer.getvalue())
            buffer.close()
    else: # print to console
        print(buffer.getvalue())

    if organization == 'page':
        return pageDict
    elif organization == 'label':
        return labelDict



    
