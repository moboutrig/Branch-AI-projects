import os
from webscraper import scrap
from utils import save_json,read_json
import pandas as pd
import analysis
from colorama import Fore

def choose_url():    
    choice = input('''     Choose a website :
        1 : CCN
        2 : IGN France
        3 : IGN Middle East (English)
        0 : skip webscraping (analyse existing data)
    ''')
    return int(choice)

def print_headline(title, url):
    print(f"\n\nEnriching {Fore.CYAN}'{title}'{Fore.RESET}")
    print(f"Read More : {Fore.BLUE}'{url}'{Fore.RESET}")

def main():
    
    # choose a website to scrap and scrap it
    user_selection = choose_url()
    if user_selection != 0: # 0 means 'skip webscraping'
        scrap(user_selection)
        
    # load the articles
    articles = read_json(user_selection)
    articles_df = pd.DataFrame(articles)
    
    
    # topic detection
    article_content = pd.Series(articles_df['title'] +' '+ articles_df['body'])
    topic_prediction = analysis.detect_topic(article_content)
    articles_df['topic'] = topic_prediction
    # article analysis : companies, sentiment, scandal
    results = []
    for [url, date, title, body, topic] in articles_df.values:
        
        print_headline(title, url)
        
        print('----------- topic detection result --------------')
        print(f'the topic of the article is {Fore.MAGENTA}{topic}{Fore.RESET}')

        companies = analysis.search_companies(title + body)
        
        print('\n--------- Sentiment Analysis ----------')
        title_sentiment = analysis.analyze_sentiment(title)
        body_sentiment = analysis.analyze_sentiment(body)
        
        # print sentiment analysis results
        print('title :', end='')
        analysis.print_sentiment_results(title_sentiment)
        print('body :', end='')
        analysis.print_sentiment_results(body_sentiment)
        
        # scandal detection
        scandal_metric, scandal_sentence = analysis.detect_scandal(companies, title + body)
        
        results.append({
            'url' : url,
            'date' : date,
            'companies' : companies,
            'title sentiment': title_sentiment.polarity,
            'title subjectivity': title_sentiment.subjectivity,
            'body sentiment': title_sentiment.polarity,
            'body subjectivity': title_sentiment.subjectivity,
            'most scandalous sentence' : scandal_sentence,
            'scandal metric' : round(scandal_metric*100)/100
        })
    
    # save the results of the analysis in a .csv file
    columns = ['url', 'date', 'companies', 'title sentiment', 'title subjectivity',
               'body sentiment', 'body subjectivity', 'most scandalous sentence', 'scandal metric']
    df = pd.DataFrame(results, columns=columns)
    df['topic'] = topic_prediction
    
    # set top 10
    df = analysis.top_10_scandal(df)
    df.to_csv('results/enriched_articles.csv')
    
    
if __name__ == '__main__':
    main()