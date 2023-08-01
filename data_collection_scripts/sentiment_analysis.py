# packages imported
import pandas as pd
import nltk
import string
import re
from nltk.corpus import stopwords
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer
from nltk.corpus import words

# variable set up 
stopWords = set(stopwords.words('english'))
sia = SentimentIntensityAnalyzer()
ps = PorterStemmer()
lemmatizer = WordNetLemmatizer()
wordList = words.words()

dataFileName = 'gdpr_sentiment_analysis.csv'
columnName = 'title_not_bot'
resultFileName = 'non_gdpr_sentiment_analysis.csv'

# Read the original data file
data_df = pd.read_csv(dataFileName)
items = data_df[columnName]
negative = []
neutral = []
positive = []
compound = []
preprocess = []

# preprocess the original data
count = 0
for item in items:
    if type(item) is str:
        #remove @mentions hyper link
        item = re.sub(r'@[A-Za-z0-9]+', '', item)
        item = re.sub(r'https?:\/\/\S+', '', item) 
        # Tokenize the string
        tokens = nltk.word_tokenize(item,language='english')
        # Lower all strings
        lower = [token.lower() for token in tokens]
        # Remove punctuation
        punctuation = [''.join(char for char in item
                        if char not in string.punctuation)
                for item in lower]
        # Remove stopwords
        stop_words = []
        for word in punctuation:
            if word not in stopWords:
                stop_words.append(word)
        # lemmatization
        lemma_words = []
        for word in stop_words:
            lemma_words.append(lemmatizer.lemmatize(word))
        # Remove empty string in the punctuation removal list
        updatedList = list(filter(None, lemma_words))
        # Get rid of the meaningless word by len
        updateTokens = []
        for word in updatedList:
            if len(word) < 20 and word.encode().isalpha():
                updateTokens.append(word)
        # Convert the list to a single string and sentiment analyzing it
        updateString = " ".join(updateTokens)
        outcomes = sia.polarity_scores(updateString)
        preprocess.append(updateString)
        negative.append(outcomes['neg'])
        neutral.append(outcomes['neu'])
        positive.append(outcomes['pos'])
        compound.append(outcomes['compound'])
    else:
        negative.append(None)
        neutral.append(None)
        positive.append(None)
        compound.append(None)
        preprocess.append(None)

data_df['negativeTitle'] = negative
data_df['neutralTitle'] = neutral
data_df['positiveTitle'] = positive
data_df['compoundTitle'] = compound
data_df['title_prepro2'] = preprocess
data_df.to_csv(resultFileName, index=False)
