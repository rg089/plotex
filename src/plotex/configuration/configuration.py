import requests
import os
import matplotlib.pyplot as plt
import seaborn as sns
from plotex.utils.general import check_if_exists, save_file, combine_hash, find_value_from_keys
from plotex.utils.hashing import hash_url


class BackendConfiguration():
    
    CONFIG_FILE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config_files/config.txt")
    CONFIG_URL = "https://gist.githubusercontent.com/rg089/26d06984604c92cf452e77ee345434ea/raw/98730d2afa1be6381b4c9c0f6f18da440200fc9a/latex_plots.txt"
    
    
    def __init__(self, url=None, override=False, **kwargs):
        """
        initializing the configuration class
        
        :param url: the url of the config to create a new config, defaults to None
        :param override: if the config from the specified link already exists, whether to create it again
                         (used if in-place changes have been made to the url)
        :kwargs: other keyword arguments can include arguments for theme, style, palette etc.
        """
        if url is None:
            self.url = BackendConfiguration.CONFIG_URL
        self.override = override
        
        self.style = None
        self.palette = None
        self.__init_theme(**kwargs)


    def __fetch_content(self, url):
        """
        fetches the config params from the url if not locally present

        :raises Exception: if issue in fetching and decoding
        :return str: returns the content from the url
        """
        print(f"[INFO] Fetching configuration parameters from {url}!")
        try:
            r = requests.get(url)
            content = r.content.decode()
        except:
            raise Exception('An error occured while fetching and decoding the url content')
        
        return content


    def __generate_content_path(self):
        """
        creates the config by using a cached file, or fetching from the internet if cached file not present

        :return: the file path of the config file
        """
        url_hash = hash_url(self.url)
        fpath = combine_hash(BackendConfiguration.CONFIG_FILE_PATH, url_hash)
        
        exists = check_if_exists(fpath)
        if exists and not self.override: # If file exists and we don't need to override
            return fpath
        
        content = self.__fetch_content(url=self.url)
        save_file(content=content, fpath=fpath)
        
        return fpath
    
    
    def __init_theme(self, **kwargs):
        # Set style
        self.style = find_value_from_keys(kwargs, ['style', 'theme', 'background'])
        
        # Set palette
        self.palette = find_value_from_keys(kwargs, ['palette', 'cmap'])
        if self.palette is None: # If palette wasn't specified but colorblind argument is given
            use_colorblind = find_value_from_keys(kwargs, ['colorblind', 'colourblind', 'blind'])
            if use_colorblind:
                self.palette = 'colorblind'
                
    
    def reset(self):
        """
        reset the parameters to the original matplotlib ones
        """
        plt.rcdefaults()
        
        
    def initialize(self):
        """
        initializes the configuration file by setting the style from the config file
        """
                
        if self.style is not None:
            sns.set_style(self.style)
        
        # Nothe that the settings in the config file will override the conflicting ones in the specified seaborn style
        final_path = self.__generate_content_path()
        plt.style.use(final_path)
        
        if self.palette is not None:
            sns.set_palette(self.palette)