import nltk
import sys
import os
import string
import math
from copy import copy
import operator
from nouns import extract_nouns, extract_nouns_phrase
from nltk.corpus import stopwords

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


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
    file_idfs = compute_idfs(copy(file_words))
    new_ma_val = max(file_idfs.items(), key=operator.itemgetter(1))[0]

    # Prompt user for query
    query = input("Query: ")

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)
    
    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


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
            files[filename] = content

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


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    """
    Compute IDF (inverse document frequency) for each token in the given dictionary of tokenized documents.

    Args:
        documents (dict): A dictionary mapping a tokenization of words with their file name.

    Returns:
        A dictionary mapping each token to its IDF value.
    """
    num_docs = len(documents.values())  # number of documents in the corpus
    token_counts = {}  # keep track of how many documents each token appears in

    # iterate over each document's tokens
    for doc_name, tokens in documents.items():
        for token in set(tokens):
            token_counts[token] = token_counts.get(token, 0) + 1

    idf_values = {}  # dictionary to store the IDF values for each token
    
    # calculate IDF for each token
    for token, count in token_counts.items():
        idf_values[token] = math.log(num_docs / count) + 1

    

    return idf_values


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.      
    """
    
    
    files = copy(files)
    files_topic = {}
    for filename in files:
        files_topic[filename] = {}
        NOUNS = extract_nouns(' '.join(files[filename]))
        for word in files[filename]:
            if word in idfs and word in NOUNS :
                files_topic[filename][word] = idfs[word] * compute_tf(word, {filename: files[filename]})
        
        files_topic[filename] = dict(sorted(files_topic[filename].items(), key=lambda item: item[1], reverse=True))


    for name in files_topic:
        print(list(files_topic[name].items())[:4])

        pass
    NP_of_query = extract_nouns_phrase(query)
    print(NP_of_query)
    rank_core = {}
    for name in files_topic:
        rank_core[name] = 0
        for topic in list(files_topic[name].items())[:4]:
            for NP in NP_of_query:
                for N in NP.split(" "):
                    if topic[0] == N:
                        rank_core[name] +=  topic[1]
                        
    return sorted(rank_core.items(), key=lambda item: item[1], reverse=True)[n]

def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    raise NotImplementedError


if __name__ == "__main__":
    main()






