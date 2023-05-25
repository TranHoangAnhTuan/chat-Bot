import nltk
import sys
import os
import string
import math
import operator
from nouns import *
from nltk.corpus import stopwords
import re
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from collections import Counter

FILE_MATCHES = 1
SENTENCE_MATCHES = 3


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    # file_idfs = compute_idfs(copy(file_words))
    file_idfs = {}
    # new_ma_val = max(file_idfs.items(), key=operator.itemgetter(1))[0]

    # Prompt user for query
    query = input("Query: ")

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)
    
    print(filenames)
    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = nltk.word_tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens
              

    # Compute IDF values across sentences

    # Determine top sentence matches
    matches = top_sentences(query, sentences, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)

def is_link(string):
    # Regular expression pattern for URL matching
    pattern = re.compile(r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+")

    if re.match(pattern, string):
        return True
    else:
        return False


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    files = {}

    for filename in os.listdir(directory):
    # Get the full path of the file
        filepath = os.path.join(directory, filename)
        with open(filepath , "rb") as file:
            content = file.read()
            content = content.decode("utf-8")
            files[filename] = content.lower()

    return files
def have_common_char(str1, str2):
    for char in str1:
        if char in str2:
            return True
    return False

def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    tokens = nltk.word_tokenize(document, language='english')

    tokens = [token.lower() for token in tokens if not have_common_char(token, string.punctuation + "''")]

    # Remove stopwords
    stop_words = set(stopwords.words('english') + ['’']) 
    tokens = [token.lower() for token in tokens if token not in stop_words ]
 
    return tokens


def compute_tf(term, documents):
    """
    Compute the term frequency of a term across all documents in a dictionary.

    Arguments:
    term -- the term to compute the TF for
    documents -- a dictionary where keys are file names and values are lists of words in each file

    Returns:
    The term frequency of the term across all documents as a float.
    """
    # Convert the term to lowercase to make the search case-insensitive
    term = term.lower()

    # Get the count of the term across all documents
    term_count = 0
    for document in documents.values():
        term_count += document.count(term)

    # Compute the total number of terms across all documents
    total_terms = sum(len(document) for document in documents.values())

    # Compute the TF as the term count divided by the total number of terms
    tf = term_count

    return tf


def compute_idfs(noun_phrases, documents):
    """
    Given a list of `noun_phrases` and a `documents` dictionary where keys are
    document names and values are the content of each document, return a dictionary
    of IDF values for the noun phrases.

    Args:
        noun_phrases (list): A list of noun phrases.
        documents (dict): A dictionary containing the content of multiple documents.

    Returns:
        A dictionary of IDF values mapped to the noun phrases.
    """
    num_docs = len(documents)

    # Calculate the number of documents that contain each noun phrase
    phrase_counts = Counter()
    for document_content in documents.values():
        normalized_phrases = [noun_phrase.lower() for noun_phrase in noun_phrases]
        for phrase in normalized_phrases:
            if phrase in document_content.lower():
                phrase_counts[phrase] += 1

    # Calculate IDF for each noun phrase and store in a dictionary
    idf_values = {}
    for noun_phrase in noun_phrases:
        phrase_count = phrase_counts[noun_phrase]
        denominator = max(1, phrase_count)
        idf_values[noun_phrase] = math.log(num_docs / denominator)

    return idf_values
def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.      
    """
    
    raw_files = load_files(sys.argv[1])

    files = copy(files)
    # files_topic = {}
    # for filename in files:
    #     files_topic[filename] = {}
    #     NOUNS = extract_nouns(' '.join(files[filename]))
    #     for word in files[filename]:
    #         if word in idfs and word in NOUNS :
    #             files_topic[filename][word] = idfs[word] * compute_tf(word, {filename: files[filename]})
        
    #     files_topic[filename] = dict(sorted(files_topic[filename].items(), key=lambda item: item[1], reverse=True))


    introduction = {}

    for filename in raw_files:
        for passage in raw_files[filename].split("\n"):
            if is_link(passage) or len(passage) < 2:
                continue
            # print(passage)
            introduction[filename] = extract_nouns_phrase(passage)
            break

    # print(extract_nouns_phrase(introduction['artificial_intelligence.txt']))


    # remove  Det position and dup in noun pharse
    
    
    for file_name in introduction:
        introduction[file_name] = remove_duplicate_noun(introduction[file_name])
        temp = set()
        for np in introduction[file_name]:
            temp.add(remove_determiners(np))
        
        introduction[file_name] = temp
        temp = set()
        
        
    
    # print(remove_duplicate_noun(introduction["natural_language_processing.txt"]))
    
    
    # calculate tf-idf but base on noun pharse quantity
    top_pics = {}
    
    for filename in introduction:
        introduction[filename] = remove_duplicate_noun(introduction[filename])
        idfs = compute_idfs(introduction[filename], raw_files)
        top_pics[filename] = {}
        for np in introduction[filename]:
            if len(np.split(' ') )< 2:
                top_pics[filename][np] = raw_files[filename].count(np) * idfs[np]
            else:
                
                top_pics[filename][np] = pow(raw_files[filename].count(np) , len(np.split(' ') )) * idfs[np]


    sorted_idf_values = {}

    
    query = extract_pos(query)['noun']
    docs = []
    for doc, idf_dict in top_pics.items():
        sorted_idf_values[doc] = dict(sorted(idf_dict.items(), key=lambda x: x[1], reverse=True))
        
        for noun in query:
            if noun.lower() in list(sorted_idf_values[doc])[:3]:
                docs.append(doc)
            print(list(sorted_idf_values[doc])[:3])

                
    print(docs[:n])
    # print(sorted_idf_values['artificial_intelligence.txt']['artificial intelligence'])
    # print(raw_files['natural_language_processing.txt'].count("natural language processing"))
    return docs[:n]
  
                        

    return sorted(rank_core.items(), key=lambda item: item[1], reverse=True)[n]

def top_sentences(query, sentences, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    
    query = extract_pos(query)
    print(query)
    sent_res = []
    top_sent = {}
    for sent in sentences:
       
        if query['noun'][0].lower() in sentences[sent] and query['verb'][0].lower() in sentences[sent]:
            top_sent[sent] = sentences[sent]
            sent_res.append(sent)
            # print(sent)
            

        
    
    return sent_res[:n]


if __name__ == "__main__":
    main()
    

    






