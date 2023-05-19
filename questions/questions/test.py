import gensim
from gensim import corpora

# Sample documents
documents = [
    "I like to play football",
    "Football is a popular sport",
    "I enjoy playing basketball",
    "Basketball is great",
    "I love watching tennis",
    "Tennis players are skilled"
]

# Preprocessing: tokenizing and creating a dictionary
tokenized_documents = [document.lower().split() for document in documents]
dictionary = corpora.Dictionary(tokenized_documents)

# Creating the document-term matrix
doc_term_matrix = [dictionary.doc2bow(doc) for doc in tokenized_documents]

# Training the LDA model
lda_model = gensim.models.LdaModel(
    doc_term_matrix,
    num_topics=2,  # Number of topics to extract
    id2word=dictionary,
    passes=10,  # Number of training passes
    random_state=42
)

# Print the topics and their top words
for topic in lda_model.print_topics():
    print(topic)

# Infer topics for new documents
new_documents = [
    "I enjoy playing football",
    "Tennis is a fun sport"
]
tokenized_new_docs = [doc.lower().split() for doc in new_documents]
new_doc_term_matrix = [dictionary.doc2bow(doc) for doc in tokenized_new_docs]
for doc, doc_topic in zip(new_documents, lda_model[new_doc_term_matrix]):
    print(f"Document: {doc}")
    print(f"Topics: {doc_topic}")
