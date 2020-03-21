## Preparation

Before you build/start the docker, you should change external MySQL server connection keywords in `frontend/app/update_rand.py` and `frontend_show_data/index.php`.

## Get Start

`docker-compose build`
`docker-compose up`

## Structure

+ backend-php  (backend)
  -  cases (webshell cases and no webshell cases)
  -  handler (check WAF uploaded by players)

+ backend-rabbitmq (information delivering queue between backend and frontend)

+ frontend (frontend)

+ frontend_show_data (display team rank)


