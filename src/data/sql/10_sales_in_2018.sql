SELECT COUNT(*)
FROM sales
WHERE date_part('year', sales.DocumentDate) = 2018;