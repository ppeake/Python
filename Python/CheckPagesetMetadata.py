import snappy
import snappy.util
from Snap.Core.EntityModel import *
from Snap.Core.Common import PageSetQueries

import os
import sys
import glob


propertiesList = ('Language','ContentIdentifier','ContentVersion','FriendlyName',
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

"""
This script takes a file containing the default values for all of the PageSetProperties and checks that the actual page sets match
"""
for path in snappy.util.argPageSetsPaths(recurseDirectories=False):
    with PageSet(path) as pageSet:
        filename = os.path.basename(path)
        languages = list(PageSetQueries.GetPageSetLanguages(pageSet))
        print(f'\n\n*****\n{filename}\n*****\n')
        for prop in propertiesList:
            currentValue = getattr(pageSet, prop)
            match prop:
                case 'LanguageSettingsCollection':
                    currentValue = currentValue.ToString()
                case 'ActiveHomePage':
                    currentValue = currentValue.Title
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
            print(f'{prop}: {currentValue}')

