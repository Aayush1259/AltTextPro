from openai import OpenAI
from app.core.config import Config

class Sentiment:
    def __init__(self):
        self.client = OpenAI(api_key=Config.OPENAI_API_KEY)

    def analyze_sentiment(self, description):
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{
                    "role": "system",
                    "content": "Analyze the emotional content and sentiment of this image description. Return a JSON with: dominant_emotion, sentiment_score (-1 to 1), and emotional_elements list."
                }, {
                    "role": "user",
                    "content": description
                }]
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"Sentiment analysis failed: {str(e)}")