import streamlit as st
import pandas as pd
import sqlite3

st.set_page_config(page_title="Audit Complaint Dashboard", layout="wide")

DB_PATH = "output/complaints.db"


@st.cache_data
def load_data():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM complaints", conn)
    conn.close()

    df["date"] = pd.to_datetime(df["date"])
    return df


def generate_audit_summary(filtered_df: pd.DataFrame) -> str:
    total_complaints = len(filtered_df)
    flagged_df = filtered_df[filtered_df["exception_flag"] == 1]
    flagged_count = len(flagged_df)

    if total_complaints == 0:
        return "No complaints found for the selected filters."

    if flagged_count == 0:
        return (
            f"No flagged exceptions were detected across {total_complaints} complaints "
            f"for the selected filters."
        )

    flag_rate = flagged_count / total_complaints * 100

    top_product = (
        flagged_df["product"].value_counts().idxmax()
        if not flagged_df["product"].dropna().empty
        else "Unknown"
    )

    top_reason = (
        flagged_df["exception_reason"].value_counts().idxmax()
        if not flagged_df["exception_reason"].dropna().empty
        else "Unknown"
    )

    spike_df = (
        filtered_df.groupby(["date", "product"])["complaint_id"]
        .count()
        .reset_index(name="complaint_count")
        .sort_values("complaint_count", ascending=False)
    )

    spike_text = ""
    if not spike_df.empty and spike_df.iloc[0]["complaint_count"] >= 10:
        top_spike = spike_df.iloc[0]
        spike_date = pd.to_datetime(top_spike["date"]).strftime("%Y-%m-%d")
        spike_text = (
            f" A potential spike was detected on {spike_date} for "
            f"{top_spike['product']} with {int(top_spike['complaint_count'])} complaints."
        )

    return (
        f"Audit summary: {flagged_count} of {total_complaints} complaints "
        f"({flag_rate:.1f}%) were flagged as exceptions. "
        f"The highest concentration of flagged complaints was in {top_product}. "
        f"The most common exception theme was '{top_reason}'."
        f"{spike_text}"
    )


df = load_data()

st.title("Audit Complaint Exception Dashboard")
st.markdown("Identify risky complaint patterns, exception themes, and unusual spikes for audit review.")

# Sidebar filters
st.sidebar.header("Filters")

product_filter = st.sidebar.multiselect(
    "Product",
    options=sorted(df["product"].dropna().unique()),
    default=sorted(df["product"].dropna().unique())
)

channel_filter = st.sidebar.multiselect(
    "Channel",
    options=sorted(df["channel"].dropna().unique()),
    default=sorted(df["channel"].dropna().unique())
)

region_filter = st.sidebar.multiselect(
    "Customer Region",
    options=sorted(df["customer_region"].dropna().unique()),
    default=sorted(df["customer_region"].dropna().unique())
)

filtered_df = df[
    (df["product"].isin(product_filter)) &
    (df["channel"].isin(channel_filter)) &
    (df["customer_region"].isin(region_filter))
].copy()

# Summary box
summary_text = generate_audit_summary(filtered_df)
st.info(summary_text)

# KPIs
total_complaints = len(filtered_df)
flagged_exceptions = int(filtered_df["exception_flag"].sum())
flag_rate = (flagged_exceptions / total_complaints * 100) if total_complaints > 0 else 0

col1, col2, col3 = st.columns(3)
col1.metric("Total Complaints", f"{total_complaints}")
col2.metric("Flagged Exceptions", f"{flagged_exceptions}")
col3.metric("Flag Rate", f"{flag_rate:.1f}%")

st.divider()

# Complaints over time
st.subheader("Complaints Over Time")
daily_counts = (
    filtered_df.groupby("date")["complaint_id"]
    .count()
    .reset_index(name="complaint_count")
    .sort_values("date")
)
st.line_chart(daily_counts.set_index("date"))

# Flagged by product
col4, col5 = st.columns(2)

with col4:
    st.subheader("Flagged Exceptions by Product")
    flagged_by_product = (
        filtered_df[filtered_df["exception_flag"] == 1]
        .groupby("product")["complaint_id"]
        .count()
        .reset_index(name="flagged_count")
        .sort_values("flagged_count", ascending=False)
    )
    if not flagged_by_product.empty:
        st.bar_chart(flagged_by_product.set_index("product"))
    else:
        st.info("No flagged exceptions for current filters.")

with col5:
    st.subheader("Exception Reasons")
    exception_reasons = (
        filtered_df[filtered_df["exception_flag"] == 1]
        .groupby("exception_reason")["complaint_id"]
        .count()
        .reset_index(name="reason_count")
        .sort_values("reason_count", ascending=False)
    )
    if not exception_reasons.empty:
        st.bar_chart(exception_reasons.set_index("exception_reason"))
    else:
        st.info("No exception reasons for current filters.")

st.divider()

# Potential spike days
st.subheader("Potential Spike Days")
spike_df = (
    filtered_df.groupby(["date", "product"])["complaint_id"]
    .count()
    .reset_index(name="complaint_count")
    .sort_values("complaint_count", ascending=False)
)

spike_df = spike_df[spike_df["complaint_count"] >= 10]

if not spike_df.empty:
    st.dataframe(spike_df, use_container_width=True)
else:
    st.info("No spike days found for current filters.")

st.divider()

# Detailed flagged complaints
st.subheader("Flagged Complaint Details")
flagged_details = filtered_df[filtered_df["exception_flag"] == 1][[
    "complaint_id",
    "date",
    "product",
    "channel",
    "customer_region",
    "complaint_text",
    "sentiment_score",
    "risk_keyword",
    "exception_reason"
]].sort_values("date", ascending=False)

if not flagged_details.empty:
    st.dataframe(flagged_details, use_container_width=True)
else:
    st.info("No flagged complaints for current filters.")