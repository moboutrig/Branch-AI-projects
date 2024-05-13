import spacy
from textblob import TextBlob
from colorama import Fore
import pandas as pd
import numpy as np
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer

############ print results #################

def print_company_results(companies):
    if len(companies) == 0:
        print('no company detected')
        return
    
    company_w = 'company' if len(companies)==0 else 'companies'
    
    print(f'{len(companies)} {company_w} detected :')
    for c in companies:
        print(f'    - {c}')
        
def print_sentiment_results(sentiment)->None:
    polarity, subjectivity = sentiment
    
    if polarity == 0 and subjectivity == 0:
        print('neutral')
        return
    
    polarity_color = Fore.RED if polarity<0 else Fore.GREEN
    subj_color = Fore.LIGHTYELLOW_EX if subjectivity>0.2 else Fore.WHITE
    print(f'''sentiment={polarity_color}{100 * polarity:.2f}%{Fore.RESET}; subjectivity = {subj_color}{100 * subjectivity:.2f}% {Fore.RESET}''')
        
    
################### analysis ########################

def analyze_sentiment(text):
    # get sentiment and subjectivity
    # which are values between -1 and 1
    blob = TextBlob(text)    
    sentiment = blob.sentiment
    
    return sentiment

# companies analysis

def search_companies(article_content:str):
    print('\n--------- Searching for companies ----------')

    nlp = spacy.load('en_core_web_md')
    doc = nlp(article_content)
    
    companies = set([
        X.text
        for X in doc.ents
        if X.label_ == 'ORG'
    ])
    
    print_company_results(companies)
    return companies


    
################# Scandal Detection ########################""
    
def get_companies_sentences(companies:list, text:str) -> list[str]:
    res = []
    
    for sentence in text.split('.'):
        for company in companies:
            if company in sentence:
                res.append(sentence)
            
    return res    
    
def detect_scandal(companies, text):
    print('-------- computing embeding and word distances ---------\n This will take a few seconds ...')
    
    nlp = spacy.load('en_core_web_md')

    keywords = [
    "Spill",
    "Leak",
    "Contamination",
    "Erosion",
    "Deforestation",
    "Acidification",
    "Overfishing",
    "Dumping",
    "Poisoning",
    "Wastewater",
    "Smog",
    "Eutrophication",
    "Habitat",
    "Destruction",
    "Soot",
    "Sulfur",
    "dioxide",
    "Mercury",
    "Pesticides",
    "Herbicides",
    "Oil",
    "Cyanide",
    "Pollution",
    "Deforestation"
    ]
    
    company_sentences = get_companies_sentences(companies, text)
    similarities = {}
    
    for keyword in keywords:
        for sentence in company_sentences:

            kw_token = nlp(keyword)
            sentence_token = nlp(sentence)
            similarity = kw_token.similarity(sentence_token)
            
            similarities[similarity] = keyword + ' : ' + sentence
    
    max = np.max(list(similarities.keys()))
    sentence = similarities[max]
    return max, sentence

# topic detection
        
def detect_topic(article):
    print('------------ topic detection -------------')
    
    tfidf_vectorizer = TfidfVectorizer(max_features=1000)
    X = tfidf_vectorizer.fit_transform(article)
        
    model = pickle.load(open('results/topic_classifier.pkl', 'rb'))
    predictions = list(model.predict(X))
    
    # decode prediction
    topic_decoder = {1:'tech', 2:'sport', 3:'buisness', 4:'entertainment', 5:'politics'}
    for i, pred in enumerate(predictions):
        predictions[i] = topic_decoder[pred]
    
    return predictions
    
    
def top_10_scandal(df:pd.DataFrame) -> pd.DataFrame:
    pd.options.mode.chained_assignment = None  # ignore warning
    
    scandalous_idx = df['scandal metric'].sort_values(ascending=False).head(10).index
    df['top 10'] = False
    df['top 10'].iloc[scandalous_idx] = True
    return df
    