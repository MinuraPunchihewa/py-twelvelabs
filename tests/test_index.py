import uuid
import unittest
from typing import Text

from py_twelvelabs.models import Index
from py_twelvelabs import TwelveLabsAPIClient
from py_twelvelabs.utilities import get_logger


# TODO: update all tests to run independently
class TestIndex(unittest.TestCase):
    """
    Test index resource.
    """

    @classmethod
    def setUpClass(cls):
        """
        Set up test fixtures.
        """

        cls.client = TwelveLabsAPIClient()
        cls.index_name = f"test_index_{uuid.uuid4()}"
        cls.index_id = None

        cls.logger = get_logger(__name__)
    
    @classmethod
    def _set_index_id(cls, index_id: Text):
        """
        Set index ID.

        :param index_id: Index ID.
        """

        cls.index_id = index_id
    
    @classmethod
    def _get_index_id(cls) -> Text:
        """
        Get index ID.

        :return: Index ID.
        """

        return cls.index_id    

    def test_1_create_index(self):
        """
        Test create index.
        """

        index_id = self.client.index.create(
            self.index_name,
            ["visual", "conversation", "text_in_video", "logo"]
        )
        self.logger.debug(f"Index ID: {index_id}")

        self.assertIsNotNone(index_id)
        TestIndex._set_index_id(index_id)

    def test_2_get_index(self):
        """
        Test get index.
        """

        index = self.client.index.get(TestIndex._get_index_id())
        self.logger.debug(f"Index: {index}")

        self.assertIsInstance(index, Index)
        self.assertEqual(index.index_name, self.index_name)

    def test_3_get_task_status(self):
        """
        Test get task status.
        """

        task_status = self.client.index.get_task_status(TestIndex._get_index_id())
        self.logger.debug(f"Task status: {task_status}")

        self.assertIsNotNone(task_status)
        self.assertEqual(task_status.index_id, TestIndex._get_index_id())

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
        is_updated = self.client.index.update(TestIndex._get_index_id(), new_index_name)
        self.assertTrue(is_updated)

        index = self.client.index.get(TestIndex._get_index_id())
        self.logger.debug(f"Index: {index}")
        self.assertEqual(index.index_name, new_index_name)

    def test_6_delete_index(self):
        """
        Test delete index.
        """

        is_deleted = self.client.index.delete(TestIndex._get_index_id())
        self.assertTrue(is_deleted)

        index = self.client.index.get(TestIndex._get_index_id())
        self.assertTrue(index.deleted)


if __name__ == "__main__":
    unittest.main()