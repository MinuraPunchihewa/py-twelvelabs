import uuid
import unittest
from typing import Text

from py_twelvelabs.models import Task
from py_twelvelabs import TwelveLabsAPIClient
from py_twelvelabs.utilities import get_logger

from tests.utilities import IndexCreator


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
        cls.index_id = IndexCreator.create_index()
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
    
    def test_1_create_task(self):
        """
        Test create task.
        """
        
        task_id = self.client.task.create(index_id=self.index_id, video_url="https://mindsdb-s3-integration-verification.s3.eu-north-1.amazonaws.com/test.mp4?response-content-disposition=inline&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEBIaDmFwLXNvdXRoZWFzdC0xIkcwRQIgTOX2Wp6HpIEbSmVbWrPgk0FnbOWobC2pQrEIFDJCoYYCIQCl4LE4rA%2FEDBf9tOfnfaqURtX1fv4wUgKYiLH6i1SE1CqOAwir%2F%2F%2F%2F%2F%2F%2F%2F%2F%2F8BEAMaDDg0Njc2MzA1MzkyNCIMRkWQA4CCC7H62K1FKuICnG5vXAruXvxTwxiB%2FnIwWcLL2wrF3Vwj8JCxfqzCHM2HS5QOicizugQxMrnDYpQBmYl6jr47kbiLAaEMYdqCfrC%2FR8vsbp8%2FJ8H8%2BhL8L3hmfRDu26q9C%2BOdLiqyfq5%2B9QiIukRWAMD3g6zTxk2jRlKd7kanVJ47MWMZczTgn6iuAaFnPOtsLavyggBqO%2BHdgpFFnnUM65KcqejmkW%2BIQDSTearIplCQNd%2FyfKflArryJ066O1kMkMOxtI02L%2BVJx7y%2FFHl2zLk6w8womJA%2F8PAGKMbP7fmegUho%2FiG6RhcQIXRdeh9FklUnosnEBAQP3Z0Kje2jclwgWXJGebkDgHpyUVUVtgQNyYMl7XRzqub97M6E0ECR9eKnGkQR6q%2FixqJqUM3%2B%2FM%2BsDhsvodkoVUYpZZ2VWO7chhzB0NF71epfBWbrgM3rtiwcb6mCFNB6HMSB%2Fg3kJZdsibkMCMCN75%2BZMIKe5qwGOrMCtGVxKsPKZOKVgET3rsqXiTyTy%2F6KQf%2Brz7IOb3zQE7r5%2BaTwjmKAgJxk8SfjwcnIh3QehZL82ZvXT%2FEiVjSZj%2ByW7T0YWN6mjbrMa0UrF6WN0v0mZGxx2xpQz07M4h7PmJatC8g5%2F%2F9MzSJeUJuEh7XJiy5yH3RfJ7rLMBLAbL%2B2YkjxU1KcmfdeBlGyp4CKL8Mytfpx89GlT5YNrP5m8Yg1iabp8dq0w4Yno4kPkoA0JgKdJXz8UZYoe2SNercKDzU%2BKg9reWZsDD%2FSYKTUewAgv284pu2DPMv4A3EdLqvIJMnp5uVgYRRwNeIflX5wTxLdDDXzsM9F%2BK0FeN2zbHxGdqWZ4nmPrw9r%2FKH%2BFnn4oEjnO%2BSrNMjFMsEzaeHzj3hC%2BvWFV61wrSe07nMSg%2BDLPw%3D%3D&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20240106T173459Z&X-Amz-SignedHeaders=host&X-Amz-Expires=43200&X-Amz-Credential=ASIA4KJYC2NSLKMHCL3A%2F20240106%2Feu-north-1%2Fs3%2Faws4_request&X-Amz-Signature=cc49904edd911f025a54bbfe8cd6efc7997037f86706c26ada37f08814038346")
        self.logger.info(f"Task ID: {task_id}")

        self.assertIsNotNone(task_id)
        TestTask._set_task_id(task_id)

    def test_2_get_task(self):
        """
        Test get task.
        """

        task = self.client.task.get('TestTask._get_task_id()')
        self.logger.info(f"Task: {task}")

        self.assertIsInstance(task, Task)


if __name__ == "__main__":
    unittest.main()

    