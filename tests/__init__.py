import uuid
from typing import Text

from py_twelvelabs import TwelveLabsAPIClient


class IndexCreator:
    def __init__(self):
        self.client = TwelveLabsAPIClient()

    @staticmethod
    def _generate_random_index_name() -> Text:
        """
        Generate a random index name.

        :return: Index name.
        """

        return f"test_index_{uuid.uuid4()}"
    
    def create_index(self):
        index_id = self.client.index.create(
            self._generate_random_index_name(),
            ["visual", "conversation", "text_in_video", "logo"]
        )

        return index_id