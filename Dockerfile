FROM python:3.9

WORKDIR /awair-sync-tool-workspace

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY setup.py  ./
COPY clients ./clients
COPY handlers ./handlers

# install local package from setup.py
RUN pip install .

# start awair-sync-tool-workspace
CMD ["python3.9", "handlers/awair_sync.py"]