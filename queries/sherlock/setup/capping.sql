SELECT
	day
  , campaign_capping_starting_day
  , campaign_capping_ending_day
  , daily_capping
  , campaign_capping_since_last_visit
  , partner_capping_since_last_visit
  , campaign_lifetime_capping
FROM
  schema.table
WHERE
  client_id = {client_id}
  AND campaign_id = {campaign_id}
  AND day BETWEEN '{start_date}' AND '{end_date}'
GROUP BY
  day
  , campaign_capping_starting_day
  , campaign_capping_ending_day
  , daily_capping
  , campaign_capping_since_last_visit
  , partner_capping_since_last_visit
  , campaign_lifetime_capping
ORDER BY
  day
