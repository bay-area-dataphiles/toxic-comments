"""
data
Functions for getting and preprocessing data.

Matthew Chatham
January 26
"""
import pandas as _pandas

def get_kaggle_data(file='train', verbose=False):
    """
    Get Kaggle data.
    
    Parameters
    ----------
    file : str, 'train|test' to get the corresponding data (default 'train')
    verbose : bool, True to see progress messages from BigQuery (default False)
    
    Returns
    ----------
    res : a pandas dataframe holding the train/test data
    """
    if file not in ['train', 'test']: raise ValueError('file must be train|test')
    
    try:
        res = _pandas.read_csv('{}.csv'.format(file), encoding='utf-8', index_col='id')
    except:
        query = """
        #standardSQL
        SELECT *
        FROM `mlmasters-191705.toxic_comments.{}`
        """.format(file)
        res = _pandas.read_gbq(
            query, project_id='mlmasters-191705',
            dialect='standard',
            verbose=verbose
        ).set_index('id')
        res.to_csv('{}.csv', encoding='utf-8', index=True)
    
    return res
