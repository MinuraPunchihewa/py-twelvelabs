import os
import json
import requests
from typing import Text, Dict

from .models import Index
from .utilities import get_logger
from .exceptions import MissingAPIKeyError, MethodNotImplementedError, APIRequestError

# TODO: move to config
BASE_API_URL = "https://api.twelvelabs.io"
API_VERSION = "v1.1"
DEFAULT_ENGINE = "marengo2.5"
DEFAULT_WAIT_DURATION = 5


class TwelveLabsAPIClient:
    """
    Twelve Labs API client.
    """

    def __init__(self, api_key: Text = None):
        """
        Initialize the Twelve Labs API client.
        """

        self.api_key = self._get_api_key(api_key)
        self.logger = get_logger(__name__)

    def get_index(self, index_id: Text) -> Dict:
        """
        Get an index.

        :param index_id: Index ID.
        :return: Index.
        """
        
        response = self._submit_request(f"indexes/{index_id}")
        result = response.json()
        if response.status_code == 200:
            return Index(**result)
        else:
            raise APIRequestError(f"Failed to get index {index_id}: {result['message']}")

    def update_index_name(self, index_id: Text, index_name: Text) -> Dict:
        """
        Update an index name.

        :param index_id: Index ID.
        :param index_name: Index name.
        :return: True if successful.
        """

        response = self._submit_request(f"indexes/{index_id}", headers={"accept": "application/json"}, method="PUT", data={"index_name": index_name})
        if response.status_code == 200:
            return True
        else:
            raise APIRequestError(f"Failed to update index {index_id} name: {result['message']}")

    def _get_api_key(self, api_key: Text = None) -> Text:
        """
        Get the API key.

        The API key can be provided as an argument or as the environment variable TWELVE_LABS_API_KEY.

        :param api_key: API key.
        :return: API key.
        """

        if api_key is None:
            api_key = os.environ.get('TWELVE_LABS_API_KEY', None)
        if api_key is None:
            raise MissingAPIKeyError('API key must be provided.')
        return api_key

    def _get_headers(self, headers: Dict = None) -> Dict:
        """
        Get request headers.

        :param headers: Request headers.
        :return: Request headers.
        """

        if headers is None:
            headers = {}

        headers.update({
            'Content-Type': 'application/json',
            'x-api-key': self.api_key
        })
        return headers

    def _get_url(self, endpoint: str) -> Text:
        """
        Get the API URL.

        :param endpoint: API endpoint.
        :return: API URL.
        """

        return f"{BASE_API_URL}/{API_VERSION}/{endpoint}"

    def _submit_request(self, endpoint: str, headers: Dict = None, params: Dict = None, data: Dict = None, method: str = "GET") -> Dict:
        """
        Submit a request to the Twelve Labs API.

        :param endpoint: API endpoint.
        :param headers: Request headers. The API key and content type are automatically added.
        :param params: Request parameters.
        :param data: Request data.
        :param method: HTTP method.
        :return: Response data.
        """

        url = self._get_url(endpoint)
        headers = self._get_headers(headers)

        if method == "GET":
            response = requests.get(
                url=url,
                headers=headers,
                params=params,
            )

        elif method == "POST":
            response = requests.post(
                url=url,
                headers=headers,
                json=data,
            )

        elif method == "PUT":
            response = requests.put(
                url=url,
                headers=headers,
                json=data,
            )

        else:
            raise MethodNotImplementedError(f"Method {method} not implemented yet.")

        return response
