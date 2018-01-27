import wordcloud
import matplotlib.pyplot as plt
import seaborn
from google.cloud import storage
from io import StringIO
import pandas
import numpy
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

from sklearn.base import BaseEstimator, TransformerMixin

from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem.snowball import EnglishStemmer
from nltk.stem.lancaster import LancasterStemmer

import scipy

from collections import OrderedDict

class _Stemmer():
            
            def __init__(self, stemming=None):
                
                self.stemming = stemming
                
                if stemming == 'snowball':
                    self.stemmer = EnglishStemmer()
                elif stemming == 'lancaster':
                    self.stemmer = LancasterStemmer()
                elif stemming == 'wordnet':
                    self.stemmer = WordNetLemmatizer()
                else:
                    raise ValueError('Unrecognized stemmer')
            
            def stem(self, word=None):
                res = ''
                if self.stemming in ['snowball','lancaster']:
                    res = self.stemmer.stem(word)
                elif self.stemming == 'wordnet':
                    res = self.stemmer.lemmatize(word)
                return res
            
class LogisticRegression_mod(LogisticRegression):
    def __init__(self):
        return None
    
    def fit(self, x=None, y=None):
        return LogisticRegression.fit(x['matrix_res'])

class Stemmer(BaseEstimator, TransformerMixin):
    """
    Takes a term-document matrix, stems each word,
    and adds the term vectors with the same stem.
    Returns the modified vocabulary and t-d  matrix.
    """
    def __init__(self, stemming=None):
        self.stemming = stemming
        return None
    
    def fit(self, x=None, y=None, td_matrix=None, vocab=None):
        return self
    
    def transform(self, **kwargs):
        """
        Stemmer should be [snowball|lancaster|wordnet],
        see http://www.nltk.org/api/nltk.stem.html#module-nltk.stem
        for more information.
        
        pseudo-code:
        start a dict of indices to combine and the associated stem
        start a new vocabulary of stems
        start the vocab index at 0
        for each word in the vocabulary:
            stem the word
            add/append the stem's index to the result indices dict, with stem as key
            if stem not in vocab results: add at vocab index, increment vocab_index
        create a result matrix with dim(axis1) = len(vocab result dict)
        for each stem in the indices dict:
            compute np.sum(x, axis=1) where x is the columns of td_matrix at the indices in the item
            set the column of the result matrix per the result vocab dict
        """
        #print(stemming)
        print('Creating variables...')
        combine_idx = dict()
        vocab_res = OrderedDict()
        vocab_idx = 0
        stemmer = _Stemmer(stemming=self.stemming)
        
        print('Stemming vocabulary...')
        for oldword in kwargs['vocab']:
            stem = stemmer.stem(word=oldword)
            if stem in combine_idx:
                combine_idx[stem].append(kwargs['vocab'][oldword])
            else:
                combine_idx[stem] = [kwargs['vocab'][oldword]]
            
            if stem not in vocab_res:
                vocab_res[stem] = vocab_idx
                vocab_idx += 1
#                 print(vocab_res)
        
        print('Combining stem facet vectors...')
        matrix_res = scipy.sparse.csr_matrix((kwargs['td_matrix'].shape[0], 0))
        print('shape of empty matrix res:', matrix_res.shape)
        
        print('Summing across stem facets...')
#         print('matrix res', matrix_res)
        for stem in vocab_res:
            old_vectors = kwargs['td_matrix'][:, combine_idx[stem]]
#             print('old vectors shape', old_vectors.shape)
            new_vector = old_vectors.sum(axis=1)
#             print('new vector', new_vector.shape)
#             print('stem_vector:', stem_vector.sum())
#             print(matrix_res)
            matrix_res = scipy.sparse.hstack([matrix_res, new_vector], format='csr')
        
        print('result stack shape:', matrix_res.shape)
        
        print('Sorting result matrix...')
        stem_sums = matrix_res.sum(axis=0)
#         print('stem sums:', stem_sums)

        sorted_idx = numpy.asarray(numpy.argsort(stem_sums, )).flatten(order='F')[::-1]
        #
        print('sorted index shape:', sorted_idx.shape)
        print('sorted index:', sorted_idx)
        matrix_res = matrix_res[:, sorted_idx]
        
        print('Sorting vocabulary')
        #import pdb; pdb.set_trace()
        vocab_res = numpy.array([item[0] for item in vocab_res.items()])[sorted_idx]
        #def dict_to_list(dict=None):
         #   {stem: vocab_res.index(stem) for stem in vocab_res}
        #vocab_res = dict_to_list(vocab_res)
            
        return {'vocab_res': vocab_res, 'matrix_res': matrix_res}

def gcs_to_df(project='mlmasters', bucket='toxic-comments', blob='sample_submission.csv'):
    """
    Gets data from Google Cloud Storage.
    """
    client = storage.Client(project=project)
    bucket = client.get_bucket(bucket)
    s = bucket.get_blob(blob).download_as_string()
    f = StringIO(s.decode())
    df = pandas.read_csv(f)
    return df

def plot_wordcloud_to_axis(cloud_string=None, title=None, ax=None, cloud_obj=wordcloud.WordCloud(random_state=42)):
    """
    Plots a wordcloud to the passed axis using the passed string.
    """
    if cloud_string:
        cloud = cloud_obj.generate(cloud_string)
        ax.imshow(cloud)
        if title:
            ax.set_title(title)
        ax.axis("off")
        return ax

def density_plot(data=None, variable=None, color_mask=None):
    """
    somewhat ggplot-like simple plotting 
    interface for densities segmented by a mask
    """
    fig = plt.figure(1, figsize=(10,5))
    
    ax1 = plt.subplot(121)
    barvals = data.groupby(color_mask).mean()[variable]
    seaborn.barplot(x=barvals.index, y=barvals, ax=ax1)
    
    ax2 = plt.subplot(122)
    seaborn.kdeplot(data.loc[~color_mask, variable], shade=True, color="b", label='normal', ax=ax2)
    seaborn.kdeplot(data.loc[color_mask, variable], shade=True, color="g", label='toxic', ax=ax2)
    return fig

default_params = dict(
    ngram_range=(1,1),
    stop_words='english',
    max_features=1000,
    binary=False
)

def vectorize_text(
    corpus=None, 
    output='sparse',
    vect='count',
    param_dict=default_params
):
    """
    Helper function to vectorize raw comments.
    Fits and transforms either a CountVectorizer ('count') or
    TfidfVectorizer ('tfidf') to a corpus of comments and returns
    a DataFrame with appropriately-labeled axes.    
    """
    if not isinstance(corpus, pandas.Series):
        raise ValueError('Enter a Pandas Series object for corpus')
    
    if vect == 'count':
        vectorizer = CountVectorizer(**param_dict)
    elif vect == 'tfidf':
        vectorizer = TfidfVectorizer(**param_dict)
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
        result = pandas.DataFrame(
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