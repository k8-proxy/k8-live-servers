from pprint import pprint
from unittest import TestCase

from k8_kubectl.helpers.to_add_to_sbot.OSBot_Utils__Local import flist
from k8_live_servers.Live_Servers import Live_Servers
from k8_live_servers.icap.Server_EC2 import Server_EC2


class test_Server_EC2(TestCase):

    def setUp(self):
        self.server_ip = flist(Live_Servers().icap_aws_ec2()).first()
        self.server_ec2 = Server_EC2(self.server_ip)

    def test_exec_command(self):
        assert self.server_ec2.exec_command('uname').get('output').strip() == 'Linux'

    def test_gw_logs_folder_size(self):
        pprint(self.server_ec2.gw_logs_folder_size())