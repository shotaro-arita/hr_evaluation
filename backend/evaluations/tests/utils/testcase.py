import inject
from rest_framework.test import APIClient, APITestCase

from evaluations.tests.utils.entity_factory import Counter


class MyAPITestCase(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        # inject.configure_once(mock_injection_config)
        pass

    def setUp(self) -> None:
        super().setUp()
        Counter.reset()
