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


# TO CLOSE A PAGE SET
# once you load a page set using the PageSet() function, it will lock up the file until you quit iPython or close the page set.
# You can close it manually with the following:
pageSet = PageSet(path) #loads pageset into variable pageSet
pageSet.Dispose() #closes pageset
del pageSet #clears variable from namespace memory


# TO GET ALL PAGES IN PAGE SET 
pages = pageSet.AllPages() #Returns a list of all pages in the pageset
# Note: not a true list
# but an iterable object containing all the pages. You cannot index into it like a list
# i.e. pages[0] will not work
# NOTE#2: .AllPages() returns a Generator object. This is an iterable function that can only be iterated through once. After you have iterated through it, it is empty
# and will not return anything, so you will need to reload the generator to iterate through it again. You can see that it is a generator by just entering pageSet.AllPages() 
# in iPython and seeing the output. It will say <generator object _allPages at....>, telling you it is a generator.

# TO GET SPECIFIC PAGE
page = pageSet.PageWithTitle(pageTitle) #Returns the page with the given title


# TO GET ALL BUTTONS ON A PAGE
buttons = page.Buttons #Returns a list of all buttons on a page (not a true list)
# Note: this is a Collection object, which is an iterable object that can be indexed into like a list. Unlike the Generator object, it can be iterated through multiple times
# You can see this by typing page.Buttons in iPython. It will say <System.Collections.Generic.IEnumerable[Button] object...>, telling you it is a Collection object.


#TO GET ALL BUTTON SYMBOLS IN A PAGE SET
buttonSymbols = pageSet.ButtonSymbols() #Returns a list of all button symbols in the pageset as a list of tuples
#each entry has format ([label], [symbolId]), i.e. ('cucumber', 578)

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
UniqueId
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
#NOTE: DO NOT USE page.Id -- Id values are for internal reference only and can change. Use page.UniqueId (need .ToString() to view it) if you need to reference an exact page

# TO ACCESS BUTTON PROPERTIES
button.Label
button.SymbolId() # use this rather than button.Image
button.BackgroundColor.Serialize() #returns color using Snap color values (what you see in the SQL database)
button.BackgroundColor.ToString() #returns color in argb format as string, i.e. 'argb: #FFAF95D1'
button.BackgroundColor.ToHSV() #returns color in HSV (hue/saturation/value) format as tuple, i.e. (189, 73, 209)
button.ElementReference #returns the ElementReference of the button
button.ContentType.ToString() #returns the content type of the button, i.e. 'Regular', 'Grammar', etc
#NOTE: DO NOT USE button.Id -- Id values are for internal reference only and can change. Use button.UniqueId (need .ToString() to view it) if you need to reference an exact button

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



#DOCUMENTATION FOR THE GIT DIFFTOOL THAT IS INTEGRATED INTO SNAPPY. 
#It generates a text representation of the page set (currently only Motor Plan) that can be compared using a text diff tool
#so you can quickly see the changes that were made across different versions.
"""
This script supports comparison of two page sets (.sps files) by generating
text representations which can be compared using a typical diff tool.

Usage:
python -m snappy.util.spsdiff <local.sps> <remote.sps> <difftool> <additional difftool args...>

<local.sps>
The path to version A of the page set.

<remote.sps>
The path to version B of the page set.

<difftool>
A diff tool program to invoke for comparison of text files.

<additional difftool args...>
Arguments with which to invoke the difftool. At a minimum these would include
the paths to two files to compare. Instances <local.sps> and <remote.sps> will
be automatically replaced with generated text representation files. If no
additional difftool arguments are provided <local.sps> <remoted.sps> will be
used by default. 

Git Integration
===============
This script is designed to be directly integrated with git, so that it can be
invoked using "git difftool ..." to compare various versions of page set files
in a repo. To do this, spsdiff must be declared as a difftool that can be used
by git through the .gitconfig file. Take these lines added to .gitconfig as a
concrete example:

[difftool "spsdiff"]
    cmd=python -m snappy.util.spsdiff \"$LOCAL\" \"$REMOTE\" meld \"$LOCAL\" \"$REMOTE\"

This example declares spsdiff as a difftool available to git. spsdiff uses
meld as the difftool to display text representations of page sets, which it
invokes with two file arguments.

With this example configuration the following can invoked to compare unstaged
changes to MyPageSet.sps:
git difftool -t spsdiff MyPageSet.sps

Similarly two committed versions of a MyPageSet.sps can be compared using:
git difftool -t spsdiff <commit-hash1> <commit-hash2> MyPageSet.sps

To compare the current version of MyPageSet.sps to the previous commit:
git difftool -t spsdiff HEAD~ MyPageSet.sps
"""
You can probably just pay attention the section on git integration.

#TO INSTALL: Add the following to your .gitconfig file under /users/[username]/.gitconfig
#You also will need to install the Meld text comparison tool, available at https://meld.app/
'''
[difftool "spsdiff"]
    cmd=python -m snappy.util.spsdiff \"$LOCAL\" \"$REMOTE\" Meld \"$LOCAL\" \"$REMOTE\"
    '''
