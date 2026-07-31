import pandas as pd
from django.shortcuts import render
from ml.predict import predict_sentiment


def home(request):
    return render(request, "sentiment/index.html")


def analyze(request):

    if request.method == "POST":

        review = request.POST.get("review_text")
       

        result = predict_sentiment(review)


        # ---------------- Recommendation ----------------
        sentiment = result["sentiment"]
        confidence = result["confidence"]

        if sentiment == "Positive":
            if confidence >= 95:
                recommendation = (
                    "🌟 Outstanding Positive Sentiment! "
                    "This review expresses extremely strong positive opinions, making the movie appear highly recommended."
                )
            elif confidence >= 85:
                recommendation = (
                    "🍿 Highly Recommended! "
                    "The review is strongly positive and suggests a very enjoyable viewing experience."
                )
            elif confidence >= 70:
                recommendation = (
                    "👍 Worth Watching. "
                    "The review is generally positive, although individual preferences may vary."
                )
            else:
                recommendation = (
                    "🙂 Slightly Positive. "
                    "The review leans positive, but reading additional reviews may help you make a more informed decision."
                )
        else:
            if confidence >= 95:
                recommendation = (
                    "🚫 Strongly Not Recommended. "
                    "This review expresses extremely negative opinions and indicates a poor viewing experience."
                )
            elif confidence >= 85:
                recommendation = (
                    "😕 Not Recommended. "
                    "The review highlights several negative aspects that may affect your experience."
                )
            elif confidence >= 70:
                recommendation = (
                    "⚠️ Proceed with Caution. "
                    "The review is generally negative, but checking additional reviews is recommended."
                )
            else:
                recommendation = (
                    "🤔 Slightly Negative. "
                    "The review leans negative, but opinions may differ. Consider reading more reviews before deciding."
                )

        result["recommendation"] = recommendation
        # ------------------------------------------------

        result.update({
            "result": True,
            "original_text": review,
            "word_count": len(review.split()),
            "char_count": len(review),
        })

        return render(
            request,
            "sentiment/index.html",
            result
        )

    return render(request, "sentiment/index.html")

def analyze_csv(request):

    if request.method == "POST":

        csv_file = request.FILES.get("csv_file")

        if not csv_file:
            return render(request, "sentiment/index.html", {
                "csv_error": "Please select a CSV file."
            })

        df = pd.read_csv(csv_file)

        print(df.head())

        total_words = 0
        total_characters = 0
        positive_count = 0
        negative_count = 0


        for review in df["review"]:

            result = predict_sentiment(review)

            # Word and character count
            total_words += len(review.split())
            total_characters += len(review)


            # Sentiment count
            if result["sentiment"] == "Positive":
                positive_count += 1
            else:
                negative_count += 1             

        return render(
            request,
            "sentiment/csv_dashboard.html",
            {
                "total_reviews": len(df),
                "total_words": total_words,
                "total_characters": total_characters,
                "positive_count": positive_count,
                "negative_count": negative_count
            }
        )

    return render(request, "sentiment/index.html")