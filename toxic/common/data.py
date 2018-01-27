"""
data
Functions for getting and preprocessing data.

Matthew Chatham
January 26
"""
import pandas as pd

def get_kaggle_data(file='train', verbose=False):
    """Gets the data from Google Cloud Storage"""
    if file not in ['train', 'test']: raise ValueError('file must be train|test')
    
    query = """
    #standardSQL
    SELECT * 
    FROM `mlmasters-191705.toxic_comments.{}`
    """.format(file)
    res = pd.read_gbq(
        query, project_id='mlmasters-191705', 
        dialect='standard', 
        verbose=verbose
    )
    
    return res