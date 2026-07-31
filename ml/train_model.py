import pandas as pd
from preprocess import clean_text
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (accuracy_score,classification_report,confusion_matrix)
import joblib
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

df = pd.read_csv(r"C:\Users\azalf\nlp project\dataset\training_data.csv")

print("\nDataset Information:")
print(df.info())

print("\nDataset Shape:")
print(df.shape)

print("\nSentiment Distribution:")
print(df["sentiment"].value_counts())

print("\nMissing Values:")
print(df.isnull().sum())

#preprocessing
df["clean_review"] = df["review"].apply(clean_text)
print(df[["review", "clean_review"]].head())

#label Encoding
df["sentiment"] = df["sentiment"].map({
    "positive": 1,
    "negative": 0
})

print(df["sentiment"])
print(df.shape)
print(df["sentiment"].unique())
print(df["sentiment"].value_counts())

#train test
X = df["clean_review"]      
y = df["sentiment"]        

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print(f"Training Reviews : {X_train.shape}")
print(f"Testing Reviews  : {X_test.shape}")

print(f"Training Labels  : {y_train.shape}")
print(f"Testing Labels   : {y_test.shape}")

print("\nTraining Set Distribution")
print(y_train.value_counts())

print("\nTesting Set Distribution")
print(y_test.value_counts())

custom_stopwords = set(ENGLISH_STOP_WORDS)

keep_words = {
    "no",
    "not",
    "nor",
    "never",
    "none",
    "nobody",
    "nothing",
    "nowhere",
    "without"
}

custom_stopwords = list(set(ENGLISH_STOP_WORDS) - keep_words)

# TF-IDF Vectorizer
vectorizer = TfidfVectorizer(
    stop_words=custom_stopwords,
    max_features=50000,
    ngram_range=(1,2),
    min_df=2,
    max_df=0.95,
    sublinear_tf=True
)

X_train = vectorizer.fit_transform(X_train)

X_test = vectorizer.transform(X_test)

model = LogisticRegression(
    C=2,
    solver="liblinear",
    max_iter=3000,
    random_state=42
)

model.fit(X_train, y_train)

y_pred = model.predict(X_test)

print("Predictions generated successfully!")

accuracy = accuracy_score(y_test, y_pred)
print(f"\nAccuracy: {accuracy:.4f}")

print("\nClassification Report")
print(classification_report(y_test, y_pred))

cm = confusion_matrix(y_test, y_pred)
print("\nConfusion Matrix")
print(cm)

joblib.dump(model, "ml/model.pkl")
joblib.dump(vectorizer, "ml/vectorizer.pkl")