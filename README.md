# Run locally

1. Update file `.env`

2. Run following commands

```
python3 -m venv .venv
. .venv/bin/activate
pip3 install -r requirements.txt
pip3 install .
python3 handlers/awair_sync.py
```

# Deploy to AWS (currently not working due to cloudflare issues)

Deploy to AWS using `serverless deploy`


# Docker

```
  docker build -f Dockerfile . -t awair-sync-tool
  docker run --env-file .env -it --rm awair-sync-tool
```

To start the feed using docker compose: `docker-compose up`, this will load the .env automatically.