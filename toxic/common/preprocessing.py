"""
toxic.common.preprocessing

Classes and functions for processing text data.

Attributes
----------
Stemmer : class, method `stem` can be used as an analyzer for a vectorizer
vectorize_text: function, takes a series of comments and transforms to a labeled dataframe
"""

import nltk as _nltk
import pandas as _pandas
import sklearn as _sklearn

class Stemmer():
    """
    Word stemmer to use in a CountVectorizer or TfidfVectorizer.
    """
    def __init__(self, stemming=None):
        """
        stemming : str, the type of stemming algorithm to use, one of snoball|lancaster|wordnet
        """
        
        self.stemming = stemming
        if stemming == 'snowball':
            self.stemmer = _nltk.stem.snowball.EnglishStemmer()
        elif stemming == 'lancaster':
            self.stemmer = _nltk.stem.lancaster.LancasterStemmer()
        elif stemming == 'wordnet':
            self.stemmer = _nltk.stem.wordnetWordNetLemmatizer()
        else:
            raise ValueError('Unrecognized stemmer')

    def stem(self, word=None):
        """stem an individual word string"""
        
        res = ''
        if self.stemming in ['snowball','lancaster']:
            res = self.stemmer.stem(word)
        elif self.stemming == 'wordnet':
            res = self.stemmer.lemmatize(word)
        return res

def vectorize_text(
    corpus=None, 
    output='sparse',
    vect='count',
    param_dict=dict(
        ngram_range=(1,1),
        stop_words='english',
        max_features=1000,
        binary=False
    )
):
    """
    Helper function to vectorize raw comments in introduction.ipynb.
    Fits and transforms either a CountVectorizer ('count') or
    TfidfVectorizer ('tfidf') to a corpus of comments and returns
    a DataFrame with appropriately-labeled axes.    
    """
    if not isinstance(corpus, _pandas.Series):
        raise ValueError('Enter a Pandas Series object for corpus')
    
    if vect == 'count':
        vectorizer = _sklearn.feature_extraction.text.CountVectorizer(**param_dict)
    elif vect == 'tfidf':
        vectorizer = _sklearn.feature_extraction.text.TfidfVectorizer(**param_dict)
    else:
        raise ValueError('Unrecognized vectorizer')
    
    # Fit-transform vectorizer and put into DataFrame
    print('Fitting data...')
    vectorizer.fit(corpus)
    
    print('Transforming data...')
    sparse = vectorizer.transform(corpus)
    if output.lower() == 'sparse':
        result = sparse
    elif output.lower() == 'array': 
        result = sparse.toarray()
    elif output.lower() == 'df':
        result = _pandas.DataFrame(
            sparse.toarray(), 
            columns=vectorizer.get_feature_names(), 
            index=corpus.index)

        # Sort DF columns
        print('Sorting df cols...')
        word_frequencies = result.sum(axis=0)
        keep_cols = sorted(
            vectorizer.vocabulary_.copy(), 
            key=lambda k: word_frequencies[k], 
            reverse=True)
        result = result[keep_cols]
    
    print('Done')
    return result