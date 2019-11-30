SELECT COUNT(*)
FROM sales
WHERE (
        date_part('year', sales.DocumentDate) = 2018
    AND sales.SalePrice > 0                           -- assume that sale price of 0 is bad data
);