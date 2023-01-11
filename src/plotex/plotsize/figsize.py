import matplotlib.pyplot as plt
import math
import difflib
from configuration import BackendConfiguration


class Sizing():
    
    def __init__(self, config=None, **config_kwargs):
        """
        initialize the sizing class

        :param config: the config file, defaults to None
        """
        self.config = config
        if self.config is None:
            self.config = BackendConfiguration(**config_kwargs)
            self.config.initialize()
        self.params = None
    
    
    def __save_params(self):
        """
        save a copy of the current rcParams
        """
        self.params = plt.rcParams.copy()
        
        
    def __load_params(self):
        """
        load the current saved copy of the rcParams
        """
        if self.params is not None:
            plt.rcParams.update(self.params)
    
    
    def __get_width_publisher(self, publisher):
        """
        get the width in pts given the name of the publisher

        :param publisher: the name of the publisher
        :return: the width in pts
        """
        if publisher == 'thesis':
            width = 426.79135
        elif publisher == 'acl':
            width = 455.244
        else:
            print(f'[INFO] Publisher "{publisher}" not found, setting to ACL format!')
            width = 455.244
            
        return width


    def adjust_font_size(self, subplots, fraction, **kwargs):
        """
        adjust the font_size based on the fraction and number of columns and \
        saves the adjusted params

        :param subplots: at uple of (nrow, ncols)
        :param fraction: fraction of the total width to use
        """
        _, num_cols = subplots
        
        font_params = ['font.size', 'axes.titlesize', 'legend.title_fontsize', 'xtick.labelsize', 'ytick.labelsize', 'axes.labelsize', 'legend.fontsize']
        for param in font_params:
            curr_value = float(plt.rcParams[param])
            plt.rcParams[param] = math.ceil(curr_value/num_cols*fraction)
        self.__save_params()
            

    def update_textsize(self, reinitialize=True, **kwargs):
        """
        This function changes the font size of various text elements in the plot such as xlabel, \
        ylabel, title, sticks, etc., by a specified offset. Uses deterministic and probabilistic \
        matching to determine and map the keyword argument to the required property
        
        :param reinitialize: initialize size params to those created by `get_size` after adjusting for\
            columns, fraction etc.
        :param kwargs: flexible keyword arguments specified by the user, where the name of \
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
        
        all_matches = list(font_params.keys()) + list(font_params.values()) # Search over both keys and values
        
        for key, value in kwargs.items():
            if key in special_params:
                font_param = special_params[key]
            else:
                font_param = difflib.get_close_matches(key, all_matches, n=1)
                if not font_param:
                    print(f"[INFO] No match found for argument: {key}!")
                    continue
                
                font_param = font_param[0]
                
            if font_param not in font_params:
                font_param = [k for k, v in font_params.items() if v == font_param][0]
            
            current_size = plt.rcParams[font_param]
            plt.rcParams[font_param] = current_size + value
    

    def convert_width_to_inches(self, width=None, publisher=None):
        """
        convert width from pts to inches

        :param width: the given width in pts, defaults to None
        :param publisher: the name of the publisher, defaults to None
        :return: the width in inches
        """
        width_pt = width or self.__get_width_publisher(publisher=publisher)
        fig_width_pt = width_pt 
        inches_per_pt = 1 / 72.27

        fig_width_in = fig_width_pt * inches_per_pt
        return fig_width_in
        
        
    def get_size(self, width=None, publisher=None, width_in_pts=True, reinitialize=True, fraction=1, 
                   subplots=(1, 1), **kwargs):
        """
        finds the ideal size of the plot and adjusts the text sizes according to the required dimensions

        :param width: the width, defaults to None
        :param publisher: the name of the publisher, defaults to None
        :param width_in_pts: whether the width is in points, defaults to True
        :param reinitialize: whether to reinitialize the config to itys defaults, defaults to True
        :param fraction: the fraction of the width supplied to use, defaults to 1
        :param subplots: (nrows, ncols), defaults to (1, 1)
        
        :return: figsize (width, height)
        """
        assert publisher is not None or width is not None, "Either set the width or the format."

        if reinitialize: self.config.initialize()

        golden_ratio = (5**.5 - 1) / 2
        
        if width_in_pts:
            fig_width_in = self.convert_width_to_inches(width=width, publisher=publisher)
            
        fig_width_in *= fraction
        fig_height_in = fig_width_in * golden_ratio * (subplots[0] / subplots[1])

        self.adjust_font_size(subplots=subplots, fraction=fraction, **kwargs)
        
        return (fig_width_in, fig_height_in)