SELECT b.bank_name, COUNT(*) AS review_count
FROM reviews r
JOIN banks b ON b.bank_id = r.bank_id
GROUP BY b.bank_name
ORDER BY review_count DESC;

SELECT b.bank_name, ROUND(AVG(r.rating)::numeric, 2) AS average_rating
FROM reviews r
JOIN banks b ON b.bank_id = r.bank_id
GROUP BY b.bank_name
ORDER BY average_rating DESC;

SELECT
    SUM(CASE WHEN review_text IS NULL THEN 1 ELSE 0 END) AS null_review_text,
    SUM(CASE WHEN rating IS NULL THEN 1 ELSE 0 END) AS null_rating,
    SUM(CASE WHEN review_date IS NULL THEN 1 ELSE 0 END) AS null_review_date
FROM reviews;
