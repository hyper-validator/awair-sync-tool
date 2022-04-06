# Run on any machines

### Create environment file `.env` and update awair token, pw username and password

```
awair_token=eyJ0xxxxxxxxxxxx
pw_username=aaaa@example.com
pw_password=alj1l2j4ljfaf
```

### Run on the background

1. Ubuntu: `docker run -d --restart=always --env-file=.env kaka314/awair-sync-tool:linux`
2. Mac M1: `docker run -d --restart=always --env-file=.env kaka314/awair-sync-tool:mac-m1`


# Run locally

1. Create file `.env` from `.env.sample`, update all fields and run command `export $(grep -v '^#' .env | xargs)` to load these fields to environment

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


# This is Inspired

This project is inspired by following projects,

1. https://github.com/Sheherezadhe/awair-uploader
2. https://github.com/wwadge/awair-bridge