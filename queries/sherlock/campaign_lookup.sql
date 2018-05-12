SELECT
	campaign_id
	, campaign_name
FROM
	schema.table
WHERE
	client_id = {client_id}
GROUP BY
	campaign_id
	, campaign_name
ORDER BY
	campaign_name
