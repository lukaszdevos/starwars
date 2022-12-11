import os
from urllib.parse import urljoin

import requests

from utils.exceptions import EndpointTimeout, UnexpectedApiError


class SwapiAdapter:
    def __init__(self):
        self.base_url = os.environ.get("SWAPI_URL")

    def get_characters(self, **kwargs) -> dict[str, str]:
        endpoint = (
            f"{urljoin(self.base_url, 'api/people')}?page={kwargs.get('page', '1')}"
        )
        return self._call_api("GET", endpoint)

    def get_planets(self, **kwargs) -> dict[str, str]:
        endpoint = (
            f"{urljoin(self.base_url, 'api/planets')}?page={kwargs.get('page', '1')}"
        )
        return self._call_api("GET", endpoint)

    def _call_api(self, method: str, url: str, **kwargs) -> dict[str, str]:
        try:
            response = requests.request(method, url, verify=False, **kwargs)
        except requests.ConnectionError:
            raise EndpointTimeout("Connection error")
        if response.status_code == 200:
            return response.json()
        else:
            raise UnexpectedApiError("Something goes wrong")
