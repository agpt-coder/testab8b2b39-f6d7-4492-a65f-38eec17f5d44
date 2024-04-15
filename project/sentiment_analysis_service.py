from pydantic import BaseModel


class SentimentAnalysisResponse(BaseModel):
    """
    A model representing the response from the sentiment analysis endpoint. It provides the sentiment result of the analyzed text.
    """

    sentiment: str
    confidence: float


def sentiment_analysis(text: str) -> SentimentAnalysisResponse:
    """
    Analyzes input text to determine sentiment.

    Since no external libraries for Natural Language Processing (NLP) or sentiment analysis are allowed as per the constraints,
    and all operations regarding database and external APIs are to be executed with given or predefined models and structures,
    this function will simulate a basic sentiment analysis logic based on the presence of simple positive or negative words.

    This is a highly simplified and not accurate method of sentiment analysis and is used here just for demonstration.
    In a real-world scenario, one would use specialized libraries or microservices (e.g., TextBlob, NLTK, or external APIs) for sentiment analysis.

    Args:
        text (str): The text input to analyze for sentiment.

    Returns:
        SentimentAnalysisResponse: A model representing the response from the sentiment analysis endpoint. It provides the sentiment result of the analyzed text.

    Example:
        sentiment_analysis("This is an awesome day")
        > SentimentAnalysisResponse(sentiment='positive', confidence=0.8)

        sentiment_analysis("This is a terrible day")
        > SentimentAnalysisResponse(sentiment='negative', confidence=0.8)
    """
    positive_words = ["good", "great", "awesome", "happy", "joy", "pleased"]
    negative_words = ["bad", "terrible", "horrible", "sad", "unhappy", "displeased"]
    text_words = text.lower().split()
    positive_matches = sum((word in text_words for word in positive_words))
    negative_matches = sum((word in text_words for word in negative_words))
    if positive_matches > negative_matches:
        sentiment = "positive"
        confidence = min(1, 0.5 + 0.05 * positive_matches)
    elif negative_matches > positive_matches:
        sentiment = "negative"
        confidence = min(1, 0.5 + 0.05 * negative_matches)
    else:
        sentiment = "neutral"
        confidence = 0.5
    return SentimentAnalysisResponse(sentiment=sentiment, confidence=confidence)
