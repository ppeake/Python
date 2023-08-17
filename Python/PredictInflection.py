import snappy
from MvvmCross.Platform import Mvx
from Tdx.LanguageModel.Core import ILanguageModelProvider

# pick a language and model version
language = 'en_US'
model = 1

languageModelProvider = Mvx.Resolve[ILanguageModelProvider]()
languageModel = languageModelProvider.GetLanguageModel(language)

while True:
    context = input('Enter preceding context: ')
    if not context:
        break

    contextTokens = languageModel.WordTokenize(context)
    inflector = languageModel.GetPredictiveInflector(contextTokens, model)
    
    while True:
        word = input('Enter word to inflect: ')
        if not word:
            break

        wordToken = languageModel.FactoryWordToken(word)
        inflectedWordToken = inflector.TryInflect(wordToken)
        
        if not inflectedWordToken:
            inflectedWord = word.upper() # fallback
        else:
            inflectedWord = inflectedWordToken.Text

        print(f'{context} [ {inflectedWord} ]\n')
