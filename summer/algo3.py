import numpy as np
import lda
import lda.datasets
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import PCA
from sklearn.lda import LDA



def do_lda(data,n) :
	np.random.seed(0)
	vectorizer = TfidfVectorizer(stop_words='english')
	X = vectorizer.fit_transform(data)
	print vectorizer.get_feature_names()