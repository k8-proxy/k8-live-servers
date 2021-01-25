from pprint import pprint
from unittest import TestCase

from k8_live_servers.cloud.aws.Lambda_Setup import Lambda_Setup


class test_Lambda_Setup(TestCase):

    def setUp(self) -> None:
        self.lambda_setup = Lambda_Setup()
        self.package      = 'requests'
        print()

    def test_upload_packages_to_s3__for_elastic(self):
        result = self.lambda_setup.upload_packages_to_s3__for_elastic()
        pprint(result)


