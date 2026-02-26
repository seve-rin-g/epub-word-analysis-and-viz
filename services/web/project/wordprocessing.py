
import re
import ebooklib
from ebooklib import epub
import nltk
from nltk.stem import WordNetLemmatizer

# Download required NLTK data if not already present
try:
    nltk.data.find('corpora/wordnet')
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('taggers/averaged_perceptron_tagger')
except LookupError:
    nltk.download('wordnet')
    nltk.download('punkt')
    nltk.download('averaged_perceptron_tagger')
    
from nltk.corpus import wordnet as wn

def read_epub_file(filepath):
    book = epub.read_epub(filepath)
    # Example: extract all text from the epub
    text_content = []
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            text_content.append(item.get_content().decode('utf-8', errors='ignore'))
    return '\n'.join(text_content)

def word_frequency_analysis(alltext):
    # Simple word frequency analysis using regex to split words
    alltext = re.sub(r'<[^>]+>', '', alltext)     # remove html tags
    words = re.findall(r'\b\w+\b', alltext.lower()) # regex version
    pos_tagged = nltk.pos_tag(words)
    frequency = {}
    for word, pos in pos_tagged:
        if word.isdigit():
            continue    
        stemmedword = WordNetLemmatizer().lemmatize(word, get_wordnet_pos(pos[0].upper())) # stem the word to its root form
        frequency[stemmedword] = frequency.get(stemmedword, 0) + 1
    # Sort by word
    sorted_freq = sorted(frequency.items(), key=lambda item: item[0])
    
    return sorted_freq

def semantic_grouping(word_freq):
    # Placeholder for semantic grouping logic
    # use NLTK or spaCy to determine word meanings and group them
    return word_freq

def get_wordnet_pos(treebank_tag):
        """
        return WORDNET POS compliance to WORDENT lemmatization (a,n,r,v) 
        """
        if treebank_tag.startswith('J'):
            return wn.ADJ
        elif treebank_tag.startswith('V'):
            return wn.VERB
        elif treebank_tag.startswith('N'):
            return wn.NOUN
        elif treebank_tag.startswith('R'):
            return wn.ADV
        else:
            # As default pos in lemmatization is Noun
            return wn.NOUN
