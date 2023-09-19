import snappy
import snappy.util
from Snap.Core.EntityModel import *
from Snap.Core.Common import PageSetQueries
from Snap.Core.Commands import *

from collections import defaultdict


#This function returns a list of all of the buttons that link to the specified page
def FindLinksToPage(pageSet,targetPage):
    if pageSet is None:
        pageSetPath = input("Enter the path to the page set: ")
        pageSet = PageSet(pageSetPath)
    if targetPage is None:
        targetPage = input("Enter the name of the target page: ")
    #create dictionary of all links to all pages
    allPages = pageSet.AllPages()
    linksToPage = []
    print(f'[pageName]/[buttonLabel]')
    for page in allPages:
        for button in page.Buttons:
            for command in button.CommandSequence.Commands:
                if type(command) == Link:
                    linkedPageTitle = pageSet.GetPageName(command.LinkedPageId)
                    if linkedPageTitle == targetPage:
                    #if button.LinkedPage() and button.LinkedPage().Title == targetPage:
                        linksToPage.append(f'{page.Title}/{button.Label}')
                        print(f'{page.Title}/{button.Label}')
    if len(linksToPage) == 0:
        print(f'There are no links to page "{targetPage}"')
    return linksToPage



FindLinksToPage(None, None)

