from typing import List, Dict, Any
from collections import Counter
import re
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


class SentimentAnalyzer:
    def __init__(self):
        self.analyzer = SentimentIntensityAnalyzer()

    def analyze_text(self, text: str) -> Dict[str, Any]:
        """Analyze sentiment of a single text."""
        if not text:
            return {"compound": 0.0, "positive": 0.0, "negative": 0.0, "neutral": 1.0}

        scores = self.analyzer.polarity_scores(text)
        return {
            "compound": scores["compound"],
            "positive": scores["pos"],
            "negative": scores["neg"],
            "neutral": scores["neu"]
        }

    def get_sentiment_label(self, compound_score: float) -> str:
        """Convert compound score to sentiment label."""
        if compound_score >= 0.05:
            return "positive"
        elif compound_score <= -0.05:
            return "negative"
        else:
            return "neutral"

    def extract_keywords(self, texts: List[str], top_n: int = 20) -> List[Dict[str, Any]]:
        """Extract common keywords from texts with their sentiment."""
        stop_words = {
            "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
            "of", "with", "by", "from", "as", "is", "was", "are", "were", "been",
            "be", "have", "has", "had", "do", "does", "did", "will", "would",
            "could", "should", "may", "might", "must", "shall", "can", "need",
            "this", "that", "these", "those", "i", "you", "he", "she", "it",
            "we", "they", "what", "which", "who", "whom", "whose", "where",
            "when", "why", "how", "all", "each", "every", "both", "few", "more",
            "most", "other", "some", "such", "no", "nor", "not", "only", "own",
            "same", "so", "than", "too", "very", "just", "also", "now", "here",
            "there", "then", "once", "if", "my", "your", "its", "our", "their",
            "app", "use", "using", "used", "really", "very", "much", "get", "got",
            "one", "two", "first", "new", "even", "still", "well", "way", "many"
        }

        word_sentiments = {}
        word_counts = Counter()

        for text in texts:
            if not text:
                continue

            words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
            sentiment = self.analyze_text(text)

            for word in words:
                if word not in stop_words:
                    word_counts[word] += 1
                    if word not in word_sentiments:
                        word_sentiments[word] = []
                    word_sentiments[word].append(sentiment["compound"])

        keywords = []
        for word, count in word_counts.most_common(top_n * 2):
            if count >= 2:
                avg_sentiment = sum(word_sentiments[word]) / len(word_sentiments[word])
                keywords.append({
                    "word": word,
                    "count": count,
                    "sentiment": self.get_sentiment_label(avg_sentiment),
                    "score": round(avg_sentiment, 3)
                })

        return sorted(keywords, key=lambda x: x["count"], reverse=True)[:top_n]

    def analyze_reviews(self, reviews: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze sentiment for a list of reviews."""
        if not reviews:
            return {
                "overall": "neutral",
                "breakdown": {"positive": 0, "negative": 0, "neutral": 0},
                "average_score": 0.0,
                "keywords": []
            }

        sentiments = []
        texts = []

        for review in reviews:
            comment = review.get("comment", "")
            if comment:
                texts.append(comment)
                sentiment = self.analyze_text(comment)
                sentiments.append(sentiment)

        if not sentiments:
            return {
                "overall": "neutral",
                "breakdown": {"positive": 0, "negative": 0, "neutral": 0},
                "average_score": 0.0,
                "keywords": []
            }

        breakdown = {"positive": 0, "negative": 0, "neutral": 0}
        total_compound = 0.0

        for s in sentiments:
            total_compound += s["compound"]
            label = self.get_sentiment_label(s["compound"])
            breakdown[label] += 1

        avg_compound = total_compound / len(sentiments)
        overall = self.get_sentiment_label(avg_compound)

        keywords = self.extract_keywords(texts)

        return {
            "overall": overall,
            "breakdown": breakdown,
            "average_score": round(avg_compound, 3),
            "keywords": keywords
        }


sentiment_analyzer = SentimentAnalyzer()
