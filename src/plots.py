import sys

import numpy as np
import pandas as pd

from sklearn import manifold as skm

from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

import matplotlib.pyplot as plt
plt.ion()

def wordcloud_plot(text, filename=None, cloudargs={}):
    '''
    Displays and saves a wordcloud plot. 

    Parameters
    ----------
    text : str
        The text to be parsed in the wordcloud.
    filename : str
        If used, also saves a copy of the wordcloud to file as specified
        in the string.
    cloudargs : dict
        A list of keywords that can be passed to WordCloud if deviating from defaults.

    Returns
    -------
    fig : matplotlib figure
        A hook to the figure to make tweaks if wanted.
    '''
    default_kwargs = {
        'collocations':False, 
        'width':1000, 
        'height':700, 
        'background_color':'white', 
        'min_font_size':10
    }
    for key in default_kwargs.keys():
        if key not in cloudargs:
            cloudargs[key] = default_kwargs[key]

    wordcloud = WordCloud(**cloudargs).generate(text)

    fig, ax = plt.subplots(1,1, tight_layout=True)
    fig.set_size_inches(8,8)
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    fig.show()

    if filename is not None:
        fig.savefig(filename+'.jpg', dpi=300)

    return fig

def make_tSNE_projection_of_SVD(df, kwargs={}):
    '''
    Project SVD-transformed data onto two dimensions for visualisation.

    Parameters
    ----------
    df : Pandas DataFrame
        A dataframe with the reduced-dimensionality vector representation
        of tweets.
    kwargs : dict
        Optional keyword arguments which can be fed to sci-kit learn's TSNE
        model.

    Returns
    -------
    coords : Pandas DataFrame
        The x- and y-coordinates of each tweet in the projected 2d-space. 
    '''
    defaults = dict(
        init='random',
        random_state=0, 
        n_jobs=2, 
        perplexity=50, 
        n_iter=5000, 
        learning_rate=400)
    for key in defaults.keys():
        if key not in kwargs:
            kwargs[key] = defaults[key]

    tsne = skm.TSNE(n_components=2, **kwargs)
    tsneout = tsne.fit_transform(df)

    coords = pd.DataFrame(tsneout, columns=['tsne_x', 'tsne_y'], index=df.index)

    return coords

def plot_tsne_projection(df, label_str, plotly=False, kwargs={}):
    '''
    Function to visualise a tSNE projection in 2 dimensions.

    Parameters
    ----------
    df : Pandas DataFrame
        A dataframe that must contain columns `tsne_x` and `tsne_y` generated
        by `make_tSNE_projection_of_SVD()` as well as a column which can be used
        for labels.
    label_str : str
        The name of the column in `df` to be used as labels for colouring.
    plotly: bool
        If True, use plotly for the visualisation.
        If False, use matplotlib.
    '''

    if plotly: # Import and use plotly
        import plotly.express as px

        defaults = dict(
            width=800,
            height=800,
            #hover_name='screen_name',
            #hover_data=['hashtags'],
            color_discrete_sequence=px.colors.qualitative.Bold
        )
        for key in defaults.keys():
            if key not in kwargs:
                kwargs[key] = defaults[key]

        fig = px.scatter(df, 'tsne_x', 'tsne_y', color=label_str, **kwargs)

    else: # Use Matplotlib
        fig, ax = plt.subplots(1,1)
        ax.scatter(df['tsne_x'], df['tsne_y'], c=df[label_str].astype(int), cmap='tab20')
        fig.set_size_inches(10,10)
    
    return fig

def plot_H_index(df):
    '''

    Parameters
    ------

    Returns
    -------

    '''
    sns.set(font_scale=2)
    f = plt.figure(figsize=(20, 25))
    gs = f.add_gridspec(2, 1)
    ax = f.add_subplot(gs[0, 0])
    sns.distplot(df['h-index_like&retweets'], kde=False, rug=False)
    ax.set_xlabel('H-Index (like&retweets)', fontsize=50)
    ax.set_ylabel('N of users', fontsize=50)
    ax = f.add_subplot(gs[1, 0])
    sns.scatterplot(df['user_friends_n'],df['user_followers_n'],
                     size = df['h-index_like&retweets'],hue =df['h-index_like&retweets'],
                     alpha=0.4, sizes=(20, 200))
    ax.set_xlabel('Number of Friends', fontsize=50)
    ax.set_ylabel('Number of Followers', fontsize=50)
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_ylim(1, max(df['user_followers_n'])+1000000000)
    ax.set_xlim(0.5)