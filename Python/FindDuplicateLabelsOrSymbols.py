import snappy
import snappy.util
from Snap.Core.EntityModel import *
from Snap.Core.Common import PageSetQueries
import argparse
import sys
import os
from collections import defaultdict



"""
This script finds labels in a page set that
are associated with more than one button.
"""

parser = argparse.ArgumentParser(description="Allow flat to specify whether to check for duplicates of symbols, labels, or both.")

# Add arguments with optional flags
parser.add_argument("action", nargs="?", default="default_action", help="Specify an action")
parser.add_argument("--label", action="store_true", help="Check for duplicate labels")
parser.add_argument("--symbol", action="store_true", help="Check for duplicate symbols")

args = parser.parse_args()

exceptions = ['!','.','0','1','10','10:00','11','11:00','12','12:00','13','14','15','16','17','18','19','1:00','2','20','2:00','3','3:00','4','4:00','5','5:00','6','6:00','7','7:00','8','8:00','9','9:00','?','A','A.M.','Abrir pizarra','Actividades de Boardmaker','Alexa','Alexa, baja el volumen','Alexa, cuelga','Alexa, hang up','Alexa, para','Alexa, play messages','Alexa, stop','Alexa, sube el volumen','Alexa, toca mis mensajes','Alexa, turn down volume','Alexa, turn up volume','Apoyos','Asia','Asistente de Google','Atrás','Australia','B','Back','Bajar volumen','Be quiet','C','Calibrar','China','Cinco de Mayo','Coca-Cola','Colombia','Controles del hogar','Copiar en botón','Copy to Button','Cosas divertidas','Costa Rica','D','DVD','Delete','E','F','Facebook','Fun Stuff','G','Google','H','Hey Siri, cancel','Hey Siri, next','Hey Siri, play','Hey Siri, previous','Hey Siri, turn down the volume','Hey Siri, turn up the volume','Home','Home Controls','India','Información','Information','Inicio','Israel','J','Jamaica','K','Kwanzaa','L','Lento: 1.2s','M','Medio: 1.0s','Mensajes','Mostrar estado','Move backward by character','Move forward by character','N','No','No device required. You must be signed into a Google account in Snap under Settings>User.','No requiere un dispositivo extra. Debe ingresar a su cuenta Google desde Snap en Configuración> Usuario.','O','Ok Google',' ','Ok Google, baja el volumen','Ok Google, sube el volumen','Ok Google, turn down the volume','Ok Google, turn up the volume','Oye Siri, anterior','Oye Siri, baja el volumen','Oye Siri, cancela','Oye Siri, para','Oye Siri, sigue','Oye Siri, siguiente','Oye Siri, sube el volumen','P','P.M.','PE','Pepsi','Pon el volumen','Portugal','Puerto Rico','Q','R','Rápido: 0.8s','S','Set volume','Silencio','Siri','Social Studies','Speak','Subir volumen','Sí','T','TV','Temporizador visual','Twitter','U','V','Venezuela','Venus','W','X','Y','Yes','YouTube','Z','Zoom']


for path in snappy.util.argPageSetsPaths():
    with PageSet(path) as pageSet:

        filename = os.path.basename(path)
        print(f'\n\n{filename}')

        pages = pageSet.AllPages()
        #get all languages in pageset
        languages = list(PageSetQueries.GetPageSetLanguages(pageSet))
        #create a dictionary for each language of all of the labels used in the pageset and the buttons and pages they are used in
        labelDict = {language: defaultdict(set) for language in languages}
        #create a dictionary for each language of all of the symbols used in the pageset and the buttons and pages they are used in
        symbolDict = {language: defaultdict(set) for language in languages}
        for page in pages:
            if page.Language:
                if page.Language in ['rw_RW','neut']: #if pagel language is 'rw_RW' (AccessIT mouse page) or 'neut', use the page set language
                    currentLang = pageSet.Language
                elif page.Language not in languages:
                    currentLang = pageSet.Language
                    print(f'\n***\n{page.Title} has a language that does not match the page set language(s): {page.Language}\n***')
                    continue
                else:
                    currentLang = page.Language
            else:
                currentLang = pageSet.Language #if page language is None, use the page set language
            currentLabelDict = labelDict[currentLang] #store values in dictionary for currentLang
            currentSymbolDict = symbolDict[currentLang]
            buttons = page.Buttons
            for button in buttons:
                #only include regular and grammar buttons
                if button.ContentType.ToString() in ['Regular', 'Grammar']:
                    #get label & symbol for each button
                    label = button.Label
                    if button.Image:
                        symbol = button.Image.Identifier
                    else:
                        symbol = None
                    if label and label not in exceptions:
                        currentLabelDict[label].add(page.Title)
                    if symbol:
                        currentSymbolDict[symbol].add((button.Id, page.Title))
        #create list for each language of labels used more than once
        labelDupes = {language: [] for language in languages}
        symbolDupes = {language: [] for language in languages}
        for lang in languages:
            labelDupes[lang] = [(i[0], list(i[1])) for i in labelDict[lang].items() if len(i[1]) > 1]
            symbolDupes[lang] = [(i[0], list(i[1])) for i in symbolDict[lang].items() if len(i[1]) > 1]
        if args.label or args.action == 'default_action':
            #print labels used more than once
            # Check if any of the label dictionary entries have non-empty lists
            duplicatesExist = any(len(list) > 0 for list in labelDupes.values())
            if duplicatesExist:
                print(f'\n***\nDUPLICATE LABELS\n***')
                for lang in languages:
                    print(f'\n***\n{lang}:\n***')
                    print(f'\n{len(labelDupes[lang])} labels used one more than one button label\n')
                    for label, pages in sorted(labelDupes[lang],key=lambda x: x[0]):
                        print(f'\n{label}:')
                        for page in sorted(pages):
                            print(f'\t{page}')
        if args.symbol:
            #print symbols used more than once
            # Check if any of the symbol dictionary entries have non-empty lists
            duplicatesExist = any(len(list) > 0 for list in symbolDupes.values())
            if duplicatesExist:
                print(f'\n***\nDUPLICATE LABELS\n***')
                for lang in languages:
                    print(f'\n***\n{lang}:\n***')
                    print(f'\n{len(symbolDupes[lang])} symbols used one more than one button label\n')
                    for symbol, locations in sorted(symbolDupes[lang],key=lambda x: x[0]):
                        print(f'\n{symbol}:')
                        for loc in sorted(locations, key=lambda x: x[1]):
                            print(f'\t{loc}')

