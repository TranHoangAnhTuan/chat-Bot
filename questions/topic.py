from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.decomposition import LatentDirichletAllocation as LDA
from nltk.corpus import stopwords
from numpy import int64, matrix
corpus = [
#  "Rafael Nadal Joins Roger Federer in Missing U.S. Open",
#           "Rafael Nadal Is Out of the Australian Open",
#           "Biden Announces Virus Measures",
#           "Biden's Virus Plans Meet Reality",
#           "Where Biden's Virus Plan Stands",
          "Johnathan is a field  computer science",
          "Artificial Intelligence will get your job",
          "An AI's intended utility function "
          ]


count_vect = CountVectorizer(stop_words=stopwords.words('english'), lowercase=True)
x_counts = count_vect.fit_transform(corpus)
x_counts.todense()

# matrix([[0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0],
#         [0, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0],
#         [1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
#         [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1],
#         [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1]], dtype=int64)

# print(count_vect.get_feature_names_out())
tfidf_transformer = TfidfTransformer()
x_tfidf = tfidf_transformer.fit_transform(x_counts)
# print(x_tfidf)
dimension = 3
lda = LDA(n_components = dimension)
lda_array = lda.fit_transform(x_tfidf)
# print(lda_array)
components = [lda.components_[i] for i in range(len(lda.components_))]
features = list(count_vect.get_feature_names_out())
important_words = [sorted(features, key = lambda x: components[j][features.index(x)], reverse = True)[:4] for j in range(len(components))]
print(important_words)