from pprint                       import pprint
from unittest                     import TestCase
from osbot_utils.utils.Files      import file_exists
from osbot_utils.utils.Misc       import sorted_set
from k8_live_servers.Live_Servers import Live_Servers


class test_Live_Servers(TestCase):

    def setUp(self):
        self.live_servers = Live_Servers()
        print()

    def test__init__(self):
        assert file_exists(self.live_servers.path_live_servers)

    def test_icap_aws_ec2(self):
        assert len(self.live_servers.icap_aws_ec2()) > 0

    def test_icap(self):
        sorted_set(self.live_servers.icap()) == ['aws-ec2', 'azure-aks', 'azure-rancher', 'vmware-esxi', 'vmware-vcenter']
        pprint(self.live_servers.icap())
