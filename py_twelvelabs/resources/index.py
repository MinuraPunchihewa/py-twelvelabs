from typing import Text, List

from py_twelvelabs.settings import settings
from py_twelvelabs.models import Index, TaskStatus
from py_twelvelabs.exceptions import APIRequestError


class IndexResource:
    def __init__(self, client):
        self.client = client

    def create(self, index_name: Text, index_options: List[Text], engine_id: Text = settings.DEFAULT_ENGINE, addons: List[Text] = None) -> Text:
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
        
    def get_task_status(self, index_id: Text) -> TaskStatus:
        """
        Get task status.

        :param index_id: Index ID.
        :return: Task status.
        """

        response = self.client.submit_request(f"tasks/status?index_id={index_id}")
        result = response.json()
        if response.status_code == 200:
            if result is not None:
                return TaskStatus(**result)
            else:
                return None
        else:
            raise APIRequestError(f"Failed to get task status for index {index_id}: {result['message']}")
        
    def list(self, page: int = 1, page_limit: Text = 10, sort_by: Text = "created_at", sort_option: Text = "desc", _id: Text = None, index_name: Text = None, index_options: List[Text] = None) -> List[Index]:
        """
        List indexes.

        :param page: Page number.
        :param page_limit: Page limit.
        :param sort_by: Sort by.
        :param sort_option: Sort option.
        :param _id: Index ID.
        :param index_name: Index name.
        :param index_options: Index options.
        :return: List of Indexes.
        """

        params = {
            "page": page,
            "page_limit": page_limit,
            "sort_by": sort_by,
            "sort_option": sort_option,
            "_id": _id,
            "index_name": index_name,
            "index_options": index_options,
        }

        response = self.client.submit_request("indexes", params=params)
        result = response.json()
        if response.status_code == 200:
            return [Index(**index) for index in result['data']]
        else:
            raise APIRequestError(f"Failed to list indexes: {result['message']}")
        
    # TODO: add metod to list all tasks

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
            result = response.json()
            raise APIRequestError(f"Failed to update index {index_id} name: {result['message']}")
        
    def delete(self, index_id: Text) -> bool:
        """
        Delete an index.

        :param index_id: Index ID.
        :return: True if successful.
        """

        response = self.client.submit_request(f"indexes/{index_id}", method="DELETE")
        if response.status_code == 204:
            return True
        else:
            result = response.json()
            raise APIRequestError(f"Failed to delete index {index_id}: {result['message']}")