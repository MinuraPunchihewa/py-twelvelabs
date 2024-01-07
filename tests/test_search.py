import unittest

from py_twelvelabs import TwelveLabsAPIClient
from py_twelvelabs.utilities import get_logger

from tests.utilities import IndexCreator, TaskCreator


class TestSearch(unittest.TestCase):
    """
    Test search resource.
    """

    @classmethod
    def setUpClass(cls):
        """
        Set up test fixtures.
        """

        cls.client = TwelveLabsAPIClient()
        cls.index_id = IndexCreator.create_index()
        cls.task_id = TaskCreator.create_task(cls.index_id)

        cls.logger = get_logger(__name__)

    def test_1_query(self):
        """
        Test query.
        """

        results = self.client.search.query(
            self.index_id,
            "Dog getting excited",
            ["visual", "conversation", "text_in_video", "logo"],
        )
        self.logger.info(f"Response: {results}")

        self.assertIsNotNone(results)


if __name__ == "__main__":
    unittest.main()
