import sys
import os
import glob

import snappy
import snappy.util
from snappy.util import *
from Snap.Core.EntityModel import *
from Snap.Core.Common import *
from io import StringIO
from collections import defaultdict
import System
from System import *
from System.Linq import Enumerable
from System.Collections.Generic import *
from SQLite.Net import SQLiteConnection
from Tdx.DataStructures import GenericObjectWrapper

"""TIPS FROM SHEA

#Here's a way to get a specific page referenced by Guid:

import System
guid = System.Guid('5e09eb03-e51d-4402-9aae-96380938a4b4')
page = pageSet.LoadPage(guid)



#To do a symbol search:
import snappy
from snappy.util import *
lm = GetLanguageModel('en')
lm.SnappySymbolSearch('chicken')
"""



def symbolSearch(searchTerm, lang = 'en'):
    """This function returns a list of symbols that match a search term."""
    lm = GetLanguageModel(lang)
    results = lm.SnappySymbolSearch(searchTerm)
    return results



def removePage(page):
    """
    This function deletes a page from the page set.
    DO NOT USE THIS FUNCTION EXCEPT FOR TEST PURPOSES FOR NOW
    """
    operation = page.PageSet.FactoryAddRemovePageOperation(page, "")
    operation.ExecuteAndInvert()
    operation.Persist()


def getPageSetsPaths(pathArg = None, recurseDirectories=True):
    """
    This helper function returns a list of page sets paths when passed a file path or folder path.
    If no path is passed, or the path argument is
    invalid the user will be prompted to enter a valid path.
    """

    while True:
        if pathArg is None:
            pathArg = input('Enter a page set path or directory: ')

        # dragging a file in Windows into the console brackets it with double quotes
        # get rid of those (if any)
        pathArg = pathArg.strip('"')
        # convert path to absolute path (if necessary)
        pathArg = os.path.abspath(pathArg)

        if not os.path.exists(pathArg):
            pathArg = None
            continue # bogus path, try again

        if os.path.isdir(pathArg):
            if recurseDirectories:
                paths = glob.glob(os.path.join(pathArg, "**", "*.sps"), recursive=True)
            else:
                paths = glob.glob(os.path.join(pathArg, "*.sps"), recursive=False)
            
            if paths:
                return paths

        if os.path.isfile(pathArg) and os.path.splitext(pathArg)[1] == '.sps':
            return [pathArg]



def generateVocabList(path, output = None, organization = 'Page', exceptions = []): #vocabulary can be listed by 'Page' or 'Label'
    """This script generates a list of all of the vocabulary included in a page set."""
    if not (os.path.isfile(path) and os.path.splitext(path)[1] == '.sps'):
        print(f'path {path} does not exist')
        exit # bogus path, try again
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
        with open(output, 'w', encoding="utf-8") as file:
            file.write(buffer.getvalue())
            buffer.close()
    else: # print to console
        print(buffer.getvalue())

    if organization == 'Page':
        return pageDict
    elif organization == 'Label':
        return labelDict


    

'''This function returns a list of dictionaries or a table with all of the metadata for a page set or folder of page sets'''
def getPagesetMetadata(paths = None, output = 'Table', recurseDirectories=False): #output can be 'Table' or 'Dictionary'
    propertiesList = ('ContentIdentifier','Language','ContentVersion','FriendlyName',
                  'SchemaVersion','GridDimension','Description','ToolbarLocation','ToolBarGridDimension',
                  'ToolBarBackgroundColor','PreferredGridDimensions','SmartSymLayout','ShowButtonUsageCounts',
                  'ActiveHomePage','KeyboardPage','PreferNavigationButtons','ButtonSearchPathIsAccessible','ButtonSearchShowHiddenPaths',
                  'LanguageSettingsCollection','PageBackgroundColor','AccessMethodType','ActiveMessageBarVisible','ActiveMessageWindowVisible',
                  'ActiveToolBarLocation','FontFamily','FontSize',
                  'GridMarginFactor','MessageBarVisible','MessageWindowBackgroundColor',
                  'MessageWindowFontFamily','MessageWindowFontSize',
                  'MessageWindowFontStyle','MessageBarBackgroundColor',
                  'MessageWindowHighlightColor','MessageWindowLabelAboveSymbol','MessageWindowTextColor',
                  'PageBackgroundColor','OffscreenButton1Commands','OffscreenButton2Commands')
    exceptions = ()
    if paths is None:
        paths = snappy.util.argPageSetsPaths(recurseDirectories=recurseDirectories)
    contentList = []
    for path in paths: #first collect list of content identifiers for each pageset
        with PageSet(path) as pageSet:
            contentIdentifier = pageSet.ContentIdentifier
            contentList.append(contentIdentifier)
    metadataDict = {contentIdentifier: defaultdict() for contentIdentifier in contentList} # now intialize dictionary of dictionaries for each pageset
    for path in paths:
        with PageSet(path) as pageSet:
            filename = os.path.basename(path)
            languages = list(PageSetQueries.GetPageSetLanguages(pageSet))
            contentIdentifier = pageSet.ContentIdentifier
            currentDict = metadataDict[contentIdentifier]
            print(f'\n\n*****\n{filename}\n*****\n')
            for prop in propertiesList:
                currentValue = getattr(pageSet, prop)
                match prop:
                    case 'ActiveHomePage':
                        currentValue = currentValue.Title
                    case 'LanguageSettingsCollection':
                        currentValue = str(currentValue).replace('\r\n\t',',')
                        currentValue = currentValue.replace('\r\n','|')
                    case 'PreferredGridDimensions':
                        gridDimensions = pageSet.PreferredGridDimensions.Items
                        currentValue =           ''
                        for dim in gridDimensions:
                            currentValue += f'({dim.GridDimension}),'
                    case 'KeyboardPage':
                        currentValue = currentValue.Title
                    case 'OffscreenButton1Commands':
                        currentValue = ''
                        for command in pageSet.OffscreenButton1Commands:
                            currentValue += f'{command.DescriptionKey},'
                    case 'OffscreenButton2Commands':
                        currentValue = ''
                        for command in pageSet.OffscreenButton2Commands:
                            currentValue += f'{command.DescriptionKey},'
                currentValue = str(currentValue)
                currentDict[prop] = currentValue
                print(currentValue)
    metadataTable = [] #a single table of all of the metadata for all the pagesets, with a column for each page set
    pagesetList = list(metadataDict.keys())
    for prop in propertiesList:
        propList = [prop]
        for pageset in pagesetList:
            propList.append(metadataDict[pageset][prop])
        metadataTable.append(propList)
    if output == 'Table':
        return metadataTable
    elif output == 'Dictionary':
        return metadataDict



# This function takes 2 dictionaries of metadata (from getPagesetMetadata) and compares them, returning a list of differences.
# The first dictionary is the reference dictionary, which should contain the 'correct' values.
# The 2nd dictionary should be read using getPagesetMetadata and will be tested against the reference dictionary.
def checkPagesetMetadata(referenceDict, testDict):
    differences = []
    for contentIdentifier, dictionary in referenceDict.items():
        for prop, referenceValue in dictionary.items():
            testValue = testDict[contentIdentifier][prop]
            if testValue != referenceValue:
                differences.append((contentIdentifier, prop, referenceValue, testValue)) 

    return differences



def getButtonOrder(pageSet, pageName, targetLayout, output = None): #layout is serialized layout in format [col,row,navButtonEnabled,0]
    """This function returns a list of buttons in a page layout in the order they appear in the layout."""
    page = pageSet.PageWithTitle(pageName)
    buttonList = page.Buttons
    elementList = page.Elements
    pageLayoutList = page.PageLayouts
    layout = next((layout for layout in pageLayoutList if layout.PageLayoutSetting.Serialize() == targetLayout), None)
    placements = layout.ElementPlacements
    buttonOrder = []
    for placement in placements:
        button = ElementPlacementExtensions.GetButton(placement)
        gridPosition = placement.GridPosition.Serialize()
        visible = placement.Visible
        if button.Label is not None:
            buttonOrder.append(button.Label)
            print(button.Label)
    return buttonOrder




