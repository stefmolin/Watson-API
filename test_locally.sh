docker network create frontend --scope swarm --driver overlay
docker network create watson_api --scope swarm --driver overlay
docker-compose build
docker stack rm watson_api
sleep 2
docker stack deploy -c docker-compose.yml watson_api
# sleep 35
# curl -m 5 -i -X POST '127.0.0.1:53865/api/v1/query/sherlock/campaign_lookup?client_id=5535'
