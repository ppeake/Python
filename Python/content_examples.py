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

