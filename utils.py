from __future__ import unicode_literals
from bs4 import BeautifulSoup
from bs4.element import Comment
import requests
from os import path
from persian_wordcloud.wordcloud import STOPWORDS, PersianWordCloud
import datetime
import numpy as np
from PIL import Image
from hazm import *
import re
import pickle

d = path.dirname(__file__)

def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

def text_from_html(soup):
    # soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)
    return u" ".join(t.strip() for t in visible_texts)

def get_article_body(body):
    soup = BeautifulSoup(body, 'html.parser')
    article_body = soup.find('div', {'class': 'article-content'})
    return article_body

def remove_emoji(data):
    if not data:
        return data
    try:
    # UCS-4
        patt = re.compile(u'([\U00002600-\U000027BF])|([\U0001f300-\U0001f64F])|([\U0001f680-\U0001f6FF])')
    except re.error:
    # UCS-2
        patt = re.compile(u'([\u2600-\u27BF])|([\uD83C][\uDF00-\uDFFF])|([\uD83D][\uDC00-\uDE4F])|([\uD83D][\uDE80-\uDEFF])')
    return patt.sub('', data)

def clean_text(text):
    text = re.sub("(@[A-Za-z0-9_]+)|(?:\@|https?\://)\S+", " ", text)
    text = re.sub("#", "", text)
    text = remove_emoji(text)
    return text

def generate_wordcloud(virgool_article, output_name=None):
    html = requests.get(virgool_article).text
    body = get_article_body(html)
    text = text_from_html(body)
    stopwords = set(STOPWORDS)

    sentences = sent_tokenize(text)
    normalizer = Normalizer()
    tagger = POSTagger(model=path.join(d, 'resources/postagger.model'))
    lemmatizer = Lemmatizer()

    all_words = []

    for sentence in sentences:
        clean_sentence = clean_text(text=sentence)
        text_normal = normalizer.normalize(clean_sentence)
        taged = tagger.tag(word_tokenize(text_normal))
        for item, key in taged:
            if key in ['Ne', 'N', 'AJ', 'AJe']:
                word = ''
                for w in item:
                    word += w
                all_words.append(lemmatizer.lemmatize(word, pos=key))

    all_words.reverse()
    text = ' '.join(all_words)
    virgool_mask = np.array(Image.open(path.join(d, "virgool.png")))

    wc = PersianWordCloud(font_path=path.join(d, "IRANSans.ttf"), mask=virgool_mask, max_words=100,
                background_color="white", width=600, height=600, prefer_horizontal=1, stopwords=stopwords)
    wc.generate(text)

    if output_name is None:
        output_name = "{}.png".format(list(body)[1].text)

    # store to file
    wc.to_file(path.join(d, output_name))

def get_last_article():
    html = requests.get('https://virgool.io/').text
    soup = BeautifulSoup(html, 'html.parser')
    last_article = soup.find('article', {'class': ['card', 'card-post']})
    last_article_div = last_article.find('div', {'class': ['post-content']})
    last_article_a = last_article_div.find('a', {})
    last_article_h2 = last_article_a.find('h2', {'class': ['post--title']})
    # print(last_article_h2.text)
    return (last_article_a['href'], last_article_h2.text)

def persist(file_path, var):
    f = open(file_path, 'wb')
    pickle.dump(var, f)
    f.close()

def get_vars(file_path):
    f = open(file_path, 'rb')
    obj = pickle.load(f)
    f.close()
    return obj
