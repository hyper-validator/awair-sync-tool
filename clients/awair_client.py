import requests
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
LOG = logging.getLogger(__name__)


class AwairClient:

    def __init__(self, token):
        # https://docs.developer.getawair.com/#test-requests
        self._token = token

    def fetch_devices(self):
        url = "https://developer-apis.awair.is/v1/users/self/devices"
        payload={}
        headers = {
            'Authorization': f'Bearer {self._token}'
        }
        try:
            LOG.info(f"Fetching all devices")
            response = requests.request("GET", url, headers=headers, data=payload)
            if response.status_code == 200:
                return response.json()

            LOG.error(f"Failed to fetch devices with error code: {response.status_code}, response: {response.text}")
        except requests.exceptions.RequestException:
            LOG.exception(f"Failed to fetch devices from url: {url}")


    def fetch_latest_data(self, device_type, device_id):
        url = f"https://developer-apis.awair.is/v1/users/self/devices/{device_type}/{device_id}/air-data/latest"
        payload={}
        headers = {
            'Authorization': f'Bearer {self._token}'
        }
        try:
            LOG.info(f"Fetching latest data for device id: {device_id}")
            response = requests.request("GET", url, headers=headers, data=payload)
            if response.status_code == 200:
                return response.json()

            LOG.error(f"Failed to fetch latest data with error code: {response.status_code}, resonse: {response.text}")
        except requests.exceptions.RequestException:
            LOG.exception(f"Failed to fetch latest data from url: {url}")
        

    def fetch_data(self):
        devices = self.fetch_devices()
        if not devices:
            LOG.warning("No device found!")
            return

        for device in devices["devices"]:
            LOG.info(f"Syncing data for device: {device['deviceId']}")
            latest_data = self.fetch_latest_data(device["deviceType"], device["deviceId"])

            yield {
                "deviceId": device["deviceUUID"],
                **latest_data["data"][0]
            }

if __name__ == "__main__":
    import os
    client = AwairClient(os.environ["awair_token"])
    for data in client.fetch_data():
        print(data)
