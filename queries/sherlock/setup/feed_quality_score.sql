SELECT
  day
  , CASE WHEN COUNT(DISTINCT day) = 0 THEN 0
         ELSE (SUM(catalog_quality)/COUNT(DISTINCT day))/10000 END AS feed_quality
  , MAX(last_date_import) AS feed_import
FROM
  schema.fact_table AS fc
JOIN
  (SELECT
    partner_id
    , client_id
  FROM
    schema.dim_table
  WHERE
    client_id = {client_id}
  GROUP BY
    partner_id
    , client_id) c
ON
  c.partner_id = fc.partner_id
WHERE
	client_id = {client_id}
	AND day BETWEEN '{start_date}' AND '{end_date}'
GROUP BY
  client_id
  , day
ORDER BY
  day
