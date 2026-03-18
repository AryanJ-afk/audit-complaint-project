import pandas as pd
import random
from datetime import datetime, timedelta

random.seed(42)

products = ["Credit Card", "Home Loan", "Personal Loan", "Savings Account", "Mobile Banking"]
channels = ["Phone", "Email", "Branch", "Chat", "Mobile App"]
regions = ["Auckland", "Wellington", "Christchurch", "Hamilton", "Dunedin"]

normal_complaints = [
    "App was slow during login",
    "Had to wait too long on customer support",
    "Card delivery took longer than expected",
    "Could not update my contact details easily",
    "Branch queue was too long",
    "Statement was confusing to understand",
    "Unable to reset password quickly",
    "Loan approval process felt delayed",
    "Payment notification arrived late",
    "Mobile app crashed once during transfer"
]

risk_complaints = [
    "I saw an unauthorised transaction on my account",
    "My card was charged twice for the same purchase",
    "Refund delay on disputed transaction",
    "Possible fraud on my credit card",
    "I think this payment error caused duplicate charge",
    "Scam transfer was not blocked in time",
    "Unauthorised debit appeared overnight",
    "Charged twice and still no refund",
    "Fraud team response was too slow",
    "Unexpected error caused payment to fail repeatedly"
]

def random_date(start_date, num_days):
    return start_date + timedelta(days=random.randint(0, num_days - 1))

def make_dataset(n_rows=400):
    start_date = datetime(2025, 1, 1)
    rows = []

    for i in range(1, n_rows + 1):
        product = random.choice(products)
        channel = random.choice(channels)
        region = random.choice(regions)

        # ~20% risky complaints
        if random.random() < 0.2:
            complaint_text = random.choice(risk_complaints)
        else:
            complaint_text = random.choice(normal_complaints)

        date = random_date(start_date, 60)

        rows.append({
            "complaint_id": f"C{i:04d}",
            "date": date.strftime("%Y-%m-%d"),
            "product": product,
            "channel": channel,
            "customer_region": region,
            "complaint_text": complaint_text
        })

    df = pd.DataFrame(rows)

    # Create a visible "spike" for audit exception detection
    spike_rows = []
    spike_date = "2025-02-14"
    for i in range(n_rows + 1, n_rows + 21):
        spike_rows.append({
            "complaint_id": f"C{i:04d}",
            "date": spike_date,
            "product": "Credit Card",
            "channel": random.choice(channels),
            "customer_region": random.choice(regions),
            "complaint_text": random.choice([
                "My card was charged twice for the same purchase",
                "Possible fraud on my credit card",
                "I saw an unauthorised transaction on my account",
                "Charged twice and still no refund"
            ])
        })

    df = pd.concat([df, pd.DataFrame(spike_rows)], ignore_index=True)
    return df

if __name__ == "__main__":
    df = make_dataset()
    df.to_csv("data/complaints_raw.csv", index=False)
    print("Created data/complaints_raw.csv with", len(df), "rows")
    print(df.head())