from typing import Text, Dict, List

from py_twelvelabs.models import Index
from py_twelvelabs.exceptions import APIRequestError

# TODO: move to config
DEFAULT_ENGINE = "marengo2.5"


class IndexResource:
    def __init__(self, client):
        self.client = client

    def create(self, index_name: Text, index_options: List[Text], engine_id: Text = DEFAULT_ENGINE, addons: List[Text] = None) -> Text:
        """
        Create an index.

        :param index_name: Index name.
        :param engine_id: Engine ID. 
        :param index_options: Index options.
        :param addons: Addons.
        :return: Index ID.
        """

        data = {
            "index_name": index_name,
            "engine_id": engine_id,
            "index_options": index_options,
            "addons": addons,
        }

        response = self.client.submit_request("indexes", method="POST", data=data)
        result = response.json()
        if response.status_code == 201:
            return result['_id']
        else:
            raise APIRequestError(f"Failed to create index {index_name}: {result['message']}")

    def get(self, index_id: Text) -> Index:
        """
        Get an index.

        :param index_id: Index ID.
        :return: Index.
        """
        
        response = self.client.submit_request(f"indexes/{index_id}")
        result = response.json()
        if response.status_code == 200:
            return Index(**result)
        else:
            raise APIRequestError(f"Failed to get index {index_id}: {result['message']}")

    def update(self, index_id: Text, index_name: Text) -> bool:
        """
        Update an index name.

        :param index_id: Index ID.
        :param index_name: Index name.
        :return: True if successful.
        """

        response = self.client.submit_request(f"indexes/{index_id}", headers={"accept": "application/json"}, method="PUT", data={"index_name": index_name})
        if response.status_code == 200:
            return True
        else:
            raise APIRequestError(f"Failed to update index {index_id} name: {result['message']}")