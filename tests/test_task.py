import uuid
import unittest
from typing import Text

from py_twelvelabs.models import Task
from py_twelvelabs import TwelveLabsAPIClient
from py_twelvelabs.utilities import get_logger
from py_twelvelabs.exceptions import TaskDeletionNotAllowedError


# TODO: update all tests to run independently
class TestTask(unittest.TestCase):
    """
    Test task resource.
    """

    @classmethod
    def setUpClass(cls):
        """
        Set up test fixtures.
        """

        cls.client = TwelveLabsAPIClient()
        cls.index_id = cls.client.index.create(
            f"test_index_{uuid.uuid4()}",
            ["visual", "conversation", "text_in_video", "logo"]
        )
        cls.task_id = None

        cls.logger = get_logger(__name__)

    @classmethod
    def _set_task_id(cls, task_id: Text):
        """
        Set task ID.

        :param task_id: Task ID.
        """

        cls.task_id = task_id

    @classmethod
    def _get_task_id(cls) -> Text:
        """
        Get task ID.

        :return: Task ID.
        """

        return cls.task_id
    
    def test_1_create_task_async(self):
        """
        Test create task asynchronously.
        """
        
        task_id = self.client.task.create_async(index_id=self.index_id, video_file="tests/data/test.mp4")
        self.logger.info(f"Task ID: {task_id}")

        self.assertIsNotNone(task_id)
        TestTask._set_task_id(task_id)

    def test_2_get_task(self):
        """
        Test get task.
        """

        task = self.client.task.get(TestTask._get_task_id())
        self.logger.info(f"Task: {task}")

        self.assertIsInstance(task, Task)

    def test_3_list_tasks(self):
        """
        Test list tasks.
        """

        tasks = self.client.task.list()
        self.logger.info(f"Tasks: {tasks}")

        self.assertIsInstance(tasks, list)
        self.assertGreater(len(tasks), 0)

    def test_4_delete_task(self):
        """
        Test delete task.
        """

        try:
            is_deleted = self.client.task.delete(TestTask._get_task_id())
            self.assertTrue(is_deleted)
        except TaskDeletionNotAllowedError as e:
            self.logger.info(f"Task deletion not allowed: {e}")
            self.assertIsInstance(e, TaskDeletionNotAllowedError)

    def test_5_create_task_sync(self):
        """
        Test create task synchronously.
        """

        task = self.client.task.create_sync(index_id=self.index_id, video_file="tests/data/test.mp4")
        self.logger.info(f"Task: {task}")

        self.assertIsInstance(task, Task)
        self.assertEqual(task.index_id, self.index_id)

if __name__ == "__main__":
    unittest.main()

    