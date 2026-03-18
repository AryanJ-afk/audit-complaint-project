# Audit Complaint Exception Detection Dashboard

## Overview

This project is a data analytics prototype for Audit & Assurance teams,
designed to identify high-risk complaint patterns, exception trends, and
potential control failures.

## Objective

-   Detect high-risk complaints (fraud, duplicate charges)
-   Identify unusual spikes
-   Surface exception themes
-   Support audit prioritisation

## Tech Stack

-   Python
-   SQLite (SQL)
-   Streamlit
-   TextBlob

## Workflow

1.  Generate synthetic complaint data
2.  Process data (sentiment + keyword tagging)
3.  Flag exceptions
4.  Store in SQLite
5.  Visualise in Streamlit dashboard

## Exception Logic

-   Negative sentiment threshold
-   Risk keyword detection
-   Spike detection

## Dashboard Features

-   KPI metrics
-   Trend analysis
-   Exception breakdown
-   Drill-down table

## Limitations

-   Synthetic dataset
-   Basic sentiment model
-   Rule-based logic

## Future Improvements

-   Real datasets
-   Advanced NLP models
-   Automated alerts
