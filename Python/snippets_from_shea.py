# Mvx.Resolve something
from MvvmCross.Platform import Mvx
from Plugin.Utilities import IAppPaths
ReadonlyAppDataDir = Mvx.Resolve[IAppPaths]().ReadonlyAppDataDir
print("ReadonlyAppDataDir =", ReadonlyAppDataDir)

# another example
from MvvmCross.Platform import Mvx
from MvvmCross.Plugins.File import IMvxFileStore
fileStore = Mvx.Resolve[IMvxFileStore]()

# create a language model
from Tdx.LanguageModel.Core import ILanguageModelProvider
from MvvmCross.Platform import Mvx
languageModelProvider = Mvx.Resolve[ILanguageModelProvider]()
lm = languageModelProvider.GetLanguageModel('en_US')
list(lm.GetAllForms('saw'))


# create an Action<string> callback that can be passed to a c# function
import System
def myLogger(x):
    print('...', x)
loggerAction = System.Action[str](myLogger)
# another way (inline)
loggerAction = System.Action[str](lambda x: print('...', x))


# print all pages in page set
# path = ...
from Snap.Core.EntityModel import *
with PageSet(path) as pageSet:
    for p in pageSet.AllPages():
        print(p.Title)


# list Grammar buttons on a page
# page = ...
from Snap.Core.Common import ButtonContentType
for button in page.Buttons:
    if button.ContentType == ButtonContentType.Grammar:
        print(button.Label)


# list buttons on a page that link to another page
# page = ...
from Snap.Core.Commands import *
for button in page.Buttons:
    for command in button.CommandSequence.Commands:
        if type(command) == Link:
            linkedPageGuid = command.LinkedPageId
            print(f'{button.Label} -> {linkedPageGuid}')


# use MessageText() function to build a set of all of the words in the page set
allWords = set(MessageText(b) for p in pageSet.AllPages() for b in p.Buttons)
allWords.remove(None)

# use MessageText() function to build a wordCounts histogram of all words in the page set
from collections import Counter
wordCounts = Counter(MessageText(b) for p in pageSet.AllPages() for b in p.Buttons)
wordCounts.pop(None)

# use wordCounts to find duplicated words
for word, count in wordCounts.items():
    if count != 1:
        print(f'{word} => {count}')


# use a language model to inflect words
from snappy.util import GetLanguageModel

language = 'es'
words = ['ir', 'seguir', 'comprar', 'encontrar', 'recordar', 'ser']

languageModel = GetLanguageModel(language)
inflector = languageModel.GetInflector("VERB:VIP3S") # indicative third person singular present
print(languageModel.GetLocalizedInflectorString(languageModel.Name, inflector.Name))

for word in words:
    wordToken = languageModel.FactoryWordToken(word)
    inflectedWordToken = inflector.TryInflect(wordToken)
    if inflectedWordToken:
        inflectedWord = inflectedWordToken.Text
    else:
        inflectedWord = None
    print(f'{word} => {inflectedWord}')


def ComputePageDepths(pageSet):
    """
    This function returns a dictionary where keys are Page objects and values are
    the shortest distance from the home page.
    """
    from collections import deque

    pagesDict = dict()
    stack = deque()
    stack.append((pageSet.HomePage(), 0))

    while stack:
        page, depth = stack.pop()
        
        if page in pagesDict:
            continue
        
        pagesDict[page] = depth

        for button in page.Buttons:
            linkedPage = button.LinkedPage()
            if linkedPage:
                stack.append((linkedPage, depth + 1))

    return pagesDict


