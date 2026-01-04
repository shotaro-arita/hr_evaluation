import inject
from rest_framework.test import APITestCase

from evaluations.tests.utils.entity_factory import Counter
from evaluations.utils.mock_injection_config import mock_injection_config


class MyAPITestCase(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        inject.clear_and_configure(mock_injection_config)
        pass

    def setUp(self) -> None:
        super().setUp()
        Counter.reset()
