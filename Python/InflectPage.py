import snappy
import snappy.util
from snappy.util import GetLanguageModel
from Snap.Core.EntityModel import *
from Snap.Core.Common import PageSetQueries

#GENERATES SQL SCRIPT TO CHANGE ALL BUTTONS ON SPECIFIED PAGES TO A SPECIFIED INFLECTION
path = r"C:\Users\ytao\Documents\SnapPageSets\MotorPlan30-es_US-en_US\MotorPlan30-es_US-en_US.sps"
language = 'es'
targetInflection = "VERB:VR" # infinitive
ignoreList = ["Inicio"] #list of labels to ignore
languageModel = GetLanguageModel(language)
inflector = languageModel.GetInflector(targetInflection)
print(languageModel.GetLocalizedInflectorString(languageModel.Name, inflector.Name))

pageSet = PageSet(path)
pages = pageSet.AllPages()
for page in pages:
    if "Acciones:" in page.Title:
        buttons = page.Buttons
        for button in buttons:
            label = button.Label
            wordToken = languageModel.FactoryWordToken(label)
            inflectedWordToken = inflector.TryInflect(wordToken)
            if inflectedWordToken is not None and label not in ignoreList:
                inflectedWord = inflectedWordToken.Text
                print(f'UPDATE Button SET Label = "{inflectedWord}" WHERE UniqueId = "{button.UniqueId}";')
                #print(f'--{label} -> {inflectedWord}')
            else:
                inflectedWord = None
