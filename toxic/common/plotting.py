"""
toxic.common.plotting

Functions for plotting.

Attributes
----------
plot_wordcloud_to_axis : function, plots a wordcloud to a passed axis
density_plot : function, ggplot-like interface for plotting densities segmented by a mask
"""

import seaborn as _seaborn
import wordcloud as _wordcloud
import matplotlib as _matplotlib

def plot_wordcloud_to_axis(cloud_string=None, title=None, ax=None, cloud_obj=_wordcloud.WordCloud(random_state=42)):
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
    fig = _matplotlib.pyplo.figure(1, figsize=(10,5))
    
    ax1 = _matplotlib.pyplo.subplot(121)
    barvals = data.groupby(color_mask).mean()[variable]
    _seaborn.barplot(x=barvals.index, y=barvals, ax=ax1)
    
    ax2 = _matplotlib.pyplot.subplot(122)
    _seaborn.kdeplot(data.loc[~color_mask, variable], shade=True, color="b", label='normal', ax=ax2)
    _seaborn.kdeplot(data.loc[color_mask, variable], shade=True, color="g", label='toxic', ax=ax2)
    return fig