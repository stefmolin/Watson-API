SELECT
	day
  , campaign_sampling_ratio
FROM
  schema.table
WHERE
  client_id = {client_id}
  AND campaign_id = {campaign_id}
  AND day BETWEEN '{start_date}' AND '{end_date}'
GROUP BY
  day
ORDER BY
  day
