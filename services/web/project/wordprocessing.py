
import ebooklib
from ebooklib import epub
import re

def read_epub_file(filepath):
    book = epub.read_epub(filepath)
    # Example: extract all text from the epub
    text_content = []
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            text_content.append(item.get_content().decode('utf-8', errors='ignore'))
    print(f"text content = {text_content}")
    return '\n'.join(text_content)

def word_frequency_analysis(alltext):
    # Simple word frequency analysis using regex to split words
    alltext = re.sub(r'<[^>]+>', '', alltext)     # remove html tags
    words = re.findall(r'\b\w+\b', alltext.lower())
    frequency = {}
    for word in words:
        frequency[word] = frequency.get(word, 0) + 1
    # Sort by frequency
    sorted_freq = sorted(frequency.items(), key=lambda item: item[1], reverse=True)
    sorted_dict = {word: count for word, count in sorted_freq}
    return sorted_dict