import math

def compute_idf(doc_tokens):
    """
    Compute IDF (inverse document frequency) for each token in the given dictionary of tokenized documents.

    Args:
        doc_tokens (dict): A dictionary mapping a tokenization of words with their file name.

    Returns:
        A dictionary mapping each token to its IDF value.
    """
    print(len(doc_tokens.values()))
    num_docs = len(doc_tokens.values())  # number of documents in the corpus
    token_counts = {}  # keep track of how many documents each token appears in

    # iterate over each document's tokens
    for doc_name, tokens in doc_tokens.items():
        for token in set(tokens):
            token_counts[token] = token_counts.get(token, 0) + 1

    idf_values = {}  # dictionary to store the IDF values for each token

    # calculate IDF for each token
    for token, count in token_counts.items():
        idf_values[token] = math.log(num_docs / count)

    return idf_values

doc_tokens = {
    'document1': ['the', 'cat', 'sat', 'on', 'the', 'mat'],
    'document2': ['the', 'dog', 'chased', 'the', 'cat'],
    'document3': ['the', 'rat', 'ate', 'the', 'cheese'],
}
idf_values = compute_idf(doc_tokens)
print(idf_values)
