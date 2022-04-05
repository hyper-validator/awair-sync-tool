import cloudscraper
import logging

from urllib import parse
from bs4 import BeautifulSoup

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
LOG = logging.getLogger(__name__)

class PlanetwatchClient:
    PLANET_AUTH_URL = "https://login.planetwatch.io/auth/"
    CLIENT_ID       = "external-login"
    REALM_NAME      = "Planetwatch"

    def __init__(self, username, password):
        self._scraper = cloudscraper.create_scraper(browser="chrome")
        self._auth_url = (
            f"{self.PLANET_AUTH_URL}realms/Planetwatch/protocol/openid-connect/auth"
            f"?client_id=external-login&response_type=code&redirect_uri="
        )
        self._token_url = "https://login.planetwatch.io/auth/realms/Planetwatch/protocol/openid-connect/token"
        
        self._access_token = None
        self._refresh_token = None

        self._username = username
        self._password = password

    def _extract_login_url(self, text):
        soup = BeautifulSoup(text, 'html.parser')
        login_url = soup.find(id="kc-form-login")["action"].replace("&amp;", "&")
        return login_url
        
    def login(self):
        # step 1: auth
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
        }
        payload = {
            "client_id": self.CLIENT_ID,
            "redirect_uri": "",
            "scope": "openid offline_access",
            "esponse_type": "code",
        }
        response = self._scraper.get(self._auth_url, headers=headers, data=payload)
        if response.status_code != 200:
            LOG.error(f"Failed to initiate authrization using: {self._auth_url}, resopnse: {response.text}")
            return

        login_url = self._extract_login_url(response.text)
        LOG.info(f"Login using url: {login_url}")


        # step 2: login
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "*/*",
        }
        payload = {
            "username": self._username,
            "password": self._password,
            "cookies": response.cookies,
        }
        # do not redirect to get the 'code'
        response = self._scraper.post(login_url, data=payload, headers=headers, allow_redirects = False)
        LOG.info(f"Login resonse code: {response.status_code}") # http code: 302
        if response.status_code != 302:
            LOG.error(f"Failed to login with {login_url}")
            return

        query = parse.parse_qs(parse.urlparse(response.headers["Location"]).query)
        code = query['code'][0]
        LOG.info(f"code returned from successful login: {code}")


        # step 3: get tokens
        token_url = "https://login.planetwatch.io/auth/realms/Planetwatch/protocol/openid-connect/token"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        }
        payload = {
            "grant_type": "authorization_code",
            "client_id": self.CLIENT_ID,
            "redirect_uri": "",
            "code": code,
        }
        response = self._scraper.post(self._token_url, data=payload, headers=headers)
        if response.status_code != 200:
            LOG.error(f"Failed to get access token using {token_url} with payload {payload}")
            return

        self._access_token = response.json()["access_token"]
        self._refresh_token = response.json()["refresh_token"]
        LOG.info(f"Access token: {self._access_token}")


    def list_all_sensors(self):
        if not self._access_token:
            LOG.error(f"Invalid access token, please login first")
            return

        headers = {
            'Authorization': f'Bearer {self._access_token}'
        }
        response = self._scraper.get("https://wearableapi.planetwatch.io/api/sensors", headers=headers)
        LOG.info(f"Sensors: {response.json()}")


    def send_data(self, data):
        if not self._access_token:
            LOG.error(f"Invalid access token, please login first")
            return

        LOG.info(f"Sending data: {data}")
        headers = {
            "Accept": "application/json",
            'Authorization': f'Bearer {self._access_token}'
        }
        response = self._scraper.post(
            "https://wearableapi.planetwatch.io/api/data/devicedata", json=data, headers=headers
        )
        LOG.info(response.status_code)
        LOG.info(response.text)

    
if __name__ == "__main__":
    import os
    pw_client = PlanetwatchClient(os.environ["pw_username"], os.environ["pw_password"])
    pw_client.login()
    pw_client.list_all_sensors()

    from awair_client import AwairClient
    awair_client = AwairClient(os.environ["awair_token"])
    for data in awair_client.fetch_data():
        pw_client.send_data(data)
