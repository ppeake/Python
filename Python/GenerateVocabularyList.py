import snappy
import snappy.util
from Snap.Core.EntityModel import *
from Snap.Core.Common import PageSetQueries
from io import StringIO

import os

from collections import defaultdict


"""
This script generates a list of all of the vocabulary included in a page set."""

exceptions = ['Atrás','Back','Copiar en botón','Copy to Button','Home','Inicio']



def generateVocabList(path, output = None, organization = 'Page'): #vocabulary can be listed by 'Page' or 'Label'
    pageSet = PageSet(path)
    filename = os.path.basename(path)
    print(f'\n\n{filename}')
    pages = pageSet.AllPages()
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
                #only include regular and grammar buttons
                if button.ContentType.ToString() in ['Regular', 'Grammar']:
                    #get label for each button
                    label = button.Label

                    if label and label not in exceptions:
                        currentLabelDict[label].add(page.Title)
                        currentPageDict[page.Title].add(label)            

        if organization == 'Page':
            currentDict = pageDict[lang]
            if numLanguages > 1:
                buffer.write(f'\n\n{lang}')
            for page, labels in sorted(currentDict.items(),key=lambda x: x[0]):
                buffer.write(f'\n\n{page}:')
                for label in sorted(labels):
                    buffer.write(f'\n\t{label}')
        elif organization == 'Label':
            print(labelDict)
            currentDict = labelDict[lang]
            if numLanguages > 1:
                buffer.write(f'\n\n{lang}')
            for label, pageList in sorted(currentDict.items(),key=lambda x: x[0]):
                pageList_str = ', '.join(sorted(pageList))
                buffer.write(f'\n{label}: {pageList_str}')
    if output: #print to console
        with open(output, 'w') as file:
            file.write(buffer.getvalue())
            buffer.close()
    else: # print to consolve
        print(buffer.getvalue())

    if organization == 'Page':
        return pageDict
    elif organization == 'Label':
        return labelDict


    
