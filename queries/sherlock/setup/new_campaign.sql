SELECT
	day
	, campaign_name
FROM
  schema.dim_table
WHERE
	client_id = {client_id}
	AND day BETWEEN '{start_date}' AND '{end_date}'
	AND campaign_status = 0
GROUP BY
  day
  , campaign_name
ORDER BY
  day
  , campaign_name
