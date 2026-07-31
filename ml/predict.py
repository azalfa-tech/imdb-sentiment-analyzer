import joblib
from ml.preprocess import clean_text

# Load model and vectorizer
model = joblib.load("ml/model.pkl")
vectorizer = joblib.load("ml/vectorizer.pkl")


def predict_sentiment(review):

    # Clean text
    cleaned_review = clean_text(review)

    # Convert to TF-IDF
    review_vector = vectorizer.transform([cleaned_review])

    # Prediction
    prediction = model.predict(review_vector)[0]

    if hasattr(model, "predict_proba"):
        probabilities = model.predict_proba(review_vector)[0]

        negative_prob = round(probabilities[0] * 100, 2)
        positive_prob = round(probabilities[1] * 100, 2)
        confidence = max(positive_prob, negative_prob)

    else:
        negative_prob = 0
        positive_prob = 0
        confidence = 0

    sentiment = "Positive" if prediction == 1 else "Negative"

    return {
        "sentiment": sentiment,
        "confidence": confidence,
        "positive_prob": positive_prob,
        "negative_prob": negative_prob
    }