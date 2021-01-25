from pprint import pprint
from unittest import TestCase

from k8_live_servers.servers.Icap_AWS_EC2 import Icap_AWS_EC2


class test_Icap_AWS_EC2(TestCase):

    def setUp(self) -> None:
        self.icap_aws_ec2 = Icap_AWS_EC2()
        print()

    def test_elastic_update_server_metadata(self):
        items_updated         = self.icap_aws_ec2.elastic_update_server_metadata()
        assert items_updated == len(self.icap_aws_ec2.live_servers())