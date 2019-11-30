/*
    SQL select query for the first simple model

    This will most likely be moved to the archive eventually as it is superseded
    by newer versions of the query
*/
SELECT
    CONCAT(sales.Major, sales.Minor) AS PIN,        -- parcel id number
    sales.SalePrice,
    sales.DocumentDate,
    CASE
        WHEN parcels.WfntLocation > 0                -- 1-9 indicate particular bodies of water
            THEN TRUE
        ELSE                                         -- I infer that 0 means no waterfront
            FALSE
    END as WfntLocation,
    buildings.SqFtTotLiving
FROM sales                                           -- start the join with sales bc sale price is target
    INNER JOIN parcels ON (                          -- parcel major + minor is the unique identifier
            parcels.Major = sales.Major              -- (parcels are the things being sold in the sales)
        AND parcels.Minor = sales.Minor
    )
    INNER JOIN buildings ON (                        -- building belongs to one parcel
            buildings.Major = parcels.Major          -- parcel can have many buildings (unclear how often)
        AND buildings.Minor = parcels.Minor
    )
WHERE (
        date_part('year', sales.DocumentDate) = 2018 -- 2018 is the specified year
    AND sales.SalePrice > 0                          -- assume that sale price of 0 is bad data
)
ORDER BY sales.DocumentDate;
