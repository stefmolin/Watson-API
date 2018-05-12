# Watson API
The Watson API runs queries in the background using Celery.

## How It Works
Those wishing to add queries to the API simply need to add a SQL file (file
extension `.sql`) to the `queries` directory (anywhere they choose inside that
directory). Once the file is included, an endpoint will be generated of the form
`[hostname]/api/<api_version>/query/<subdirectories_if_any>/<query_file_name>` like
`[hostname]/api/v1/query/sherlock/sample_query` or `[hostname]/api/v1/query/sample_query`.
After a successful `POST` request to these endpoints, you will see the resource
where the results for that query can be retrieved with a `GET` request (when they are ready).

## Parameterized Queries
Most use-cases will require the input of parameters into the queries. This can be
achieved by including the parameters in the SQL files as `{<parameter_name>}`
where replacing them with the value would yield a valid SQL query. Then to run
your query, simply add all your query parameters as a query string to your request.
For example, if the query needs `start_date` and `end_date` include something like
`date BETWEEN {start_date} AND {end_date}` in your query and make your `POST` request like
`curl -i -X POST [hostname]/api/v1/query/sherlock/sample_query?start_date=2015-09-28&end_date=2018-06-08`.
Your query will then be properly parameterized!

Note that should you forget the query parameters or misspell them, you will
receive a response with the query showing its parameters and the parameters you
need to provide instead of the resource to retrieve your result.

## Data Retention
Query results will be automatically removed 24 hours after their creation.

## Caveats
Note that this has been built for small queries. Issues may arise with queries that have large outputs.

## Requirements
Python 3, Flask, Celery, RabbitMQ, MongoDB, SQLAlchemy, PyMongo, Docker

## Docker Images Used
- MongoDB: `FROM mongo:3.6.3-jessie`
- RabbitMQ: `FROM rabbitmq:3.7.4-management-alpine`

## Author
Stefanie Molin
