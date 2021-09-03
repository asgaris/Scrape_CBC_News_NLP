from CBC_Data_Preparationn import df 
from gensim.models import Word2Vec
from gensim.models import Phrases
from nltk.probability import FreqDist


class TextAnalysis:
    def __init__(self, n):
        #n number of most common words
        self.n = n
        # detect phrases longer than one word
        self.bigram_transformer = Phrases(df['clena_data'])
        self.train()
    
    # train model
    def train(self):
        self.model = Word2Vec(self.bigram_transformer[df['clena_data']], min_count=5, vector_size=200, epochs=100, workers=4)
        # summarize the model
        return f" Summarize Word2Vec model: \n {self.model}"
    
    # summarize vocabulary
    def Summarize_vocab(self):
        words = list(self.model.wv.index_to_key)
        return f" Words: \n {words}"
    
    #embedded vector for a specific token
    def Embedded_vector(self):
        return self.model.wv['vaccin']
    
    def Similar_words(self):
        most_similars_precalc = {k : self.model.wv.most_similar(k) for k in self.model.wv.index_to_key}
        return f" Most similar tokens: \n {most_similars_precalc}"
    
    def Freq_words(self):
        fdist = FreqDist(self.model.wv.index_to_key)
        print(fdist)
        return f" Frequency of words: \n {fdist.most_common(self.n)}"

# save model
#model.save('model.bin')
# load model
#new_model = Word2Vec.load('model.bin')

text_analysis = TextAnalysis(10)
print(text_analysis.train())
print(text_analysis.Freq_words())


        




