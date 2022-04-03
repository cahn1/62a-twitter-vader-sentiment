import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


def render_query(term):
    return {
        'query': term,
        'tweet.fields': 'author_id',
        'user.fields': 'location',
        'max_results': 25
    }


def analyze_sentiment(text):
    try:
        sid_obj = SentimentIntensityAnalyzer()
        sentiment_dict = sid_obj.polarity_scores(text)
    except Exception as e:
        return 'sentiment_error', 'sentiment_error'
    score = round(sentiment_dict['compound'], 2)

    if score >= 0.05:
        result = f'Positive: {score}'
    elif score <= - 0.05:
        result = f'Negative: {score}'
    else:
        result = f'Neutral: {score}'
    # return result, f'{sentiment_dict}'
    return pd.Series([result, f'{sentiment_dict}'])


def to_float(row):
    return float(row.split()[1])
