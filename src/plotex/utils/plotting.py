import matplotlib.pyplot as plt
import matplotlib


def optimize_labels(labels, values):
    """optimizes the bar chart labels by interweaving the labels based on their length to minimize overlap

    Args:
        labels: the original labels
        values: the original values

    Returns:
        optimized labels, values
    """
    mapper = {l:v for l,v in zip(labels, values)}
    sorted_labels = sorted(labels, key=len)

    n = len(labels)
    start, end = 0, n-1

    final_labels = []

    while end >= start:
        if end == start:
            final_labels.append(sorted_labels[start])
        else:
            final_labels.append(sorted_labels[start])
            final_labels.append(sorted_labels[end])
        start += 1
        end -= 1

    final_values = [mapper[label] for label in final_labels]
    return final_labels, final_values


def set_text(plt:plt=None, ax:matplotlib.axes.Axes=None, xlabel=None, ylabel=None, title=None, xticklocs=None, xticklabels=None,
               xtickrot=None, yticklocs=None, yticklabels=None, ytickrot=None):
    """set xlabel/ylabel/xticks/yticks/title (including rotation of ticks)

    Args:
        plt: the matplotlib pyplot object
        ax: axis on which to label
        xlabel: the xlabel string, defaults to None
        ylabel: the ylabel string, defaults to None
        title: the title string, defaults to None
        xticklocs: the location of xticks, defaults to None
        xticklabels: the labels of xticks, defaults to None
        xtickrot: the rotation angle in degrees of xtick labels,
            defaults to None
        yticklocs: the location of yticks, defaults to None
        yticklabels: the labels of yticks, defaults to None
        ytickrot: the rotation angle in degrees of ytick labels,
            defaults to None
    """
    
    assert plt is not None or ax is not None
    
    if xlabel is not None:
        if ax is not None: ax.set_xlabel(xlabel)
        elif plt is not None: plt.xlabel(xlabel)
        
    if ylabel is not None:
        if ax is not None: ax.set_ylabel(ylabel)
        elif plt is not None: plt.ylabel(ylabel)
        
    if title is not None:
        if ax is not None: ax.set_title(title)
        elif plt is not None: plt.title(title)
        
    if xtickrot is not None:
        if ax is not None: ax.tick_params(axis='x', rotation=xtickrot)
        elif plt is not None: plt.xticks(rotation=xtickrot)
        
    assert xticklabels is None or (xticklabels is not None and xticklocs is not None)
    if xticklocs is not None:
        if ax is not None: ax.set_xticks(xticklocs, labels=xticklabels)
        elif plt is not None: plt.xticks(ticks=xticklocs, labels=xticklabels)
        
    if ytickrot is not None:
        if ax is not None: ax.tick_params(axis='y', rotation=ytickrot)
        elif plt is not None: plt.yticks(rotation=ytickrot)
        
    assert yticklabels is None or (yticklabels is not None and yticklocs is not None)
    if yticklocs is not None:
        if ax is not None: ax.set_yticks(yticklocs, labels=yticklabels)
        elif plt is not None: plt.yticks(ticks=yticklocs, labels=yticklabels)
        
        
def custom_legend(ax, text, xy=(0.5, 0.5), box=True, box_bgcolor=(1.0, 1, 1, 1),
                  box_edgecolor=(0.0, 0.0, 0.0, 0.1)):
    """create a custom legend/text (without color strip)

    Args:
        ax: mpl axes object
        text: the text to add (str or list); if list added with `\n`
        xy: the (x,y) offset fraction, relative to the BOTTOM-LEFT
            point, defaults to (0.5, 0.5)
        box: whether to add a bounding box, defaults to True
        box_bgcolor: the background color of the box, defaults to (1.0,
            1, 1, 1)
        box_edgecolor: the edge color of the box, defaults to (0.0, 0.0,
            0.0, 0.1)

    Returns:
        `ax`, the axis object
    """
    
    if isinstance(text, list):
        text = '\n'.join(text)
    
    assert isinstance(text, str)
    
    if box:
        ax.annotate(text,
                xy=xy, xycoords='axes fraction',
                textcoords='offset points',
                bbox=dict(boxstyle="round", fc=box_bgcolor,
                          ec=box_edgecolor))
    else:
        ax.annotate(text,
                xy=xy, xycoords='axes fraction',
                textcoords='offset points')
    
    return ax
    
    
custom_text = custom_legend
    