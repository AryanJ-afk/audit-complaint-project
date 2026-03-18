-- 1. Total complaints
SELECT COUNT(*) AS total_complaints
FROM complaints;

-- 2. Total flagged exceptions
SELECT COUNT(*) AS total_flagged_exceptions
FROM complaints
WHERE exception_flag = 1;

-- 3. Flagged complaints by product
SELECT
    product,
    COUNT(*) AS flagged_count
FROM complaints
WHERE exception_flag = 1
GROUP BY product
ORDER BY flagged_count DESC;

-- 4. Daily complaint volume by product
SELECT
    date,
    product,
    COUNT(*) AS complaint_count
FROM complaints
GROUP BY date, product
ORDER BY date, complaint_count DESC;

-- 5. Most common exception reasons
SELECT
    exception_reason,
    COUNT(*) AS reason_count
FROM complaints
WHERE exception_flag = 1
GROUP BY exception_reason
ORDER BY reason_count DESC;

-- 6. Complaints by channel
SELECT
    channel,
    COUNT(*) AS complaint_count
FROM complaints
GROUP BY channel
ORDER BY complaint_count DESC;

-- 7. High-risk complaint details
SELECT
    complaint_id,
    date,
    product,
    channel,
    customer_region,
    complaint_text,
    sentiment_score,
    risk_keyword,
    exception_reason
FROM complaints
WHERE exception_flag = 1
ORDER BY date DESC;

-- 8. Potential spike day check
SELECT
    date,
    product,
    COUNT(*) AS complaint_count
FROM complaints
GROUP BY date, product
HAVING COUNT(*) >= 10
ORDER BY complaint_count DESC;