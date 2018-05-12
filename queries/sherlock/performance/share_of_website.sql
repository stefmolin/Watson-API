SELECT
  fc.day AS day
  , fc.campaign_id AS campaign_id
  , c.partner_id AS partner_id
  , SUM(sales_all_post_click) / sales AS percentage_of_website
FROM
  schema.fact_table fc
JOIN
  (SELECT
    partner_id
    , client_id
    , campaign_id
  FROM
    schema.dim_table
  WHERE
    campaign_id = {campaign_id}
  GROUP BY
    partner_id
    , client_id
    , campaign_id) c
ON
  c.campaign_id = fc.campaign_id
JOIN
  schema.stats_table website
ON
  website.partner_id = c.partner_id
  AND website.day = fc.day
  AND period = 1
WHERE
  fc.campaign_id = {campaign_id}
  AND fc.day BETWEEN '{start_date}' AND '{end_date}'
GROUP BY
  fc.day
  , fc.campaign_id
  , c.partner_id
  , sales
