import os
import functools


def copy_docstring(method, func=None):
    if func is None:
        return functools.partial(copy_docstring, method)

    func.__doc__ = method.__doc__
    return func


def save_file(content, fpath):
    """saves the supplied content in a text file

    Args:
        content (str): the content
        fpath (str): the file path to save at
    """
    base_folder = os.path.dirname(fpath)
    os.makedirs(base_folder, exist_ok=True)
    
    with open(fpath, "w") as f:
        f.write(content)


def check_if_exists(fpath):
    """checks if fpath exists

    Args:
        fpath (str): the file path to check
    :return bool: whether the path exists
    """
    return os.path.exists(fpath)


def combine_hash(fpath, hashed):
    """combines the file name with the hashcode and returns the absolute path

    Args:
        fpath: fpath
        hashed: ahash code

    Returns:
        the absolute combine path
    """
    assert fpath.endswith('.txt')
    
    stripped_path = fpath.rstrip('.txt')
    final_path = f"{stripped_path}_{hashed}.txt"
    final_path = os.path.abspath(final_path)
    
    return final_path


def find_value_from_keys(main_dict, keys):
    """traverses the specified key list, and if any key is found in the dictionary,
    returns the corresponding value, else None

    Args:
        main_dict: the dictionary to search in
        keys: the list of keys

    Returns:
        the value if found, else None
    """
    for key in keys:
        if key in main_dict:
            return main_dict[key]
        
    return None


def save(save_path, fig=None, plt=None, format='pdf'):
    """utility function to save the figure

    Args:
        save_path: the save path for the figure (including the
            extension)
        fig: the figure object, defaults to None
        plt: the plt object, defaults to None
        format: the format of the output plot, defaults to 'pdf'
    """
    assert fig is not None or plt is not None
    
    if fig is not None:
        fig.savefig(save_path, format=format)
    if plt is not None:
        plt.savefig(save_path, format=format)