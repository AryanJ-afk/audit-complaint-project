import pandas as pd
from textblob import TextBlob

RISK_KEYWORDS = {
    "unauthorised": "Unauthorised transaction risk",
    "fraud": "Fraud-related complaint",
    "duplicate charge": "Duplicate charge risk",
    "charged twice": "Duplicate charge risk",
    "refund delay": "Refund process issue",
    "scam": "Scam/fraud risk",
    "error": "System/payment error"
}

NEGATIVE_SENTIMENT_THRESHOLD = -0.30


def get_sentiment(text: str) -> float:
    if pd.isna(text):
        return 0.0
    return round(TextBlob(str(text)).sentiment.polarity, 3)


def detect_risk_keyword(text: str) -> str:
    if pd.isna(text):
        return "None"

    text_lower = str(text).lower()
    for keyword, label in RISK_KEYWORDS.items():
        if keyword in text_lower:
            return label

    return "None"


def main():
    df = pd.read_csv("data/complaints_raw.csv")

    df["sentiment_score"] = df["complaint_text"].apply(get_sentiment)
    df["risk_keyword"] = df["complaint_text"].apply(detect_risk_keyword)

    df["negative_sentiment_flag"] = df["sentiment_score"] < NEGATIVE_SENTIMENT_THRESHOLD
    df["keyword_flag"] = df["risk_keyword"] != "None"

    df["exception_flag"] = df["negative_sentiment_flag"] | df["keyword_flag"]

    def build_exception_reason(row):
        reasons = []
        if row["negative_sentiment_flag"]:
            reasons.append("High negative sentiment")
        if row["keyword_flag"]:
            reasons.append(row["risk_keyword"])
        return "; ".join(reasons) if reasons else "Not flagged"

    df["exception_reason"] = df.apply(build_exception_reason, axis=1)

    output_columns = [
        "complaint_id",
        "date",
        "product",
        "channel",
        "customer_region",
        "complaint_text",
        "sentiment_score",
        "risk_keyword",
        "exception_flag",
        "exception_reason"
    ]

    df[output_columns].to_csv("output/complaints_processed.csv", index=False)

    print("Created output/complaints_processed.csv")
    print("\nFlag summary:")
    print(df["exception_flag"].value_counts())
    print("\nSample flagged rows:")
    print(df[df["exception_flag"]].head(10)[
        ["complaint_id", "complaint_text", "sentiment_score", "risk_keyword", "exception_reason"]
    ])


if __name__ == "__main__":
    main()