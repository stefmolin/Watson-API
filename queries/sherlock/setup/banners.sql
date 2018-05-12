SELECT
	day
	, client_id
	, campaign_id
	, width || 'x' || height as banner_size
FROM
	schema.fact_table s
LEFT OUTER JOIN
	schema.dim_table b
ON
  s.banner_id = b.banner_id
WHERE
	client_id = {client_id}
	AND campaign_id = {campaign_id}
	AND day BETWEEN '{start_date}' AND '{end_date}'
GROUP BY
	day
	, client_id
	, campaign_id
	, width || 'x' || height
HAVING
  SUM(displays) > 10
