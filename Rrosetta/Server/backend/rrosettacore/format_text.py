import string
import re
import nltk
from nltk.corpus import stopwords

def remove_symbols(_sentence):
    tokens = [token for token in _sentence.split(sep=' ') if token.isalpha()]
    
        
    









