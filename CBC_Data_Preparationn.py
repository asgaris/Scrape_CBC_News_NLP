import pandas as pd
import os
import nltk
nltk.download("stopwords")
nltk.download('wordnet')
nltk.download('punkt')
from nltk.tokenize import word_tokenize
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
import string
from nltk.corpus import stopwords
from gensim.models.phrases import ENGLISH_CONNECTOR_WORDS

class CBCDataPreparation:
    def __init__(self, path):
        self.folderpath = path
        self.data_loader()
        self.token_text()
        self.lemmatize_text()
        self.stemming_text()
        self.cleaning()
        self.csv_file()

    def data_loader(self):
        data_path = os.path.join(self.folderpath, 'CBC.csv')
        data = pd.read_csv(data_path)
        self.data = data.dropna().reset_index()

    #Tokenization 
    def token_text(self):
        self.data['token'] = self.data['Headline'].apply(word_tokenize)

    def lemmatize_text(self):
        def lemmatize(text):
            lemmatizer = WordNetLemmatizer()
            return [lemmatizer.lemmatize(w) for w in text]
        self.data['lemmatize'] = self.data['token'].apply(lemmatize)

    def stemming_text(self):
        def stemming(text):
            stemming = PorterStemmer()
            return [stemming.stem(w) for w in text]
        self.data['stemming'] = self.data['lemmatize'].apply(stemming)

    def cleaning(self):
        #Converting all Characters to Lowercase
        self.data['lower'] = self.data['stemming'].apply(lambda x: [word.lower() for word in x])
        #Removing Punctuations
        punc = string.punctuation
        self.data['no_punc'] = self.data['lower'].apply(lambda x: [word for word in x if word not in punc])
        #Removing Stopwords
        stop_words = set(stopwords.words('english'))
        self.data['stopwords_removed'] = self.data['no_punc'].apply(lambda x: [word for word in x if word not in stop_words])
        #use regex to remove E-mails, URLs, punctuations, new line characters, single characters, digits
        self.data['clena_data'] = self.data['stopwords_removed'].replace(r'(?i)\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b', '', regex=True)

    def csv_file(self):
        dataframe = self.data[['clena_data']]
        dataframe.to_csv('CBC_scrape_clean.csv')
        return dataframe

CBC = CBCDataPreparation('C:/Users/AsgariSa/CBC')
df = CBC.csv_file()
