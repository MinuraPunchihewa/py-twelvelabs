import os
import requests
from typing import Text, Dict
from requests_toolbelt.multipart.encoder import MultipartEncoder

from py_twelvelabs.settings import settings
from py_twelvelabs.utilities.logger import get_logger
from py_twelvelabs.resources import IndexResource, TaskResource, SearchResource
from py_twelvelabs.exceptions import MissingAPIKeyError, MethodNotImplementedError


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

        self.index = IndexResource(self)
        self.task = TaskResource(self)
        self.search = SearchResource(self)

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

        return f"{settings.BASE_API_URL}/{settings.API_VERSION}/{endpoint}"

    def submit_request(self, endpoint: str, headers: Dict = None, params: Dict = None, data: Dict = None, method: str = "GET") -> requests.Response:
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

        elif method == "DELETE":
            response = requests.delete(
                url=url,
                headers=headers,
            )

        else:
            raise MethodNotImplementedError(f"Method {method} not implemented yet.")

        return response

    def submit_multi_part_request(self, endpoint: str, data: Dict, headers: Dict = None, method: str = "GET") -> requests.Response:
        """
        Submit a multi-part request to the Twelve Labs API.

        :param endpoint: API endpoint.
        :param headers: Request headers. The API key and content type are automatically added.
        :param data: Request data.
        :param method: HTTP method.
        :return: Response data.
        """

        url = self._get_url(endpoint)
        headers = self._get_headers(headers)

        multipart_data = MultipartEncoder(fields=data)
        headers['Content-Type'] = multipart_data.content_type

        if method == "POST":
            response = requests.post(
                url=url,
                headers=headers,
                data=multipart_data,
            )

        else:
            raise MethodNotImplementedError(f"Method {method} not supported yet.")

        return response
