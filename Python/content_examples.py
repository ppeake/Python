import sys #needed for working with command line arguments
import os #needed for all manner of operating system file functions
import glob #needed for searching finding files and directories based on a pattern

# Libraries need to use Snappy -- pretty much always import these
import snappy
import snappy.util
from snappy.util import *
from Snap.Core.EntityModel import *
from Snap.Core.Common import PageSetQueries


from io import StringIO
from collections import defaultdict #needed for working with dictionaries
import System
from System import *
from System.Linq import Enumerable
from System.Collections.Generic import *
from SQLite.Net import SQLiteConnection
from Tdx.DataStructures import GenericObjectWrapper


# make sure to do requires imports before running script

# TO LOAD A PAGE SET
# use r before ' to indicate raw string and avoid problems with backslashes
path = r'C:\Users\ytao\Desktop\Active Projects\Snap Final Builds NEW\en_US\CoreFirst en-US 1.28.1.126.sps' 
pageSet = PageSet(path) #Loads pageset into variable pageSet

# TO GET ALL PAGES IN PAGE SET 
pages = pageSet.AllPages() #Returns a list of all pages in the pageset
# Note: not a true list
# but an iterable object containing all the pages. You cannot index into it like a list
# i.e. pages[0] will not work

# TO GET SPECIFIC PAGE
page = pageSet.PageWithTitle(pageTitle) #Returns the page with the given title


# TO GET ALL BUTTONS ON A PAGE
buttons = page.Buttons #Returns a list of all buttons on a page (not a true list)

# TO ACCESS PAGE SET PROPERTIES
# The following properties can be access by simple dot notation, i.e. pageSet.property 
# and will return a string or automatically convert to a string
''' 
ContentIdentifier
Language
ContentVersion
FriendlyName
SchemaVersion
Description
SmartSymLayout
ShowButtonUsageCounts
PreferNavigationButtons
ButtonSearchPathIsAccessible
ButtonSearchShowHiddenPaths
ActiveMessageBarVisible
ActiveMessageWindowVisible
FontFamily
FontSize
GridMarginFactor
MessageBarVisible
MessageWindowFontFamily
MessageWindowFontSize
MessageWindowLabelAboveSymbol
'''

# The following properties can be converted to a string by either pageSet.prop.ToString() or str(pageSet.prop)
'''
ToolbarLocation
ActiveToolBarLocation
ToolBarBackgroundColor
MessageBarBackgroundColor
MessageWindowHighlightColor
MessageWindowTextColor
PageBackgroundColor
MessageWindowBackgroundColor
MessageWindowFontStyle
AccessMethodType
GridDimension
ToolBarGridDimension  #will have no value if Toolbar matches page set
LanguageSettingsCollection  #contains Automorph Model, Automrph Grammar Buttons, and Form Contractions for each language in page set
'''

#The following properties can only be accessed through further sub-properties
'''
ActiveHomePage.Title
KeyboardPage.Title
PreferredGridDimensions.Items  #returns a list of the optimized grid dimensions for this pageset (not a true list)
OffscreenButton1Commands    #this property is an interable list of commands (with only 1 item).
                            #Each command has a .DescriptionKey property that can be accessed and explains the key
OffscreenButton2Commands    #same as above
'''


# WRITING TO A TEXT FILE
# To output to a text file
with open(filePath, "w", encoding="utf-8") as file: #specify encoding if working with any international strings. "w" means  write (overwrite), "a" means append
    file.write(jsonString)
# By using "with open" you don't have to worry about closing the file. It will automatically close when you exit the with block
# 

# CONVERT LIST OR DICTIONARY TO JSON
import json
jsonString = json.dumps(dictionaryOrList, indent=4, ensure_ascii=False)  #ensure_ascii=False is needed to preserve international characters/ 


# CONVERT JSON TO LIST OR DICTIONARY
with open(file_path, "r", encoding="utf-8") as file:
    data = json.load(file) #json.load automatically determines whether it is a list or a dictionary by the json format and returns the appropriate object

# POPULATING A DICTIONARY ON THE FLY
from collections import defaultdict
dictionary = defaultdict(set) # creates a blank dictionary where each key is associated with a set of multiple unique values.
# can also use defaultdict(list) if you want each key to have a list of values where duplicates are allowed
# defaultdict() will automatically create a new key if it doesn't exist, i.e. dictionary['newkey'].append('newvalue')
# a normal dictionary dictionary = {} will not allow you to do this

# TO MAKE A DICTIONARY OF DICTIONARIES, I.E. ONE DICTIONARY FOR EACH LANGUAGE (very common in pagesets):
dictionary_of_dictionaries = {language: defaultdict(set) for language in languages} 
#In this case, must already know all keys of top level dictionary. Probably there is a way to do it on the fly --  maybe defaultdict(defaultdict(set))?