# NLP-Web-Scraper

In one word, this project consists of an application that keeps abreast of current events : *The analysts get their information from the news and the amount of available information is limitless. Having a platform that helps to detect the relevant information is definitely valuable.*

This application can :
- connect to a news data source
- detect the **topic** of an article
- detect the **companies/organizations** mentioned in the article
- **analyse the sentiment** of an article
- detect **environmental disaster** for the detected companies

More detail below

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the dependencies. These can be found in the **environment.yml** file

```bash
pip install <dependency>
# e.g pip install textblob
```

An alternative way to setup the environment for the project is to create one using [conda](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&ved=2ahUKEwjV1vyI8t-EAxXMVKQEHekeAyEQFnoECBsQAQ&url=https%3A%2F%2Fconda.io%2Fdocs%2Fuser-guide%2Finstall%2F&usg=AOvVaw20qqAbuNE4qDg14dVlCHz5&opi=89978449) if you're at ease with it :
```bash
conda env create -f environment.yml
conda activate myenv
# Verify that the new environment was installed correctly:
conda env list
```

## Usage
Run the program :
```bash
bash run.sh
#### OR ####
cd src
python3 main.py
```
Then you'll have to choose a website you're interested in. The program will collect data and analyse them.
You can check the results in real time in the terminal and stop the program manually (press Ctrl+C) whenever you want.
The results will be stored in the **results/** directory :
- **json files** : contains the collected articles from the selected website.
- **enriched_articles.csv** : contain a detailed list of the results for each article.




# How does it work ?
Want to understand how it works ? Well, this section is here for you !

## Webscraping
Web-scraping is a technique for the automated extraction of structured content.It is mostly handled with the [beautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) python library. In other words, it automatically collects data from a site. Note that since every site has a different strucure, you have to create a webscraper for each website you want to scrap. The method stay very similar tho. It might be possible to create a "general-webscraper", but that would be less accurate and would deserve it's own project.

## Topic Classification
The article can be classified into 5 topic : **Tech, sport, buisness, entertainment, politics**
For that I've created a very simple **Machine Learning model**. We're using the **SVC model** since the input in a whole article transformed into vectors using the **TFI-DF vectorization** method. We end up with an [accuracy](https://developers.google.com/machine-learning/crash-course/classification/accuracy) of 97.41%, which is completly fine. You can see more details in the **src/topic_detection.ipynb** file

## Detect companies using NLP
*NLP for Natural Language Processing is a discipline that focuses on the understanding, manipulation and generation of natural language by machines.  Thus, NLP is really at the interface between computer science and linguistics. It is about the ability of the machine to interact directly with humans.*

This is a pretty complex domain so we're not going to dive into the NLP technics here. But note that you can easily implement these in Python :
```python
import spacy
nlp = spacy.load('en_core_web_md')
doc = nlp(article_content)
    
companies = set([
    X.text
    for X in doc.ents
    if X.label_ == 'ORG'
])
```

## Sentiment Analysis
![sentiment analysis illustration](https://github.com/AdrienLanglois/NLP-Web-Scraper/blob/main/pictures/Screenshot%20from%202024-03-06%2016-53-27.png)


For this part we're using a pre-trained Machine Learning model since labelled news data for sentiment analysis are very expensive. Moreover there's so much existing model that sometimes there's no need to train one from scratch.
In practice, we can use the [Textblob]() library for that :
```python
from textblob import TextBlob
blob = TextBlob(text)    
sentiment = blob.sentiment
```

## Scandal Detection : Embedding and distance
The idea here is to define **keywords that correspond to environmental disaster** that may be caused by companies: pollution, deforestation etc... It's important to pay attention to **not use ambiguous words** that make sense in the context of an environmental disaster but also in another context. This would lead to detect a false positive natural disaster.

Then we extract the sentences we want to analyse (in our case, the sentences that contains a company) and compute the distance between every keyword and the words of the sentence. Then we calculate the mean distance so that we have an evaluation of whether the sentence has something to deal with environment disaster or not.
