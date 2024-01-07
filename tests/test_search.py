import unittest

from py_twelvelabs import TwelveLabsAPIClient
from py_twelvelabs.utilities import get_logger

from tests.utilities import IndexCreator


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
        # TODO: create task

        cls.logger = get_logger(__name__)

    def test_1_query(self):
        pass
