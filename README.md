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

# Deploy to AWS

Deploy to AWS using `serverless deploy` 