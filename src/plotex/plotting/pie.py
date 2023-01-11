import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
from plotex.utils import set_text


def column_frequency(ax, df, column, cmap=None, percent=True, **piekwargs):
    """
    create a pie chart based on the frequency of values in a particular column

    :param ax: matplotlib axis object
    :param df: the dataframe with the data 
    :param column: the column to calculate frequencies over 
    :param cmap: the colormap to use, defaults to None
    :param percent: whether to display percentages, defaults to True
    :param piekwargs: keyword arguments to pass into the pie function
    
    :return ax: the axis object
    """
    value_counts = df[column].value_counts()
    
    labels = value_counts.index    
    data = value_counts.values
    
    if percent:
        data = data/data.sum()*100

    colors = None
    if cmap is not None:
        if isinstance(cmap, str): cmap = sns.color_palette(cmap)
        colors = cmap[:len(data)]
    
    autopct = '%.0f'
    if percent: autopct='%.0f%%'
    
    ax.pie(data, labels = labels, colors=colors, autopct=autopct, **piekwargs)
    
    return ax