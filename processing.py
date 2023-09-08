import subprocess
import sys
import json
print("Installing necessary libs..")
# Install nltk
subprocess.check_call([sys.executable, "-m", "pip", "install", "nltk"])
# Install pymystem3
subprocess.check_call([sys.executable, "-m", "pip", "install", "pymystem3"])

import nltk
from nltk.corpus import stopwords
import string
import re

# Mystem Initialisation
from pymystem3 import Mystem
m = Mystem()
def lemmatize_sentence(text) -> str:
    lemmas = m.lemmatize(text)
    return "".join(lemmas).strip()

def deEmojify(text) -> str:
    regrex_pattern = re.compile(pattern = "["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags = re.UNICODE)
    return regrex_pattern.sub(r'',text)

def isEnglish(text, alphabet=set('абвдеёжзийклмнопрстуфхцчшщъыьэюя')) -> bool:
    '''
    print(isEnglish('test')) # True
    print(isEnglish('тест')) # False
    print(isEnglish('123Ы')) # False
    print(isEnglish(''))     # True
    '''
    return alphabet.isdisjoint(text.lower())

def filter(OLDFILE_PATH, NEWFILE_PATH):
    '''
    Read a list of names from a file line by line into an output file.
    '''
    nltk.download("stopwords")
    stop_words = stopwords.words("russian")
    print("\n\n\n\n Starting filtering..")
    print("Working with file", OLDFILE_PATH, "\n\n")

    
    with open(NEWFILE_PATH, 'w') as outfile, open(OLDFILE_PATH, 'r', encoding='utf-8-sig') as infile:
        for questions in json.load(infile):
            for line in questions['answers']:
                line = line['answer']
                # To lowercase
                outline = line.lower()

                # Remove punctuation
                outline = "".join(u if u not in (string.punctuation+'«»…') else ' ' for u in outline)

                # Remove numbers
                outline = re.sub(r'\w*\d+\w*', '', outline)

                # Remove Emoji
                outline = deEmojify(outline)

                # Remove links
                outline = re.sub("https*\S+", " ", outline)

                # Remove English words
                outline = " ".join(u for u in outline.split() if not isEnglish(u))

                # Replace the over spaces
                outline = re.sub('\s{2,}', " ", outline)

                # Remove stop-words with NLTK
                outline = ' '.join([word for word in outline.split(' ') if word not in stop_words])

                # Contextual Lemmatisation by pymystem3
                outline = lemmatize_sentence(outline)

        outfile.write(json.dumps(infile, indent=4))
        print(f'Done - {NEWFILE_PATH}')
            
