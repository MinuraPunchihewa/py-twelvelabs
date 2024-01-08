import uuid
import unittest
from typing import Text

from py_twelvelabs.models import Index
from py_twelvelabs import TwelveLabsAPIClient
from py_twelvelabs.utilities import get_logger


class TestIndex(unittest.TestCase):
    """
    Test index resource.
    """

    @classmethod
    def setUpClass(cls):
        """
        Set up test fixtures.
        """

        cls.logger = get_logger(__name__)

    def setUp(self):
        """
        Set up test fixtures for each test: initialize client, generate a random name for an index and create an index using that name.
        """

        self.client = TwelveLabsAPIClient()
        self.index_name = f"test_index_{uuid.uuid4()}"
        self.index_id = self.client.index.create(
            self.index_name,
            ["visual", "conversation", "text_in_video", "logo"]
        )

    def tearDown(self):
        """
        Tear down test fixtures after each test: delete the created index.
        """

        self.client.index.delete(self.index_id)

    def test_1_create_index(self):
        """
        Test create index.
        """

        self.assertIsNotNone(self.index_id)

    def test_2_get_index(self):
        """
        Test get index.
        """

        index = self.client.index.get(self.index_id)
        self.logger.debug(f"Index: {index}")

        self.assertIsInstance(index, Index)

    def test_3_get_task_status(self):
        """
        Test get task status.
        """

        task_status = self.client.index.get_task_status(self.index_id)
        self.logger.debug(f"Task status: {task_status}")

        if task_status is not None:
            self.assertEqual(task_status.index_id, self.index_id)

    def test_4_list_indexes(self):
        """
        Test list indexes.
        """

        indexes = self.client.index.list()
        self.logger.debug(f"Indexes: {indexes}")

        self.assertIsInstance(indexes, list)
        self.assertTrue(len(indexes) > 0)

    def test_5_update_index_name(self):
        """
        Test update index name.
        """

        new_index_name = self.index_name + "_updated"
        is_updated = self.client.index.update(self.index_id, new_index_name)
        self.assertTrue(is_updated)

        index = self.client.index.get(self.index_id)
        self.logger.debug(f"Index: {index}")
        self.assertEqual(index.index_name, new_index_name)

    def test_6_delete_index(self):
        """
        Test delete index.
        """

        is_deleted = self.client.index.delete(self.index_id)
        self.assertTrue(is_deleted)

        index = self.client.index.get(self.index_id)
        self.assertTrue(index.deleted)


if __name__ == "__main__":
    unittest.main()