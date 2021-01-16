from unittest import TestCase, mock
from _tests.unittests_utils.mock_classes import FakeDatetimeDatetime
from config.conf import Settings


class Test_Settings(TestCase):

    def setUp(self):
        mock.patch("config.conf.datetime.datetime", FakeDatetimeDatetime()).start()
        self.settings_obj = Settings()

    def test_get(self):
        self.assertEqual("https://find-and-update.company-information.service.gov.uk/company/{company_number}/officers?page={page_number}",
                         self.settings_obj.get()['companies']['officer_url'])