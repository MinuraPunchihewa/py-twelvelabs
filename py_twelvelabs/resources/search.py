from typing import Text, List, Optional

from py_twelvelabs.exceptions import APIRequestError


class SearchResource:
    def __init__(self, client):
        self.client = client

    # TODO: add the filter parameter
    def query(self, index_id: Text, search_query: Text, search_options: List[Text], group_by: Optional[Text] = "clip", threshold: Optional[Text] = "low", sort_option: Text = "score", operator: Text = "or", conversation_option: Text = "semantic", page_limit: int = 10):
        """
        Query an index and return the first page of results.

        :param index_id: Index ID.
        :param search_query: Search query.
        :param search_options: Search options.
        :param group_by: Group by.
        :param threshold: Threshold.
        :param sort_option: Sort option.
        :param operator: Operator.
        :param conversation_option: Conversation option.
        :param page_limit: Page limit.
        :return: Query result.
        """

        data = {
            "index_id": index_id,
            "query": search_query,
            "search_options": search_options,
            "group_by": group_by,
            "threshold": threshold,
            "sort_option": sort_option,
            "operator": operator,
            "conversation_option": conversation_option,
            "page_limit": page_limit,
        }

        response = self.client.submit_request("search", method="POST", data=data)
        result = response.json()

        if response.status_code == 200:
            return result
        else:
            raise APIRequestError(f"Failed to query index {index_id}: {result['message']}")
        
    def get_search_result_page(self, page_token: Text):
        """
        Get a search result page.

        :param page_token: Page token.
        :return: Search result page.
        """

        response = self.client.submit_request(method="GET", endpoint=f"search/{page_token}")
        result = response.json()

        if response.status_code == 200:
            return result
        else:
            raise APIRequestError(f"Failed to get search result page: {result['message']}")
    
    # TODO: add the filter parameter
    def query_all(self, index_id: Text, search_query: Text, search_options: List[Text], group_by: Optional[Text] = "clip", threshold: Optional[Text] = "low", sort_option: Text = "score", operator: Text = "or", conversation_option: Text = "semantic", page_limit: int = 10):
        """
        Query an index and return all pages of results.

        :param index_id: Index ID.
        :param search_query: Search query.
        :param search_options: Search options.
        :param group_by: Group by.
        :param threshold: Threshold.
        :param sort_option: Sort option.
        :param operator: Operator.
        :param conversation_option: Conversation option.
        :param page_limit: Page limit.
        :return: Query result.
        """

        results = []

        result = self.query(index_id=index_id, search_query=search_query, search_options=search_options, group_by=group_by, threshold=threshold, sort_option=sort_option, operator=operator, conversation_option=conversation_option, page_limit=page_limit)
        
        while('next_page_token' in result['page_info']):
            result = self.get_search_result_page(page_token=result['page_info']['next_page_token'])
            results.append(result)
            
        return results
