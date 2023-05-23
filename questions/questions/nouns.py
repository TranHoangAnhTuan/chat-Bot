import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet
from copy import copy
# download required resources

def remove_determiners(sentence):
    tokens = word_tokenize(sentence)
    tagged_tokens = nltk.pos_tag(tokens)
    
    determiners = ['DT']  # Determiner part-of-speech tag
    
    # Filter out tokens that are not determiners
    filtered_tokens = [token for token, tag in tagged_tokens if tag not in determiners]
    
    # Reconstruct the sentence without determiners
    cleaned_sentence = ' '.join(filtered_tokens)
    
    return cleaned_sentence

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
def extract_nouns_phrase(sentence):
    tokens = nltk.word_tokenize(sentence)
    pos_tags = nltk.pos_tag(tokens)

    # parse the POS tags to extract noun phrases
    nouns_phrase = []
    tree = chunk_parser.parse(pos_tags)
    for subtree in tree.subtrees():
        if subtree.label() == 'NP' :
            
            nouns_phrase.append(' '.join(word for word, tag in subtree.leaves()))

    return nouns_phrase

def extract_noun_phrases2(sentence):
    tokens = nltk.word_tokenize(sentence)
    pos_tags = nltk.pos_tag(tokens)

    # parse the POS tags to extract noun phrases
    noun_phrases = []
    start_index = 0
    for i in range(len(pos_tags)):
        word, tag = pos_tags[i]
        if tag.startswith('NN'):  # Check if the word is a noun
            if i > 0 and pos_tags[i - 1][1].startswith('NN'):  # Check if the previous word is also a noun
                continue
            j = i + 1
            while j < len(pos_tags) and pos_tags[j][1].startswith('NN'):  # Find the end of the noun phrase
                j += 1
            noun_phrase = ' '.join(word for word, _ in pos_tags[i:j])
            noun_phrases.append(noun_phrase)

    return noun_phrases


def remove_duplicate_noun(list_np):
    one_word = set()
    noun_phrase = set()
    res_list = copy(list_np)
    for np in list_np:
        if len(np.split(' ')) < 2:
            one_word.add(np)    
        else:
            noun_phrase.add(np)

    for w in one_word:
        
        for np in noun_phrase:
            if w.lower() in np.lower():
                res_list.remove(w)
                print(w)
                break
            
                
    return res_list
            
# list =  ['strategic game', 'simulations', 'cars', 'learning', 'Colloquially', 'computers', 'device', 'capabilities', 'actions', 'field', 'phenomenon', 'agents', 'its chance', 'achieving', 'functions', 'understanding human speech', 'content delivery', 'humans', 'Tesler', 'contrast', 'natural intelligence', 'Leading', 'intelligence', 'networks', 'human mind', 'Theorem', 'goals', 'effect', 'computer science', 'instance', 'things', 'chess', '.As', 'problem solving', 'definition', 'routine technology', 'competing', 'Go', 'its environment', 'term', 'tasks', 'operating', 'machines', 'animals', 'having', 'optical character recognition', 'textbooks', 'AI', 'level', 'Modern machine', 'systems', 'machine intelligence', 'study', 'intelligent routing', 'artificial intelligence', 'quip']


# # # print(list)
# newlist = remove_duplicate_noun(set(list))
# print(newlist)



# print('ai' in 'aaei')
        
# sentence = "The quick brown fox jumps over the lazy dog."
# cleaned_sentence = remove_determiners(sentence)
# print(cleaned_sentence)
# print(extract_nouns_phrase(sentence))

# print(pos_tag(['learning']))




import nltk
from nltk.tokenize import word_tokenize, sent_tokenize

def classify_nouns(sentence):
    words = word_tokenize(sentence)
    tagged_words = nltk.pos_tag(words)

    private_nouns = []
    common_nouns = []

    for word, pos in tagged_words:
        if pos == 'NNP' or pos == 'NNPS':
            private_nouns.append(word)
        elif pos == 'NN' or pos == 'NNS':
            common_nouns.append(word)

    return private_nouns, common_nouns

# Example usage
# sentence = " When was Python 3.0 released?"
# private, common = classify_nouns(sentence)
# print("Private nouns:", private)
# print("Common nouns:", common)

# print(extract_noun_phrases2(sentence))


# import spacy
# nlp = spacy.load('en_core_web_sm')

def extract_pos(text):
    sentences = sent_tokenize(text)
    tagged_sentences = nltk.pos_tag_sents([word_tokenize(sent) for sent in sentences])
    pos_dict = {"adjective": [], "noun": [], "verb": []}

    for tagged_sent in tagged_sentences:
        for word, tag in tagged_sent:
            if tag.startswith('NN'):
                pos_dict["noun"].append(word)
            elif tag.startswith('JJ'):
                pos_dict["adjective"].append(word)
            elif tag.startswith('VB'):
                pos_dict["verb"].append(word)

    return pos_dict


text = "when was Python 3.0 released"
result = extract_pos(text)
print(result)