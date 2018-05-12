SELECT
  day
  , campaign_id
  , CASE WHEN SUM(sales_all_post_click) = 0 THEN 0
         ELSE SUM(sales_all_post_click) / SUM(sales_all_post_click_non_deduplicated) END AS dedup_ratio
FROM
  schema.table AS stats
WHERE
  campaign_id = {campaign_id}
  AND day BETWEEN '{start_date}' AND '{end_date}'
GROUP BY
  day
  , campaign_id
ORDER BY
  day
