import pandas as pd
import sqlite3

def main():
    df = pd.read_csv("output/complaints_processed.csv")

    conn = sqlite3.connect("output/complaints.db")

    df.to_sql("complaints", conn, if_exists="replace", index=False)

    print("Loaded output/complaints_processed.csv into output/complaints.db")
    print("Table created: complaints")
    print("Row count:", len(df))

    conn.close()


if __name__ == "__main__":
    main()