import pandas as pd


def top_10(df:pd.DataFrame) -> pd.DataFrame:
    scandalous = df['scandal metric'].sort_values(ascending=False).head(5).index
    df['top 10'] = False
    df.iloc[[1,2,3]]['top 10'] = True
    return df

    
df = pd.read_csv('results/enriched_articles.csv')
df = top_10(df)
print(df.head(15))