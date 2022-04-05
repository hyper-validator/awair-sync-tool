import os
import logging

from clients.awair_client import AwairClient
from clients.planetwatch_client import PlanetwatchClient

LOG = logging.getLogger(__name__)

def handle(event, context):
    pw_client = PlanetwatchClient(os.environ["pw_username"], os.environ["pw_password"])

    # login and get tokens
    pw_client.login()
    pw_client.list_all_sensors()

    # get latest data and push them to planetwatch
    awair_client = AwairClient(os.environ["awair_token"])
    for data in awair_client.fetch_data():
        pw_client.send_data(data)

if __name__ == "__main__":
    import time

    interval = 900 # 15 minutes

    # loop forever
    while True:
        try:
            handle(None, None)
        except Except:
            LOG.exception(f"Unknown exception")

        LOG.info(f"Start next sync in {interval/60} minutes")
        time.sleep(interval)
