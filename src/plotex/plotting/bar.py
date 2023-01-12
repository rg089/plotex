import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import random
import numpy as np
from plotex.utils.plotting import optimize_labels as optim_labels


def group_reduce(ax, df, group_col, value_col, reduce='mean', cmap=None, color=None, singlecolor=True, optimize_labels=True, **barkwargs):
    """
    create a bar chart with the x axis as the distinct values in a column, and the y axis as the reduced values in another column

    :param ax: the matplotlib axis
    :param df: dataframe containing information
    :param group_col: the column/list of columns to groupby
    :param value_col: the column whose value to reduce
    :param reduce: a string or function for the reduction method, defaults to 'mean'
    :param cmap: the colormap, defaults to None
    :param color: the color to use, defaults to None
    :param singlecolor: whether to use a singlecolor for all the bars, defaults to True
    :param optimize_labels: whether to optimize and reorder labels based on their length, defaults to True
    
    :return: the axis object
    """
    group_object = df.groupby(group_col)[value_col].aggregate(reduce)
    
    labels = group_object.index.tolist()
    avg_values = group_object.values

    if optimize_labels:  
        labels, avg_values = optim_labels(labels, avg_values)

    if color is None:
        if cmap is not None:
            if isinstance(cmap, str): cmap = sns.color_palette(cmap)
                
            if singlecolor: color = random.choice(cmap[:len(labels)])
            else: color = cmap[:len(labels)]

    if isinstance(color, str):
        color = [color for i in range(len(labels))] # matplotlib requires a list of colors in the new version

    if color is None:
        ax.bar(labels, avg_values, **barkwargs)
    else:
        ax.bar(labels, avg_values, color=color, **barkwargs)

    return ax


def stack_count(ax, df, basecol, stackcol, horizontal=True, cmap='pastel', color=None, **barkwargs):
    """
    create a stacked bar chart with basecol as the labels and stackcol as the column providing values

    :param ax: matplotlib axes object
    :param df: the dataframe
    :param basecol: the base column: y-axis in case of horizontal bar/ x-axis in case of vertical bar
    :param stackcol: the column with the value counts which stacks on itself
    :param horizontal: whether to create a horizontal bar chart, defaults to True
    :param cmap: the colormap to use, defaults to 'pastel'
    :param color: the color scheme to use, defaults to None
    
    :return ax: the axes object
    """
    labels = df[stackcol].unique()
    bases = df[basecol].unique()
    prev_counts = np.zeros(len(bases))

    if isinstance(cmap, str):
        color_map = sns.color_palette(cmap)
    else:
        color_map = cmap
        
    if color is None or isinstance(color, str): 
        colors = color_map[:len(labels)]
    
    for i, label in enumerate(labels):
        value_counts = df.loc[df[stackcol]==label, basecol].value_counts()
        values = np.array([value_counts[base] for base in bases])

        if horizontal: ax.barh(bases, values, left=prev_counts, color=[colors[i] for j in range(len(bases))], label=label, **barkwargs)
        else: ax.bar(bases, values, bottom=prev_counts, color=[colors[i] for j in range(len(bases))], label=label, **barkwargs)
        prev_counts += values
            
    ax.legend()
    return ax
