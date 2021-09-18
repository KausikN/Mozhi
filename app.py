"""
Stream lit GUI for hosting Mozhi
"""

# Imports
import streamlit as st
import json
import matplotlib.pyplot as plt

import Mozhi

# Main Vars
config = json.load(open('./StreamLitGUI/UIConfig.json', 'r'))

# Main Functions
def main():
    # Create Sidebar
    selected_box = st.sidebar.selectbox(
    'Choose one of the following',
        tuple(
            [config['PROJECT_NAME']] + 
            config['PROJECT_MODES']
        )
    )
    
    if selected_box == config['PROJECT_NAME']:
        HomePage()
    else:
        correspondingFuncName = selected_box.replace(' ', '_').lower()
        if correspondingFuncName in globals().keys():
            globals()[correspondingFuncName]()
 

def HomePage():
    st.title(config['PROJECT_NAME'])
    st.markdown('Github Repo: ' + "[" + config['PROJECT_LINK'] + "](" + config['PROJECT_LINK'] + ")")
    st.markdown(config['PROJECT_DESC'])

    # st.write(open(config['PROJECT_README'], 'r').read())

#############################################################################################################################
# Repo Based Vars
LANGUAGES_NAMES_MAP = Mozhi.LANGUAGES_NAMES_MAP
POS_TAGS_MAP = Mozhi.POS_TAGS_MAP

TEXTAREA_HEIGHT = 250

# Util Functions
def HorizontalFigure(stw, title, names, values, lims=[-1.0, 1.0], thickness=0.1):
    fig_HFigure = plt.figure()
    plt.grid(True)
    plt.xlim(lims)
    plt.barh(names, values, height=thickness)
    plt.title(title)
    for index, value in enumerate(values):
        plt.text(value, index, str(round(value, 4)))
    
    stw.pyplot(fig_HFigure)

# UI Functions
def UI_WordCountAnalysis(WordData):
    st.markdown("### Word Frequency Analysis")

    words = list(WordData.keys())
    counts = []
    for w in words:
        counts.append(WordData[w])
    zipped_lists = zip(counts, words)
    sorted_pairs = sorted(zipped_lists, reverse=True)
    tuples = zip(*sorted_pairs)
    counts_sorted, words_sorted = [list(t) for t in  tuples]

    fig_WordCount = plt.figure()
    plt.grid(True)
    plt.bar(words_sorted, counts_sorted)
    st.pyplot(fig_WordCount)

def UI_SentimentAnalysis(SentimentData):
    st.markdown("### Sentiment Analysis")

    st.markdown("#### Overall Sentiment")
    col1, col2 = st.columns(2)
    polarity = SentimentData.polarity
    subjectivity = SentimentData.subjectivity
    HorizontalFigure(col1, 'Overall Polarity', ['Polarity'], [polarity], lims=[-1.0, 1.0], thickness=0.01)
    HorizontalFigure(col2, 'Overall Subjectivity', ['Subjectivity'], [subjectivity], lims=[0.0, 1.0], thickness=0.01)

    st.markdown("#### Words Sentiment")
    col1, col2 = st.columns(2)
    assessments = SentimentData.assessments
    wordGroups = []
    polarities = []
    subjectivities = []
    for a in assessments:
        wordGroups.append(','.join(list(a[0])))
        polarities.append(float(a[1]))
        subjectivities.append(float(a[2]))

    HorizontalFigure(col1, 'Word Polarity', wordGroups, polarities, lims=[-1.0, 1.0])
    HorizontalFigure(col2, 'Word Subjectivity', wordGroups, subjectivities, lims=[0.0, 1.0])

def UI_LanguageAnalysis(LanguageData):
    st.markdown("### Language Analysis")
    LanguageName = 'Unknown'
    for l in LANGUAGES_NAMES_MAP.keys():
        if LANGUAGES_NAMES_MAP[l].lower() == LanguageData.lower():
            LanguageName = l
    col1, col2 = st.columns(2)
    col1.markdown("Language of the text: ")
    col2.markdown(LanguageName)

# Repo Based Functions
def text_analyser():
    # Title
    st.header("Text Analyser")

    # Load Inputs
    USERINPUT_text = st.text_area("Enter Text", "Hello World!", height=TEXTAREA_HEIGHT)

    # Process Inputs
    AnalysedData = Mozhi.GetTextAnalysis(USERINPUT_text)
    LanguageData = AnalysedData['language']
    PosTagsData = AnalysedData['pos_tags']
    SentimentData = AnalysedData['sentiment_assessments']
    WordData = dict(AnalysedData['word_counts'])

    # Display Outputs
    st.markdown("## Analysis")
    col1, col2 = st.columns(2)
    USERINPUT_AnalysisChoice = col1.selectbox("Analysis", list(AnalysedData.keys()))
    col2.text_area("Analysis Data", str(AnalysedData[USERINPUT_AnalysisChoice]))
    UI_LanguageAnalysis(LanguageData)
    UI_WordCountAnalysis(WordData)
    UI_SentimentAnalysis(SentimentData)

def spelling_corrector():
    # Title
    st.header("Correct Spelling")

    # Load Inputs
    USERINPUT_text = st.text_area("Enter Text", "Hello World!", height=TEXTAREA_HEIGHT)

    # Process Inputs
    SpellCorrectedText = Mozhi.SpellCorrect(USERINPUT_text)

    # Display Outputs
    USERINPUT_text = st.text_area("Corrected Text", SpellCorrectedText, height=TEXTAREA_HEIGHT)

def translate_text():
    # Title
    st.header("Translate Text")

    # Load Inputs
    USERINPUT_text = st.text_area("Enter Text", "Hello World!", height=TEXTAREA_HEIGHT)
    USERINPUT_toLanguageName = st.selectbox("Target Language", list(LANGUAGES_NAMES_MAP.keys()))
    
    # Process Inputs on Button Click
    # if st.button('Translate'):
    USERINPUT_toLang = LANGUAGES_NAMES_MAP[USERINPUT_toLanguageName]
    TranslatedText = Mozhi.TranslateText(USERINPUT_text, USERINPUT_toLang)

    # Display Outputs
    USERINPUT_text = st.text_area("Translated Text", TranslatedText, height=TEXTAREA_HEIGHT)
    
#############################################################################################################################
# Driver Code
if __name__ == "__main__":
    main()