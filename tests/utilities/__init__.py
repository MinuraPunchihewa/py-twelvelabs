import uuid
from typing import Text

from py_twelvelabs import TwelveLabsAPIClient


class IndexCreator:
    @staticmethod
    def generate_random_index_name() -> Text:
        """
        Generate a random index name.

        :return: Index name.
        """

        return f"test_index_{uuid.uuid4()}"
    
    @staticmethod
    def create_index(index_name: Text = None) -> Text:
        """
        Create index for testing.

        :param index_name: Index name.
        :return: Index ID.
        """

        client = TwelveLabsAPIClient()
        index_id = client.index.create(
            index_name if index_name else IndexCreator.generate_random_index_name(),
            ["visual", "conversation", "text_in_video", "logo"]
        )

        return index_id
    

class TaskCreator:
    @staticmethod
    def create_task(index_id: Text) -> Text:
        """
        Create task for testing.

        :param index_id: Index ID.
        :return: Task ID.
        """

        client = TwelveLabsAPIClient()
        task_id = client.task.create(index_id=index_id, video_file="tests/data/test.mp4")

        return task_id