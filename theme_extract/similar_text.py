import numpy as np
from gensim import corpora, models, similarities, downloader
from keybert import KeyBERT
import os
# from theme_wc import WordCloudGenerator


def load_embeddings(embeddings_file):
    # Detect the model format by its extension:
        emb_model = models.KeyedVectors.load_word2vec_format(embeddings_file, binary=True,                                                             unicode_errors='replace')
        key_list = emb_model.index_to_key  # list
        key_index_dict = emb_model.key_to_index  # dict
        embeddings = emb_model.vectors        # print(embeddings.shape)  #(199430, 300)
        return emb_model, embeddings, key_list, key_index_dict

def get_similar_words(theme, emb_model, embeddings, key_list, key_index_dict):
    word_dict = [(key, value) for key, value in key_index_dict.items() if key.startswith(theme)]    # print(word_dict)
    # [('covid-19_PROPN', 3894), ('covid-19_NOUN', 9583), ('covid-19_ADJ', 12940), ('covid-19_NUM', 16412)]    # get embedding of theme word
    emb1 = embeddings[word_dict[0][1]]    # compute the similarities
    similarities = emb_model.cosine_similarities(emb1, embeddings)
    sorted_similarities_index = np.argsort(similarities)[::-1]  # large->small
    # get the similar words
    similar_text = [key_list[idx].split('_')[0] for idx in sorted_similarities_index[1:10]]
    similar_text = list(dict.fromkeys(similar_text))  # remove duplicates    # 
    # print(similar_text)
    # compute the frequency of these words
    similar_text_dict = {}
    for text in similar_text:
        text_frequency = sum([emb_model.get_vecattr(key, "count") for key, value in key_index_dict.items() if key.startswith(text)])
        similar_text_dict[text] = text_frequency
    similar_text_dict = sorted(similar_text_dict.items(), key=lambda x: x[1], reverse=True)
    if len(similar_text_dict) >= 5:
        similar_text_dict = similar_text_dict[:4]
    similar_text_list = list(list(zip(*similar_text_dict))[0])
    return similar_text_list

def extract_kw_similar(title):
    kw_model = KeyBERT(model='all-mpnet-base-v2')
    # title = 'Number of police officers in crimeville'
    keywords = kw_model.extract_keywords(title,
                                        keyphrase_ngram_range=(1,1),
                                        stop_words='english',
                                        highlight=False,
                                        top_n=3)
    keywords_list = list(dict(keywords).keys())
    # print(keywords_list)

    # load model
    emb_model, embeddings, key_list, key_index_dict = load_embeddings('C:/Users/user/A-project/speak/theme_extract/model.bin')
    # find all words containing "xx"
    theme = keywords_list[0]
    theme_and_text = {}
    for theme in keywords_list:
        try:
            similar_text_list = get_similar_words(theme, emb_model, embeddings, key_list, key_index_dict)
            theme_and_text[theme] = similar_text_list
        except:
            pass
            # theme_and_text[theme] = []
    result_list = []
    for key, value in theme_and_text.items():
        result_list.append(key)
        result_list.extend(value)
    my_dict = {key: 20 - 1.5*i + 10*(i//5) for i,key in enumerate(result_list)}
    return my_dict

# title = "Date of cherry blossom in High Park"
# my_dict = extract_kw_similar(title)
# # print(my_dict)
# wordcloud_gen = WordCloudGenerator(font_path='C:/Users/user/A-project/speak/frontend/src/assets/fonts/TiltNeon-Regular.ttf',  
#                                     background_color='#F5F5F5', colormap="binary",  
#                                     prefer_horizontal=1, 
#                                     max_font_size=45, min_font_size=12, 
#                                     width=420, height=200, 
#                                     margin=50, d=my_dict)
# img_path2 = wordcloud_gen.generate_wordcloud()
