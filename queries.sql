/*--------------------------------------------------------------------------------------
| Bellow query will answer the question:
| From the two most commonly appearing regions, which is the latest datasource?
|--------------------------------------------------------------------------------------*/
WITH most_common_regions 
	AS (
		SELECT region_id
		FROM (SELECT COUNT (*), region_id
				FROM apirest_trips 
			GROUP BY region_id
			ORDER BY COUNT (*) DESC
			 ) regions
		 LIMIT  2
		)
SELECT d.datasource
  FROM apirest_trips t,
	   most_common_regions common,
	   apirest_datasources d
 WHERE t.region_id = common.region_id
   AND t.datasource_id = d.id
ORDER BY datetime DESC
LIMIT 1;


/*--------------------------------------------------------------------------------------
| Bellow query will answer the question:
| What regions has the "cheap_mobile" datasource appeared in?
|--------------------------------------------------------------------------------------*/

SELECT DISTINCT r.region
  FROM apirest_trips t,
	   apirest_regions r,
	   apirest_datasources d
 WHERE t.region_id = r.id
   AND t.datasource_id = d.id
   AND d.datasource = 'cheap_mobile';