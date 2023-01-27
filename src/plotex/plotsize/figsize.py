import matplotlib.pyplot as plt
import math
import difflib, os
import json
import requests

from plotex.configuration import BackendConfiguration
from plotex.utils.general import save_file

class Sizing():
    
    CONFIG_URL = 'https://gist.githubusercontent.com/rg089/92540eef5ee88de5d2770a453c85c489/raw/b127ba7b0e7eff3c5eddf1202f01595e5c60c949/size_config.json'
    CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config_files/size_config.json")
    
    
    def __init__(self, config=None, **config_kwargs):
        """initialize the sizing class

        Args:
            config: the config file, defaults to None
        """
        self.config = config
        if self.config is None:
            self.config = BackendConfiguration(**config_kwargs)
            self.config.initialize()
        self.params = None
        self.size_config = self.__load_config()
        
        
    def __load_config(self):
        if os.path.exists(Sizing.CONFIG_PATH):
            with open(Sizing.CONFIG_PATH, 'r') as f:
                config = json.load(f)
        else:
            r = requests.get(Sizing.CONFIG_URL)
            config = r.json()
            save_file(content=config, fpath=Sizing.CONFIG_PATH)
            
        return config
            
            
    def __save_params(self):
        """save a copy of the current rcParams"""
        self.params = plt.rcParams.copy()
        
        
    def __load_params(self):
        """load the current saved copy of the rcParams"""
        if self.params is not None:
            plt.rcParams.update(self.params)
    
    
    def __get_width_publisher(self, publisher, width=None):
        """get the width in pts given the name of the publisher

        Args:
            publisher (str): the name of the publisher
            width (float): if width is specified, then it is cached

        Returns:
            float: the width in pts
        """
        publisher = publisher.lower()
        
        if width is not None:
            self.__cache_width(publisher, width)
            return width
        
        width = self.__read_width(publisher)
            
        return width
    
    
    def __read_width(self, publisher:str):
        """
        reads the width from the config file for the supplied publisher. \
        If not found, then use the ACL format width

        Args:
            publisher (str): the publisher name

        Returns:
            float: the width in pts
        """
        if publisher in self.size_config['width']:
            width = self.size_config['width'][publisher]
        else:
            print(f'[INFO] Publisher "{publisher}" not found, setting to ACL format!')
            print('To save this publisher, give the values for both publisher and width')
            width = 455.244
            
        return width
    
    
    def __cache_width(self, publisher:str, width:float):
        """
        caches the `publisher:width` mapping 

        Args:
            publisher (str): the publisher
            width (float): the width in pts
        """
        print(f'[INFO] Caching {publisher}:{width} mapping!')
        self.size_config['width'][publisher] = width
        save_file(self.size_config, Sizing.CONFIG_PATH)


    def adjust_font_size(self, subplots, fraction, **kwargs):
        """adjust the font_size based on the fraction and number of columns and
        saves the adjusted params

        Args:
            subplots: at uple of (nrow, ncols)
            fraction: fraction of the total width to use
        """
        _, num_cols = subplots
        
        font_params = ['font.size', 'axes.titlesize', 'legend.title_fontsize', 'xtick.labelsize', 'ytick.labelsize', 'axes.labelsize', 'legend.fontsize']
        for param in font_params:
            curr_value = float(plt.rcParams[param])
            plt.rcParams[param] = math.ceil(curr_value/num_cols*fraction)
        self.__save_params()
        
        
    def __find_matching_param(self, key, main_params, special_params={}):
        """find the matching paramater to the key in the matplotlib.rcParams file specified by
        the main_params and special_params

        Args:
            key: the key with which we search
            main_params: the main dictionary, with keys as rcParams keys
                and values as their shortened versions
            special_params: direct mapping to handle exceptions where
                probabilstic matching might fail, defaults to {}

        Returns:
            the found parameter, or None if not found
        """
        all_matches = list(main_params.keys()) + list(main_params.values()) # Search over both keys and values
        
        if key in special_params:
            parameter = special_params[key]
        else:
            parameter = difflib.get_close_matches(key, all_matches, n=1)
            
            if not parameter:
                print(f"[INFO] No match found for argument: {key}!")
                return None
            
            parameter = parameter[0]
            
            if parameter not in main_params:
                parameter = [k for k, v in main_params.items() if v == parameter][0]
            
        return parameter
        

    def update_textsize(self, reinitialize=True, **kwargs):
        """This function changes the font size of various text elements in the plot such as xlabel,
        ylabel, title, sticks, etc., by a specified offset. Uses deterministic and probabilistic
        matching to determine and map the keyword argument to the required property

        Args:
            reinitialize: initialize size params to those created by
                `get_size` after adjusting for columns, fraction etc.
            **kwargs: flexible keyword arguments specified by the user,
                where the name of
        the argument is the key and the offset is the value.
        """
        if reinitialize:
            self.__load_params()
        
        font_params = {'font.size': 'fontsize',
                    'axes.titlesize': 'title',
                    'legend.title_fontsize': 'legendtitle',
                    'xtick.labelsize': 'xticks',
                    'ytick.labelsize': 'yticks',
                    'axes.labelsize': 'labels',
                    'legend.fontsize': 'legend'}
        
        special_params = {'xlabel': 'axes.labelsize', 'ylabel': 'axes.labelsize', 
                          'title': 'axes.titlesize', 'legend': 'legend.fontsize'}
        
        for key, value in kwargs.items():
            font_param = self.__find_matching_param(key=key, main_params=font_params, 
                                                    special_params=special_params)
            if font_param is None: continue
            current_size = plt.rcParams[font_param]
            plt.rcParams[font_param] = current_size + value
            
            
    def update_textweight(self, reinitialize=False, **kwargs):
        """This function changes the font weight of various text elements in the plot such as xlabel,
        ylabel, title. The values are 'light', 'normal', 'bold'.
        Uses deterministic and probabilistic matching to determine and map the keyword
        argument to the required property

        Args:
            reinitialize: initialize size params to those created by
                `get_size` after adjusting for columns, fraction etc.
            **kwargs: flexible keyword arguments specified by the user,
                where the name of
        the argument is the key and the weight is the value.
        """
        if reinitialize:
            self.__load_params()
        
        font_params = {
                    'axes.titleweight': 'title',
                    'axes.labelweight': 'label'}
        
        special_params = {'xlabel': 'axes.labelweight', 'ylabel': 'axes.labelweight', 
                          'title': 'axes.titlweight'}
        
        for key, value in kwargs.items():
            font_param = self.__find_matching_param(key, main_params=font_params, 
                                                    special_params=special_params)
            if font_param is None: continue            
            plt.rcParams[font_param] = value
    

    def remove_ticks(self, xtick=True, ytick=True):
        """remove the tick marks

        Args:
            xtick: remove ticks on x-axis, defaults to True
            ytick: remove ticks on y-axis, defaults to True
        """
        if xtick:
            plt.rcParams['xtick.major.size'] = 0
        if ytick:
            plt.rcParams['ytick.major.size'] = 0
            
            
    def set_lim(self, ax, xlims=(None, None), ylims=(None, None)):
        """set the starting and ending points of the x and y axes

        Args:
            ax: the matplotlib axis object
            xlims: tuple containing the (min, max) values of the x
                axis, defaults to (None, None)
            ylims: tuple containing the (min, max) values of the y
                axis, defaults to (None, None)
        """
        if xlims[0] is not None and xlims[1] is not None:
            ax.set_xlim(xlims[0], xlims[1])
        if ylims[0] is not None and ylims[1] is not None:
            ax.set_ylim(ylims[0], ylims[1])

        
    def convert_width_to_inches(self, width=None, publisher=None):
        """convert width from pts to inches

        Args:
            width: the given width in pts, defaults to None
            publisher: the name of the publisher, defaults to None

        Returns:
            the width in inches
        """
        if publisher is not None:
            width_pt = self.__get_width_publisher(publisher=publisher, width=width)
        else:
            width_pt = width 
        fig_width_pt = width_pt 
        inches_per_pt = 1 / 72.27

        fig_width_in = fig_width_pt * inches_per_pt
        return fig_width_in
        
        
    def get_size(self, width=None, publisher=None, width_in_pts=True, reinitialize=True, fraction=1, 
                   subplots=(1, 1), **kwargs):
        """finds the ideal size of the plot and adjusts the text sizes according to the required dimensions
            if both publisher and width are specified, then the publisher:width is cached
            
        Args:
            width: the width, defaults to None
            publisher: the name of the publisher, defaults to None
            width_in_pts: whether the width is in points, defaults to
                True
            reinitialize: whether to reinitialize the config to itys
                defaults, defaults to True
            fraction: the fraction of the width supplied to use,
                defaults to 1
            subplots: (nrows, ncols), defaults to (1, 1)

        Returns:
            figsize (width, height)
        """
        assert publisher is not None or width is not None, "Either set the width or the format."

        if reinitialize: self.config.initialize()

        golden_ratio = (5**.5 - 1) / 2
        
        if width_in_pts:
            fig_width_in = self.convert_width_to_inches(width=width, publisher=publisher)
        else:
            fig_width_in = width
            
        fig_width_in *= fraction
        fig_height_in = fig_width_in * golden_ratio * (subplots[0] / subplots[1])

        self.adjust_font_size(subplots=subplots, fraction=fraction, **kwargs)
        
        return (fig_width_in, fig_height_in)