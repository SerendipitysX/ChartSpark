import numpy as np
from wordcloud import WordCloud
import matplotlib.pyplot as plt


class WordCloudGenerator:
    def __init__(self, font_path, background_color, colormap, prefer_horizontal, max_font_size, min_font_size, width, height, margin, d):
        self.font_path = font_path
        self.background_color = background_color
        self.colormap = colormap
        self.prefer_horizontal = prefer_horizontal
        self.max_font_size = max_font_size
        self.min_font_size = min_font_size
        self.width = width
        self.height = height
        self.margin = margin
        self.d = d
        print(d)
        
        self.sorted_values = sorted(d.values(), reverse=True) 
        self.sum_count = sum(d.values()) 
        self.light_list = np.linspace(5, 70, num=len(d)) 
    
    def get_rank(self, key): 
        value = self.d[key] 
        rank = self.sorted_values.index(value) 
        return rank 
    
    def color_func(self, word, font_size, position, orientation, random_state=None, **kwargs): 
        idx = self.get_rank(word) 
        hue = 11 
        lightness = self.light_list[idx] 
        return "hsl(%d, %d%%, %d%%)" % (hue, 0, lightness) 
    
    def generate_wordcloud(self):
        wc = WordCloud(font_path=self.font_path,  
                       background_color=self.background_color, colormap=self.colormap,  
                       prefer_horizontal=self.prefer_horizontal,  
                       max_font_size=self.max_font_size, min_font_size=self.min_font_size, 
                       width=self.width, height=self.height, 
                       margin=self.margin) 

        wc.generate_from_frequencies(self.d) 

        font_sizes = [word[1] for word in wc.layout_] 
        font_min, font_max = min(font_sizes), max(font_sizes) 

        wc.recolor(color_func=self.color_func) 
        fig = plt.figure() # create a new canvas with size 8x8 inches
        fig.add_subplot(1, 1, 1) # add a subplot to the canvas
        plt.margins(0,0) 
        plt.imshow(wc, interpolation='bilinear') 
        plt.axis('off') 
        plt.gca().set_title("")
        plt.savefig("frontend/src/assets/wordcloud/wc.png", bbox_inches = 'tight', pad_inches = 0) 
        print("-----------------------")
        return "frontend/src/assets/wordcloud/wc.png",
# d = {'Aghtrj': 20, 'Bsddfdh': 10, 'Cfergrr': 14, 'Jwet': 18}
# wordcloud_gen = WordCloudGenerator(font_path='C:/Users/user/A-project/speak/frontend/src/assets/fonts/TiltNeon-Regular.ttf',  
#                                    background_color='#F5F5F5', colormap="binary",  
#                                    prefer_horizontal=1, 
#                                    max_font_size=45, min_font_size=12, 
#                                    width=430, height=200, 
#                                    margin=100, d=d)
# wordcloud_gen.generate_wordcloud()
