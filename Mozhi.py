'''
Library Codes for Mozhi
'''

# Imports
import json
import requests
from textblob import TextBlob

# Module Functions
def text_to_handwriting(string: str, save_to: str = "pywhatkit.png", rgb: list = [0, 0, 138]) -> None:
    data = requests.get(
        "https://pywhatkit.herokuapp.com/handwriting?text=%s&rgb=%s,%s,%s" % (string, rgb[0], rgb[1], rgb[2])).content
    file = open(save_to, "wb")
    file.write(data)
    file.close()

# Main Vars
LANGUAGES_NAMES_MAP = json.load(open("Data/LanguageCodes.json", "r"))
POS_TAGS_MAP = json.load(open("Data/PosTags.json", "r"))

# Main Functions
def Text2Handwriting(text, savePath="handwriting.png", color=(0, 0, 0)):
    text_to_handwriting(text, save_to=savePath, rgb=color)

def SpellCorrect(text):
    return str(TextBlob(text).correct())

def TranslateText(text, toLang, fromLang="auto"):
    return str(TextBlob(text).translate(from_lang=fromLang, to=toLang))

def GetTextAnalysis(text):
    textData = TextBlob(text)
    analysisData = {}
    analysisData["language"] = str(textData.detect_language()) #NEEDED
    # analysisData["ngrams"] = textData.ngrams
    # analysisData["nouns"] = textData.noun_phrases
    # analysisData["polarity"] = textData.polarity
    analysisData["pos_tags"] = textData.pos_tags #NEEDED
    # analysisData["sentiment"] = textData.sentiment
    analysisData["sentiment_assessments"] = textData.sentiment_assessments #NEEDED
    # analysisData["subjectivity"] = textData.subjectivity
    analysisData["word_counts"] = dict(textData.word_counts) #NEEDED
    # analysisData["words"] = textData.words
    # analysisData["tokens"] = textData.tokens
    return analysisData

# Driver Code