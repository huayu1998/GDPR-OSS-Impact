# packages imported
import pandas as pd
import yake
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# global variable set up
dataFileName = 'gdpr_sentiment_analysis.csv'
keywordsTextFileName = 'gdpr2keywordsBody.txt'
wordCloudFileName = 'gdprBody.png'
columnName = 'title_prepro2'

# help function
def yakeKeywordsAnalysis(text):
    # keywords extractor parameters
    language = 'en'
    max_ngram_size = 2
    deduplication_threshold = 0.9
    deduplication_algo = 'seqm' # seqm, leve, jaro
    windowSize = 1
    numOfKeywords = 50

    # run the keyword extractor
    kw_extractor = yake.KeywordExtractor(lan=language, n=max_ngram_size, dedupLim=deduplication_threshold, dedupFunc=deduplication_algo, windowsSize=windowSize, top=numOfKeywords, features=None)
    keywords = kw_extractor.extract_keywords(text)
    yakeF = open(keywordsTextFileName,"w+")
    yakeF.write('Note: The lower the score, the more relevant the keyword is!\n')
    yakeF.write('Total keywords: '+str(len(keywords))+' & max_ngram_size used: '+str(max_ngram_size)+'\n\n')
    for kw in keywords:
        yakeF.write(kw[0]+': ')
        yakeF.write(str(kw[1]))
        yakeF.write('\n')
    yakeF.close()

def wordCloud(text):
    wordCloud = WordCloud(width = 800, height = 500, background_color = 'white', max_words = 50, random_state = 21, max_font_size= 100).generate(text)
    plt.imshow(wordCloud, interpolation='bilinear')
    plt.axis("off")
    # image save
    wordCloud.to_file(wordCloudFileName)

# read data file
df = pd.read_csv(dataFileName)
items = df[columnName]
keywordDoc = ''

# get and add all texts together and run keywords analysis
for item in items:
    if type(item) is str:
        keywordDoc += item + ' '
yakeKeywordsAnalysis(keywordDoc)
wordCloud(keywordDoc)