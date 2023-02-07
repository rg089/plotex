![logo](assets/plotex_lightmode.png#only-light)
![logo](assets/plotex_darkmode.png#only-dark)

## *Creating elegant, publication-ready plots made simple*
Plotex is a minimal wrapper over matplotlib (and to some extent, seaborn). It is primarily designed to ease plot generation for publications by taking care of the configuration (plot size, color schemes, font type/size/weight etc.) as well as enable rapid prototyping to reduce manual effort.

## Table Of Contents

The site is divided into the following sections:

1. [Snippets](frequent.md)
2. [API](api/index.md)
3. [Changelog](changelog.md)

[Snippets](frequent.md) contains examples and snippets that can be used frequently. [API](api/index.md) is the resting place for the documentation of individual classes and functions while [Changelog](changelog.md) is employed to track the added/removed functionalities in each version.

## Installation

Run the following command for installing:
```
pip install plotex
```

## Sample Usage

```
from plotex import plotex
plotex.init(colorblind=True)

subplots = (1,1)

figsize = plotex.skeleton(publisher='acl', fraction=0.5, subplots=subplots)

plotex.update_textsize(legend=3, xticks=-1, yticks=1) # Defines the font offset for each element (ex. font size of legend is increased by 3 points, size of xticks is decreased by 1pt etc.)

fig, axes = plt.subplots(nrows=subplots[0], ncols=subplots[1], figsize=figsize)

axes.plot([1,2,3], [1,2,3], label='$y=x$')
axes.plot([1,2,3], [1,4,9], label='$y=x^2$')

plotex.set_text(ax=axes, xlabel='Values of x', ylabel='Values of y')
plotex.save('sample.pdf', fig=fig)

```


## Acknowledgements

This project was mainly created for personal usage. I wanted a simple API where I could set a default theme once and use it repeatedly for multiple plots across various projects. I also required the ability to quickly change the font sizes/weights etc. without rewriting the same/similar lines of code over and over again. 

The references I used for writing this extremely simple and minimal library are:
* [Matplotlib](https://matplotlib.org/stable/tutorials/)
* [It's more fun to compute](https://jwalton.info/Embed-Publication-Matplotlib-Latex/)
* [Markov Wanderer](http://aeturrell.com/2018/01/31/publication-quality-plots-in-python/)
