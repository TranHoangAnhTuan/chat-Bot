import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet

# download required resources

def extract_nouns(document):
    # example English text

    # tokenize the text into words
    words = word_tokenize(document)
    # identify the parts of speech for each word
    pos_tags = nltk.pos_tag(words)

    # extract the nouns
    nouns = [word for word, pos in pos_tags if (pos == 'NN' or pos == 'NNS' or pos == 'NNP' or pos == 'NNPS') and len(word) > 1]
    # nouns = [word for word, pos in pos_tags if (pos == 'NN')]
    

    # print the list of nouns
    return nouns

# Import required libraries
import nltk

from nltk import pos_tag, word_tokenize, RegexpParser

# Example text
sample_text = "what the types of supervised learning ?"

# Find all parts of speech in above sentence
tagged = pos_tag(word_tokenize(sample_text))

#Extract all parts of speech from any text
import nltk

# define a grammar to extract noun phrases
grammar = r"""
  NP: {<DT|PRP\$>?<JJ|VBN.*>*<NN|VBG.*>+} # chunk determiners, possessive pronouns, adjectives, and nouns
      {<NNP>+} # chunk consecutive proper nouns
      {<PRP>} # chunk personal pronouns
      {<VBN.*>+<NN|VBG.*>+} # chunk past participle verb followed by a noun
      {<CD>+<NNS|NN>}
      {<NNS|NN>}# chunk cardinal numbers followed by a plural or singular noun
"""

# create a chunk parser with the grammar
chunk_parser = nltk.RegexpParser(grammar)

# tokenize a sentence and POS tag it
sentence = "what is supervised learning"
def extract_nouns_phrase(sentence):
    tokens = nltk.word_tokenize(sentence)
    pos_tags = nltk.pos_tag(tokens)

    # parse the POS tags to extract noun phrases
    nouns_phrase = []
    tree = chunk_parser.parse(pos_tags)
    for subtree in tree.subtrees():
        if subtree.label() == 'NP':
            
            nouns_phrase.append(' '.join(word for word, tag in subtree.leaves()))

    return nouns_phrase

# print(extract_nouns_phrase(sentence))

# print(pos_tag(['learning']))
