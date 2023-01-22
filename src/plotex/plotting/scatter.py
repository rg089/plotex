import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns


def marker(ax, df, x, y, marker_col, cmap=None, singlecolor=False, 
             markerscale=1., markersize=10, **scatterkwargs):
    """
    create a scatterplot with distinct markers (with labels) \
    based on the specified column in the dataframe

    :param ax: matplotlib axis object
    :param df: the dataframe with the data 
    :param x: the column to use for x-axis of the plot 
    :param y: the column to use for y-axis of the plot
    :param marker_col: the column for marker_types 
    :param cmap: the colormap to use, defaults to None
    :param singlecolor: whether to use a single color, defaults to False
    :param markerscale: the scale of the markers (relative to the default \
                        font size), defaults to 1.
    :param markersize: the size of the markers, defaults to 10
    :param scatterkwargs: keyword arguments to pass into the scatter function
    
    :return ax: the axis object
    """
    markers = ['*', 'o', 'X', "^", 'D', 'P', 'H', 's', "v", "d", "h"]
    
    if cmap is None: cmap = 'pastel'
    colors = sns.color_palette(cmap)
    if singlecolor:
        colors = [colors[0] for i in range(len(colors))]
        
    unique_marker_values = df[marker_col].unique()
    
    # Looping to add the label for each marker (legend)
    for i, marker_val in enumerate(unique_marker_values):
        mask = df[marker_col].values == marker_val
        x, y = df[x][mask], df[y][mask]
        ax.scatter(x=x, y=y, s=markersize, label=marker_val, marker=markers[i], 
                   color=colors[i], **scatterkwargs)
    
    ax.legend(markerscale=markerscale);
    
    return ax

# Defining the function `embeddings` to be same as the `marker` function
embeddings = marker

# TODO: Add support for separate marker_col and color_col in `marker` (or create a new function)
# Can use this link for ref: https://stackoverflow.com/questions/47832237/legend-for-colour-and-for-marker