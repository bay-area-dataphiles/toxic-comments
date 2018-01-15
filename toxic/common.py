import wordcloud
import matplotlib.pyplot
import seaborn
from google.cloud import storage
from io import StringIO
import pandas
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

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
    fig = pyplot.figure(1, figsize=(10,5))
    
    ax1 = pyplot.subplot(121)
    barvals = data.groupby(color_mask).mean()[variable]
    seaborn.barplot(x=barvals.index, y=barvals, ax=ax1)
    
    ax2 = pyplot.subplot(122)
    seaborn.kdeplot(train.loc[~color_mask, variable], shade=True, color="b", label='normal', ax=ax2)
    seaborn.kdeplot(train.loc[color_mask, variable], shade=True, color="g", label='toxic', ax=ax2)
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