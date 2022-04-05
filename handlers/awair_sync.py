import os

from clients.awair_client import AwairClient
from clients.planetwatch_client import PlanetwatchClient

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
    handle(None, None)
